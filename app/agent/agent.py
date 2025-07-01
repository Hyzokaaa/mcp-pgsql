# app/agent/agent.py

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
    # Evitar duplicar SystemMessage si ya existe en history
    if not history or not isinstance(history[0], SystemMessage):
        system_prompt = build_system_prompt()
        messages = [SystemMessage(content=system_prompt)] + history
    else:
        messages = history.copy()

    log_panel(title="User Request", content=query, border_style=green_border_style)
    messages.append(HumanMessage(content=query))

    tools_by_name = {tool.name: tool for tool in available_tools}
    n_iterations = 0

    while n_iterations < max_iteration:
        response = await llm.ainvoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return response.content

        for tool_call in response.tool_calls:
            name = tool_call["name"]
            args = tool_call["args"]
            call_id = tool_call.get("id", "")

            log_panel(
                title="Tool Call",
                content={"tool": name, "args": args, "iteration": n_iterations},
                border_style=magenta_border_style,
            )

            tool = tools_by_name.get(name)
            if not tool:
                error_msg = f"Herramienta '{name}' no encontrada."
                log_panel(
                    title="Tool Error",
                    content={"tool": name, "error": error_msg, "args": args},
                    border_style="bold red",
                )
                raise ValueError(error_msg)
            try:
                tool_result = await tool.ainvoke(args)
                log_panel(
                    title="Tool Result",
                    content={"tool": name, "result": tool_result, "status": "success"},
                    border_style=yellow_border_style,
                )
            except Exception as e:
                error_msg = str(e)
                log_panel(
                    title="Tool Error",
                    content={"tool": name, "error": error_msg, "args": args, "status": "error"},
                    border_style="bold red",
                )
                tool_result = f"Error: {error_msg}"

            messages.append(ToolMessage(content=str(tool_result), tool_call_id=call_id))

        n_iterations += 1

    raise RuntimeError(
        "Maximum number of iterations reached. Please try again with a different query"
    )

def create_history() -> list[BaseMessage]:
    """Inicializa el historial con el SYSTEM_PROMPT dinámico."""
    return []  # Ahora el prompt se inyecta dentro de `ask` en cada llamada