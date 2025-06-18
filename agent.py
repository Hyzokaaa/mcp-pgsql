from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import BaseTool

from config import Config
from logging_local import blue_border_style, green_border_style, log_panel
from tools import call_tool


SYSTEM_PROMPT = """
Eres un asistente profesional de consultas SQL para la base de datos rentacar.
Dispones de estas herramientas:
- list_db_tables() -> lista tablas
- execute_sql(query: str) -> ejecuta consulta SELECT
Responde en Markdown: explica consulta y muestra los resultados en tablas siempre que sea posible.
""".strip()


def create_history() -> list[BaseMessage]:
    return [SystemMessage(content=SYSTEM_PROMPT)]

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

    while n_iterations < max_iteration:
        # 1) Llamada al LLM
        response = await llm.ainvoke(messages)
        messages.append(response)

        # 2) Si no hay llamadas a tool, devolvemos la respuesta final
        if not response.tool_calls:
            return response.content

        # 3) Procesar cada tool_call
        for tool_call in response.tool_calls:
            log_panel(
                title=str(tool_call),
                content=str(tool_call),
                border_style=blue_border_style,
            )
            tool_response = await call_tool(tool_call, available_tools)
            messages.append(tool_response)

        # 4) Incrementar contador
        n_iterations += 1

    # Si agotamos iteraciones, lanzamos el error con typo corregido
    raise RuntimeError(
        "Maximum number of iterations reached. Please try again with a different query"
    )
