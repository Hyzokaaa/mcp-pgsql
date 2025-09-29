# app/agent/tools.py
"""
Herramientas SQL para el agente conversacional.

Este módulo define todas las herramientas (tools) que el agente puede usar para
interactuar con la base de datos. Cada herramienta está implementada como una
función decorada con @tool de LangChain, lo que permite al modelo de lenguaje
llamarlas de manera estructurada.

Herramientas disponibles:
- list_db_tables: Lista todas las tablas de usuario en la base de datos
- describe_db_table: Describe la estructura de una tabla específica
- execute_query: Ejecuta consultas SELECT y devuelve resultados
- sample_table: Obtiene una muestra de datos de una tabla

Características de seguridad:
- Validación de entrada para prevenir inyección SQL
- Solo permite consultas SELECT para lectura segura
- Logging detallado de todas las operaciones
- Manejo robusto de errores con mensajes informativos
"""

from typing import Any, List
from langchain_core.tools import tool, ToolException, BaseTool
from app.db.db import list_tables, describe_table, run_query, sample_table as db_sample_table
from app.agent.logging_local import log_panel

@tool(parse_docstring=True)
def list_db_tables(reasoning: str) -> str:
    """
    Lista todas las tablas creadas por el usuario en la base de datos (excluye tablas del sistema).

    Esta herramienta permite al agente obtener una visión general de la estructura
    de la base de datos, identificando qué tablas están disponibles para consultar.
    Filtra automáticamente las tablas del sistema para mostrar solo contenido relevante.

    Args:
        reasoning: Explicación detallada de por qué necesitas ver todas las tablas
                  (debe relacionarse con la consulta del usuario)

    Returns:
        str: JSON string con la lista de tablas, estado y conteo total

    Example:
        {"status": "success", "tables": ["users", "orders", "products"], "count": 3}
    """
    log_panel(
        title="List Tables Tool",
        content=f"Reasoning: {reasoning}",
        border_style="bold blue"
    )

    try:
        # Obtener lista de tablas desde la capa de base de datos
        tables = list_tables()
        result = {
            "status": "success",
            "tables": tables,
            "count": len(tables)
        }
        return str(result)
    except Exception as e:
        error_msg = f"Error listing tables: {str(e)}"
        log_panel(title="Tool Error", content=error_msg, border_style="bold red")
        return f"Error listing tables: {str(e)}"

@tool(parse_docstring=True)
def describe_db_table(table_name: str, reasoning: str) -> str:
    """
    Describe la estructura de una tabla de base de datos (columnas, tipos y claves primarias).

    Esta herramienta proporciona información detallada sobre el esquema de una tabla,
    incluyendo nombres de columnas, tipos de datos, restricciones y relaciones.
    Es esencial para entender cómo estructurar consultas SQL correctamente.

    Args:
        table_name: Nombre de la tabla a describir (sensible a mayúsculas/minúsculas)
        reasoning: Explicación detallada de por qué necesitas la estructura de esta tabla

    Returns:
        str: JSON string con esquema completo de la tabla

    Example:
        {"status": "success", "table": "users", "schema": {...}, "columns_count": 5}
    """
    log_panel(
        title="Describe Table Tool",
        content=f"Table: {table_name}, Reasoning: {reasoning}",
        border_style="bold cyan"
    )

    try:
        # Obtener esquema de la tabla desde la capa de base de datos
        schema = describe_table(table_name)
        result = {
            "status": "success",
            "table": table_name,
            "schema": schema,
            "columns_count": len(schema["columns"])
        }
        return str(result)
    except Exception as e:
        error_msg = f"Error describing table {table_name}: {str(e)}"
        log_panel(title="Tool Error", content=error_msg, border_style="bold red")
        return error_msg

