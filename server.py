# server.py
import json
import logging

from mcp.server.fastmcp import FastMCP
from config import Config
from db import list_tables, describe_table, run_query
from mcp.types import TextContent

# Configuramos el logger para que muestre mensajes de nivel ERROR (y superiores)
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="SEPSA IA",
    host=Config.Server.HOST,
    port=Config.Server.PORT,
    sse_path=Config.Server.SSE_PATH,
)

@mcp.tool()
def list_db_tables() -> str:
    """Lista todas las tablas de la base de datos, en JSON."""
    tables = list_tables()
    return json.dumps({"tables": tables}, indent=2)

@mcp.tool()
def describe_db_table(table_name: str) -> str:
    """Describe la estructura de la tabla indicada (columnas y PK), en JSON."""
    schema = describe_table(table_name)
    return json.dumps(
        {"table": table_name, "schema": schema},
        default=str,
        indent=2,
    )

@mcp.tool()
def execute_query(query: str) -> str:
    """
    Ejecuta un SELECT en la base de datos.
    Solo permitimos sentencias que empiecen con 'select'.
    Devuelve un string con el JSON de las filas.
    """
    if not query.strip().lower().startswith("select"):
        # En caso de que no sea SELECT, imprimimos en consola y devolvemos JSON de error
        mensaje_err = "Sólo se permiten consultas SELECT."
        logger.error(f"Intento inválido en execute_query: {mensaje_err} – Query recibida: '{query}'")
        return json.dumps({"error": mensaje_err}, ensure_ascii=False)

    try:
        rows = run_query(query)  # Esto retorna list[dict]

        # Si no devolvió filas, devolvemos un JSON con mensaje
        if not rows:
            return json.dumps(
                {"rows": [], "message": "La consulta se ejecutó correctamente, pero no devolvió filas."},
                ensure_ascii=False,
                indent=2,
            )

        # Serializamos el resultado a JSON con indentado
        return json.dumps(
            {"rows": rows},
            default=str,       # por si hubiera tipos no serializables
            indent=2,
            ensure_ascii=False,
        )

    except Exception as e:
        # Logueamos la excepción completa (incluyendo traceback) en consola
        logger.exception(f"Error ejecutando execute_query con query: '{query}'")

        # Además devolvemos un JSON con el mensaje de error
        return json.dumps(
            {"error": f"Error ejecutando execute_query: {str(e)}"},
            ensure_ascii=False,
        )

if __name__ == "__main__":
    mcp.run(transport=Config.Server.TRANSPORT)
