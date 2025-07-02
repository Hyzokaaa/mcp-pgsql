# app/api/routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio

from app.agent.agent import ask, create_history
from app.agent.models import create_llm
from app.agent.tools import load_tools
from app.core.config import Config
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

router = APIRouter()

# Modelos Pydantic para request/response
class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    
class ChatResponse(BaseModel):
    response: str
    status: str = "success"

# Instancias globales (se inicializan una vez)
llm = None
tools = None

def initialize_agent():
    """Inicializa el LLM y las herramientas una sola vez"""
    global llm, tools
    if llm is None:
        llm = create_llm(Config.MODEL)
        tools = load_tools()
        
def messages_to_langchain(messages: List[ChatMessage]):
    """Convierte mensajes de la API a formato LangChain"""
    history = []
    for msg in messages:
        if msg.role == "user":
            history.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            history.append(AIMessage(content=msg.content))
        elif msg.role == "system":
            history.append(SystemMessage(content=msg.content))
    return history

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint principal que recibe mensajes y devuelve respuesta del agente
    """
    try:
        # Inicializar agente si es necesario
        initialize_agent()
        
        # Convertir mensajes a formato LangChain
        history = messages_to_langchain(request.messages)
        
        # Obtener el último mensaje del usuario como prompt
        user_messages = [msg for msg in request.messages if msg.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No se encontró mensaje del usuario")
            
        latest_prompt = user_messages[-1].content
        
        # Remover el último mensaje del historial (se pasará como query)
        if history and isinstance(history[-1], HumanMessage):
            history = history[:-1]
        
        # Bindear herramientas al LLM
        llm_with_tools = llm.bind_tools(tools)
        
        # Procesar con el agente
        response = await ask(
            query=latest_prompt,
            history=history,
            llm=llm_with_tools,
            available_tools=tools
        )
        
        return ChatResponse(response=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando consulta: {str(e)}")

@router.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {"status": "healthy", "service": "SQL Agent API"}
