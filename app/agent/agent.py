# app/agent/agent.py
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool

from app.agent.prompt_builder import build_system_prompt
from app.core.config import Config
from app.agent.logging_local import blue_border_style, green_border_style, yellow_border_style, magenta_border_style, log_panel


SYSTEM_PROMPT = """
Eres un asistente profesional de consultas en ORACLE para la base de datos.
Dispones de estas herramientas:
- list_db_tables() -> lista tablas
- describe_db_tables(table_name) -> describe tablas
- execute_query(query: str) -> ejecuta consulta SELECT
Nunca ejecutes consultas si no estás seguro de que las tablas existen.
Responde en Markdown: explica consulta y muestra los resultados en tablas siempre que sea posible.
""".strip()


def create_history() -> list[BaseMessage]:
    system_content = build_system_prompt()
    return [SystemMessage(content=system_content)]

async def ask(
    query: str,
    history: list[BaseMessage],
    llm: BaseChatModel,
    available_tools: list[BaseTool],
    max_iteration: int = Config.Agent.MAX_ITERATIONS,
) -> str:
    log_panel(title="User Request", content=query, border_style=green_border_style)

    n_iterations = 0
    messages = history.copy()
    messages.append(HumanMessage(content=query))

    tools_by_name = {tool.name: tool for tool in available_tools}

    while n_iterations < max_iteration:
        response = await llm.ainvoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return response.content

        for tool_call in response.tool_calls:
            # Log de la llamada a la herramienta
            log_panel(
                title="Tool Call",
                content={
                    "tool": tool_call["name"],
                    "args": tool_call["args"],
                    "iteration": n_iterations
                },
                border_style=magenta_border_style,
            )

            tool = tools_by_name.get(tool_call["name"])

            if not tool:
                error_msg = f"Herramienta '{tool_call['name']}' no encontrada."
                log_panel(
                    title="Tool Error",
                    content={
                        "tool": tool_call["name"],
                        "error": error_msg,
                        "args": tool_call["args"]
                    },
                    border_style="bold red",
                )
                raise ValueError(error_msg)

            try:
                # Ejecutar la herramienta
                tool_result = await tool.ainvoke(tool_call["args"])
                
                # Log del resultado exitoso
                log_panel(
                    title="Tool Result",
                    content={
                        "tool": tool_call["name"],
                        "result": tool_result,
                        "status": "success"
                    },
                    border_style=yellow_border_style,
                )
                
            except Exception as e:
                error_msg = str(e)
                # Log del error
                log_panel(
                    title="Tool Error",
                    content={
                        "tool": tool_call["name"],
                        "error": error_msg,
                        "args": tool_call["args"],
                        "status": "error"
                    },
                    border_style="bold red",
                )
                tool_result = f"Error: {error_msg}"

            messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call['id']))

        n_iterations += 1

    raise RuntimeError(
        "Maximum number of iterations reached. Please try again with a different query"
    )