@tool(parse_docstring=True)
def execute_query(query: str, reasoning: str) -> str:
    """
    Ejecuta una consulta SELECT y devuelve los resultados en formato JSON.

    Esta herramienta es el corazón de la funcionalidad del agente SQL. Permite
    ejecutar consultas de lectura de manera segura, con validación automática
    para prevenir operaciones destructivas. Solo acepta consultas SELECT.

    Características de seguridad:
    - Sanitización automática de entrada
    - Solo permite consultas SELECT (lectura)
    - Validación contra inyección SQL
    - Logging detallado de operaciones

    Args:
        query: La consulta SQL SELECT a ejecutar (solo declaraciones SELECT permitidas)
        reasoning: Explicación detallada de qué esperas encontrar y por qué necesitas esta consulta

    Returns:
        str: JSON string con resultados de la consulta

    Raises:
        ToolException: Si la consulta no es válida o no es una declaración SELECT

    Example:
        {"rows": [{"id": 1, "name": "John"}], "count": 1}
    """
    # Sanitizar entrada eliminando espacios y punto y coma final
    sanitized = query.strip().rstrip(';').strip()
    log_panel(
        title="Execute Query Tool (sanitized)",
        content=f"Original: {query!r}\nSanitized: {sanitized!r}\nReasoning: {reasoning}",
        border_style="bold yellow"
    )
    query = sanitized

    try:
        # Ejecutar consulta a través de la capa de base de datos
        rows = run_query(query)
        if not rows:
            result = {"rows": [], "message": "Query executed successfully, no rows returned."}
        else:
            result = {"rows": rows, "count": len(rows)}
        return str(result)
    except ValueError as ve:
        # Error de validación (ej: consulta que no es SELECT)
        error_msg = f"Query validation error: {str(ve)}"
        log_panel(title="Tool Error", content=error_msg, border_style="bold red")
        raise ToolException(error_msg)
    except Exception as e:
        # Error general de ejecución
        error_msg = f"Error executing query: {str(e)}"
        log_panel(title="Tool Error", content=error_msg, border_style="bold red")
        raise ToolException(error_msg)

@tool(parse_docstring=True)
def sample_table(reasoning: str, table_name: str, row_sample_size: int) -> str:
    """
    Obtiene una muestra pequeña de filas para entender la estructura y contenido de una tabla específica.

    Esta herramienta es útil para explorar datos reales sin sobrecargar la respuesta
    con demasiada información. Permite al agente entender el tipo de datos almacenados,
    formatos, y patrones antes de construir consultas más complejas.

    Args:
        reasoning: Explicación detallada de por qué necesitas ver datos de muestra de esta tabla
        table_name: Nombre exacto de la tabla a muestrear (sensible a mayúsculas, sin comillas)
        row_sample_size: Número de filas a obtener (recomendado: 3-5 filas para legibilidad)

    Returns:
        str: JSON string con muestra de datos de la tabla

    Raises:
        ToolException: Si hay errores de validación o ejecución

    Example:
        {"rows": [...], "count": 3, "table": "users"}
    """
    log_panel(
        title="Sample Table Tool",
        content=f"Table: {table_name}\nRows: {row_sample_size}\nReasoning: {reasoning}",
        border_style="bold magenta"
    )

    try:
        # Obtener muestra de datos desde la capa de base de datos
        rows = db_sample_table(table_name, row_sample_size)

        if not rows:
            result = {"rows": [], "message": f"Table {table_name} exists but contains no data."}
        else:
            result = {"rows": rows, "count": len(rows), "table": table_name}

        return str(result)
    except ValueError as ve:
        # Error de validación desde run_query
        error_msg = f"Query validation error: {str(ve)}"
        log_panel(title="Tool Error", content=error_msg, border_style="bold red")
        raise ToolException(error_msg)
    except Exception as e:
        # Error general de muestreo
        error_msg = f"Error sampling table {table_name}: {str(e)}"
        log_panel(title="Tool Error", content=error_msg, border_style="bold red")
        raise ToolException(error_msg)

def get_available_tools() -> List[BaseTool]:
    """
    Devuelve una lista de todas las herramientas de base de datos disponibles.

    Returns:
        List[BaseTool]: Lista de herramientas configuradas para el agente
    """
    return [list_db_tables, describe_db_table, execute_query, sample_table]

def load_tools() -> List[BaseTool]:
    """
    Carga y devuelve todas las herramientas disponibles para el agente.

    Esta función sirve como punto de entrada principal para obtener las herramientas
    que serán asociadas al modelo de lenguaje. Actualmente es un alias de
    get_available_tools() pero permite extensibilidad futura.

    Returns:
        List[BaseTool]: Lista completa de herramientas cargadas y listas para usar
    """
    return get_available_tools()