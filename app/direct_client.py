# direct_client.py
import asyncio

from app.agent.agent import ask, create_history
from app.agent.models import create_llm
from app.agent.tools import load_tools
from app.core.config import Config


async def main():
    # 1. Historial y LLM
    history = create_history()
    llm = create_llm(Config.MODEL)

    # 2. Herramientas in-process
    tools = load_tools()
    llm_with_tools = llm.bind_tools(tools)

    # 3. Prueba: listar tablas
    pregunta = "Genera la consulta select * from car y dime que puedes concluir con los resultados"
    respuesta = await ask(pregunta, history, llm_with_tools, tools)
    print("\n=== RESPUESTA ===\n")
    print(respuesta)


if __name__ == "__main__":
    asyncio.run(main())
