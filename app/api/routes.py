# app/api/routes.py
"""
Rutas de la API REST para el agente SQL.

Este módulo define todos los endpoints de la API FastAPI que permiten
interactuar con el agente SQL a través de HTTP. Incluye:

- Endpoint principal de chat para consultas SQL
- Endpoint de health check para monitoreo
- Modelos Pydantic para validación de request/response
- Gestión de estado global para LLM y herramientas
- Conversión entre formatos de mensajes

El endpoint principal recibe mensajes en formato de chat y los procesa
usando el agente SQL que puede ejecutar consultas y analizar bases de datos.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio

from app.agent.agent import ask, create_history
from app.agent.models import create_llm
from app.agent.tools import load_tools
from app.core.config import Config
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Router de FastAPI para agrupar todas las rutas
router = APIRouter()

# === MODELOS PYDANTIC PARA REQUEST/RESPONSE ===

class ChatMessage(BaseModel):
    """
    Modelo para representar un mensaje individual en el chat.

    Attributes:
        role: Rol del mensaje ("user", "assistant", "system")
        content: Contenido textual del mensaje
    """
    role: str      # "user" = usuario, "assistant" = agente, "system" = instrucciones
    content: str   # Texto del mensaje

class ChatRequest(BaseModel):
    """
    Modelo para el request del endpoint de chat.

    Attributes:
        messages: Lista de mensajes que forman la conversación
    """
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    """
    Modelo para la respuesta del endpoint de chat.

    Attributes:
        response: Respuesta generada por el agente SQL
        status: Estado de la operación (default: "success")
    """
    response: str
    status: str = "success"

# === ESTADO GLOBAL DE LA APLICACIÓN ===

# Instancias globales que se inicializan una vez al primer uso
# Esto evita reinicializar el LLM y herramientas en cada request
llm = None      # Instancia del modelo de lenguaje
tools = None    # Lista de herramientas disponibles para el agente

def initialize_agent():
    """
    Inicializa el LLM y las herramientas del agente una sola vez.

    Esta función utiliza variables globales para mantener las instancias
    del modelo y herramientas, evitando la sobrecarga de inicialización
    en cada request HTTP.

    Global Variables:
        llm: Instancia del modelo de lenguaje de Ollama
        tools: Lista de herramientas SQL disponibles
    """
    global llm, tools
    if llm is None:  # Inicializar solo si no existe
        llm = create_llm(Config.MODEL)    # Crear conexión con Ollama
        tools = load_tools()              # Cargar herramientas SQL

def messages_to_langchain(messages: List[ChatMessage]):
    """
    Convierte mensajes de la API REST a formato LangChain.

    Args:
        messages: Lista de mensajes en formato de la API

    Returns:
        List: Lista de mensajes en formato LangChain (HumanMessage, AIMessage, SystemMessage)
    """
    history = []
    for msg in messages:
        # Mapear cada tipo de rol a su clase correspondiente en LangChain
        if msg.role == "user":
            history.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            history.append(AIMessage(content=msg.content))
        elif msg.role == "system":
            history.append(SystemMessage(content=msg.content))
    return history

# === ENDPOINTS DE LA API ===

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint principal que procesa consultas SQL usando el agente.

    Este endpoint recibe una conversación de chat y utiliza el agente SQL
    para generar respuestas. El agente puede ejecutar consultas SQL,
    analizar esquemas de base de datos y proporcionar información detallada.

    Args:
        request: Objeto ChatRequest con lista de mensajes

    Returns:
        ChatResponse: Respuesta del agente con el resultado de la consulta

    Raises:
        HTTPException: 400 si no hay mensajes de usuario
        HTTPException: 500 si hay errores en el procesamiento
    """
    try:
        # Inicializar agente si es la primera vez
        initialize_agent()

        # Convertir mensajes de API REST a formato LangChain
        history = messages_to_langchain(request.messages)

        # Extraer el último mensaje del usuario como consulta actual
        user_messages = [msg for msg in request.messages if msg.role == "user"]
        if not user_messages:
            raise HTTPException(
                status_code=400,
                detail="No se encontró mensaje del usuario"
            )

        latest_prompt = user_messages[-1].content

        # Remover el último mensaje del historial
        # (se pasará por separado como query al agente)
        if history and isinstance(history[-1], HumanMessage):
            history = history[:-1]

        # Asociar herramientas al modelo de lenguaje
        llm_with_tools = llm.bind_tools(tools)

        # Procesar la consulta usando el agente SQL
        response = await ask(
            query=latest_prompt,           # Consulta actual del usuario
            history=history,               # Historial de conversación previa
            llm=llm_with_tools,           # Modelo con herramientas asociadas
            available_tools=tools          # Herramientas disponibles
        )

        return ChatResponse(response=response)

    except Exception as e:
        # Capturar y reportar cualquier error durante el procesamiento
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando consulta: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """
    Endpoint de verificación de salud del servicio.

    Utilizado para monitoreo y verificar que la API está funcionando
    correctamente. No requiere autenticación ni parámetros.

    Returns:
        dict: Estado del servicio y nombre del mismo
    """
    return {
        "status": "healthy",
        "service": "SQL Agent API"
    }
