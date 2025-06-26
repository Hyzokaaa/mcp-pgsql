# app/mcp_tools/tools.py
from typing import Any
from langchain_core.tools import StructuredTool, ToolException
from app.db.db import list_tables, describe_table, run_query

async def _wrap_list_tables() -> Any:
    try:
        tables = list_tables()
        return {"tables": tables}
    except Exception as e:
        raise ToolException(f"Error en list_db_tables: {e}")

async def _wrap_describe_table(table_name: str) -> Any:
    try:
        schema = describe_table(table_name)
        return {"table": table_name, "schema": schema}
    except Exception as e:
        raise ToolException(f"Error en describe_db_table: {e}")

async def _wrap_execute_query(query: str) -> Any:
    q = query.strip().lower()
    if not q.startswith("select"):
        raise ToolException("Sólo se permiten consultas SELECT.")
    try:
        rows = run_query(query)
        if not rows:
            return {"rows": [], "message": "Consulta OK, sin filas."}
        return {"rows": rows}
    except Exception as e:
        raise ToolException(f"Error en execute_query: {e}")

def load_tools() -> list[StructuredTool]:
    return [
        StructuredTool(
            name="list_db_tables",
            description="Lista todas las tablas de la base de datos",
            args_schema={},  # no necesita args
            coroutine=_wrap_list_tables,
        ),
        StructuredTool(
            name="describe_db_table",
            description="Describe la estructura de una tabla (columnas y PK)",
            args_schema={"table_name": str},
            coroutine=_wrap_describe_table,
        ),
        StructuredTool(
            name="execute_query",
            description="Ejecuta una consulta SELECT y devuelve los resultados en JSON",
            args_schema={"query": str},
            coroutine=_wrap_execute_query,
        ),
    ]
