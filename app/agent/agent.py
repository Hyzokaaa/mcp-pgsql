# app/agent/agent.py
"""
Módulo principal del agente SQL conversacional.

Este módulo implementa la lógica central del agente que puede interactuar con bases
de datos usando herramientas SQL y un modelo de lenguaje. El agente utiliza un patrón
de conversación iterativo donde puede:

- Recibir consultas en lenguaje natural
- Usar herramientas para ejecutar consultas SQL
- Analizar resultados y proporcionar respuestas contextualmente relevantes
- Mantener un historial de conversación

Funcionalidades principales:
- Procesamiento asíncrono de consultas
- Gestión de herramientas (tools) con validación
- Logging detallado de operaciones
- Control de iteraciones máximas para evitar bucles infinitos
- Manejo robusto de errores en herramientas
"""

import asyncio
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool

from app.agent.logging_local import (
    blue_border_style,
    green_border_style,
    yellow_border_style,
    magenta_border_style,
    log_panel,
)
from app.agent.prompt_builder import build_system_prompt
from app.core.config import Config

async def ask(
    query: str,
    history: list[BaseMessage],
    llm: BaseChatModel,
    available_tools: list[BaseTool],
    max_iteration: int = Config.Agent.MAX_ITERATIONS,
) -> str:
    """
    Procesa una consulta del usuario usando el agente SQL conversacional.

    Esta función implementa el ciclo principal del agente:
    1. Prepara el contexto con historial y prompt del sistema
    2. Envía la consulta al modelo de lenguaje
    3. Ejecuta herramientas según las decisiones del modelo
    4. Itera hasta obtener una respuesta final o alcanzar el límite

    Args:
        query: Consulta del usuario en lenguaje natural
        history: Historial previo de mensajes de la conversación
        llm: Modelo de lenguaje con herramientas vinculadas
        available_tools: Lista de herramientas SQL disponibles
        max_iteration: Máximo número de iteraciones permitidas

    Returns:
        str: Respuesta final del agente

    Raises:
        ValueError: Si se solicita una herramienta que no existe
        RuntimeError: Si se alcanza el máximo de iteraciones sin respuesta final
    """
    # Preparar mensajes con prompt del sistema si no existe
    if not history or not isinstance(history[0], SystemMessage):
        system_prompt = build_system_prompt()
        messages = [SystemMessage(content=system_prompt)] + history
    else:
        messages = history.copy()

    # Logging de la consulta del usuario
    log_panel(title="User Request", content=query, border_style=green_border_style)
    messages.append(HumanMessage(content=query))

    # Crear mapeo de herramientas por nombre para acceso rápido
    tools_by_name = {tool.name: tool for tool in available_tools}
    n_iterations = 0

    # Ciclo principal del agente
    while n_iterations < max_iteration:
        # Invocar modelo de lenguaje con el contexto actual
        response = await llm.ainvoke(messages)
        messages.append(response)

        # Si no hay llamadas a herramientas, retornar respuesta final
        if not response.tool_calls:
            return response.content

        # Procesar cada llamada a herramienta solicitada por el modelo
        for tool_call in response.tool_calls:
            name = tool_call["name"]          # Nombre de la herramienta
            args = tool_call["args"]          # Argumentos para la herramienta
            call_id = tool_call.get("id", "") # ID único de la llamada

            # Logging de la llamada a herramienta
            log_panel(
                title="Tool Call",
                content={"tool": name, "args": args, "iteration": n_iterations},
                border_style=magenta_border_style,
            )

            # Validar que la herramienta existe
            tool = tools_by_name.get(name)
            if not tool:
                error_msg = f"Herramienta '{name}' no encontrada."
                log_panel(
                    title="Tool Error",
                    content={"tool": name, "error": error_msg, "args": args},
                    border_style="bold red",
                )
                raise ValueError(error_msg)

            # Ejecutar herramienta con manejo de errores
            try:
                # Invocar herramienta de forma asíncrona
                tool_result = await tool.ainvoke(args)

                # Logging de resultado exitoso
                log_panel(
                    title="Tool Result",
                    content={"tool": name, "result": tool_result, "status": "success"},
                    border_style=yellow_border_style,
                )
            except Exception as e:
                # Capturar y registrar errores de herramientas
                error_msg = str(e)
                log_panel(
                    title="Tool Error",
                    content={"tool": name, "error": error_msg, "args": args, "status": "error"},
                    border_style="bold red",
                )
                tool_result = f"Error: {error_msg}"

            # Agregar resultado de herramienta al historial de mensajes
            messages.append(ToolMessage(content=str(tool_result), tool_call_id=call_id))

        n_iterations += 1

    # Si se alcanza el máximo de iteraciones sin respuesta final
    raise RuntimeError(
        "Maximum number of iterations reached. Please try again with a different query"
    )

def create_history() -> list[BaseMessage]:
    """
    Inicializa un historial vacío de mensajes.

    Anteriormente inicializaba el historial con el prompt del sistema,
    pero ahora el prompt se inyecta dinámicamente en cada llamada a `ask()`
    para asegurar que siempre esté actualizado.

    Returns:
        list[BaseMessage]: Lista vacía que será poblada durante la conversación
    """
    return []  # El prompt del sistema se inyecta dinámicamente en `ask()`