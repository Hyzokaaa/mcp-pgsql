# app/direct_client.py
"""
Cliente directo para interactuar con el agente SQL sin API REST.

Este módulo proporciona una interfaz directa al agente SQL, permitiendo
ejecutar consultas desde la línea de comandos sin necesidad de levantar
el servidor web. Es útil para:

- Pruebas rápidas del agente
- Desarrollo y debugging
- Scripts automatizados
- Integración directa en otras aplicaciones Python

El cliente inicializa todos los componentes necesarios (LLM, herramientas, historial)
y ejecuta una consulta de ejemplo que demuestra las capacidades del agente.

Uso:
    python -m app.direct_client
    # o usando PDM:
    pdm run direct
"""

import asyncio

from app.agent.agent import ask, create_history
from app.agent.models import create_llm
from app.agent.tools import load_tools
from app.core.config import Config

async def main():
    """
    Función principal que demuestra el uso directo del agente SQL.

    Esta función realiza una demostración completa del agente:
    1. Inicializa el historial de conversación
    2. Crea y configura el modelo de lenguaje
    3. Carga las herramientas SQL disponibles
    4. Asocia las herramientas al modelo
    5. Ejecuta una consulta de ejemplo
    6. Muestra los resultados

    La consulta de ejemplo solicita al agente que ejecute una consulta SELECT
    y proporcione análisis sobre los resultados obtenidos.
    """
    # 1. Inicializar historial de conversación vacío
    history = create_history()

    # 2. Crear instancia del modelo de lenguaje desde configuración
    llm = create_llm(Config.MODEL)

    # 3. Cargar todas las herramientas SQL disponibles
    tools = load_tools()

    # 4. Asociar herramientas al modelo para habilitar tool calling
    llm_with_tools = llm.bind_tools(tools)

    # 5. Ejecutar consulta de demostración
    # Esta consulta muestra las capacidades completas del agente:
    # - Ejecutar consulta SQL
    # - Analizar resultados
    # - Proporcionar conclusiones contextuales
    pregunta = "Genera la consulta select * from car y dime que puedes concluir con los resultados"

    # Procesar consulta usando el agente
    respuesta = await ask(
        query=pregunta,
        history=history,
        llm=llm_with_tools,
        available_tools=tools
    )

    # 6. Mostrar resultados formateados
    print("\n=== RESPUESTA ===\n")
    print(respuesta)

if __name__ == "__main__":
    # Ejecutar cliente usando asyncio para compatibilidad con el agente asíncrono
    asyncio.run(main())
