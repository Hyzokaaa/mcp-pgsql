import asyncio
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

from client_config import connect_to_server
from app.mcp_tools.tools import load_tools

class ToolCallSchema(BaseModel):
    name: str = Field(..., description="Nombre de la herramienta a invocar")
    arguments: dict = Field(..., description="Argumentos de la herramienta")

async def test():
    # 1) Creamos el LLM base
    base_llm = ChatOllama(
        model="cogito:8b",   # usa exactamente el nombre de `ollama list`
        temperature=0.0,
        verbose=True,
    )

    # 2) Conectamos a MCP y cargamos las tools
    async with connect_to_server() as session:
        tools = await load_tools(session)

        # 3) Bind de tools sobre el LLM base
        llm_with_tools = base_llm.bind_tools(tools)

        # 4) Ahora sí aplicamos el esquema de salida estructurada
        llm_structured = llm_with_tools.with_structured_output(
            ToolCallSchema,
            method="function_calling",
            include_raw=True,
        )

        # 5) Invocamos al LLM estructurado
        response = await llm_structured.ainvoke(
            [HumanMessage(content="Muéstrame la tabla car")]
        )

        # 6) Interpretamos la respuesta
        if isinstance(response, ToolCallSchema):
            print("✅ Tool call detectada:")
            print("  name      =", response.name)
            print("  arguments =", response.arguments)
        else:
            print("❌ El LLM respondió texto plano:", response)

asyncio.run(test())
