# app/agent/models.py
"""
Módulo de configuración de modelos de lenguaje para el agente SQL.

Este módulo se encarga de crear y configurar instancias de modelos de lenguaje
que serán utilizados por el agente SQL. Actualmente soporta Ollama como
proveedor de LLM, con configuración optimizada para tool calling y
procesamiento de consultas SQL.

Funcionalidades:
- Creación de instancias de ChatOllama configuradas
- Optimización para tool calling con bases de datos
- Configuración de parámetros de rendimiento
- Gestión de contexto y temperatura

La configuración está optimizada para:
- Respuestas determinísticas (temperatura 0.0)
- Ventana de contexto amplia para consultas complejas
- Persistencia del modelo en memoria (keep_alive=-1)
- Desactivación de streaming para compatibilidad con tools
"""

from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from app.core.config import Config, ModelConfig
import httpx

def create_llm(model_config: ModelConfig) -> BaseChatModel:
    """
    Crea y configura una instancia de modelo de lenguaje para el agente SQL.

    Esta función inicializa un modelo ChatOllama con configuración optimizada
    para el análisis de bases de datos y tool calling. Los parámetros están
    ajustados para proporcionar respuestas determinísticas y mantener el
    modelo cargado en memoria para mejor rendimiento.

    Args:
        model_config: Configuración del modelo conteniendo nombre y temperatura

    Returns:
        BaseChatModel: Instancia configurada de ChatOllama lista para usar

    Configuration:
        - model: Nombre del modelo en Ollama (ej: "qwen3:0.6b")
        - temperature: Nivel de aleatoriedad (0.0 = determinístico)
        - num_ctx: Tamaño de ventana de contexto desde configuración global
        - verbose: Deshabilitado para logs limpios
        - keep_alive: -1 mantiene el modelo en memoria indefinidamente
        - disable_streaming: Requerido para compatibilidad con tool calling

    Example:
        >>> model_config = ModelConfig(name="qwen3:0.6b", temperature=0.0)
        >>> llm = create_llm(model_config)
        >>> # El modelo está listo para ser usado con herramientas
        >>> llm_with_tools = llm.bind_tools(tools)

    Note:
        El modelo debe estar disponible en la instancia de Ollama configurada.
        Si el modelo no existe, Ollama intentará descargarlo automáticamente.
    """
    return ChatOllama(
        model=model_config.name,                    # Nombre del modelo en Ollama
        temperature=model_config.temperature,       # Determinismo en respuestas
        num_ctx=Config.OLLAMA_CONTEXT_WINDOW,      # Tamaño de ventana de contexto
        verbose=False,                              # Logs silenciosos
        keep_alive=-1,                              # Mantener modelo en memoria
        disable_streaming=True,                     # Requerido para tool calling
    )