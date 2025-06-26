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
    pregunta = "Lístame las tablas de la base de datos y muéstrame las tablas, posteriormente descríbeme la tabla 'car' y por último muéstrame todos los carros de la tabla 'car'"
    respuesta = await ask(pregunta, history, llm_with_tools, tools)
    print("\n=== RESPUESTA ===\n")
    print(respuesta)


if __name__ == "__main__":
    asyncio.run(main())
