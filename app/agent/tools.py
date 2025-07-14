# app/agent/tools.py

from typing import Any, List
from langchain_core.tools import tool, ToolException, BaseTool
from app.db.db import list_tables, describe_table, run_query
from app.agent.logging_local import log_panel

@tool(parse_docstring=True)
def list_db_tables(reasoning: str) -> str:
    """Lists all user-created tables in the database (excludes system tables).
    
    Args:
        reasoning: Detailed explanation of why you need to see all tables (relate to the user's query)
    """
    log_panel(
        title="List Tables Tool",
        content=f"Reasoning: {reasoning}",
        border_style="bold blue"
    )
    
    try:
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
    """Describes the structure of a database table (columns, types, and primary keys).
    
    Args:
        table_name: Name of the table to describe
        reasoning: Detailed explanation of why you need this table's structure
    """
    log_panel(
        title="Describe Table Tool",
        content=f"Table: {table_name}, Reasoning: {reasoning}",
        border_style="bold cyan"
    )
    
    try:
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
    """Executes a SELECT query and returns the results in JSON format.
    
    Args:
        query: The SQL SELECT query to execute (only SELECT statements allowed)
        reasoning: Detailed explanation of what you expect to find and why this query is needed
    """
    sanitized = query.strip().rstrip(';').strip()
    log_panel(
        title="Execute Query Tool (sanitized)",
        content=f"Original: {query!r}\nSanitized: {sanitized!r}\nReasoning: {reasoning}",
        border_style="bold yellow"
    )
    query = sanitized
    
    try:
        rows = run_query(query)
        if not rows:
            result = {"rows": [], "message": "Query executed successfully, no rows returned."}
        else:
            result = {"rows": rows, "count": len(rows)}
        return str(result)
    except ValueError as ve:
        # Validation error (e.g., non-SELECT query)
        error_msg = f"Query validation error: {str(ve)}"
        log_panel(title="Tool Error", content=error_msg, border_style="bold red")
        raise ToolException(error_msg)
    except Exception as e:
        error_msg = f"Error executing query: {str(e)}"
        log_panel(title="Tool Error", content=error_msg, border_style="bold red")
        raise ToolException(error_msg)

@tool(parse_docstring=True)
def sample_table(reasoning: str, table_name: str, row_sample_size: int) -> str:
    """Retrieves a small sample of rows to understand the data structure and content of a specific table.
    
    Args:
        reasoning: Detailed explanation of why you need to see sample data from this table
        table_name: Exact name of the table to sample (case-sensitive, no quotes needed)
        row_sample_size: Number of rows to retrieve (recommended: 3-5 rows for readability)
    """
    log_panel(
        title="Sample Table Tool",
        content=f"Table: {table_name}\nRows: {row_sample_size}\nReasoning: {reasoning}",
        border_style="bold magenta"
    )
    
    try:
        # Construct the sample query
        query = f"SELECT * FROM {table_name} LIMIT {row_sample_size}"
        rows = run_query(query)
        
        if not rows:
            result = {"rows": [], "message": f"Table {table_name} exists but contains no data."}
        else:
            result = {"rows": rows, "count": len(rows), "table": table_name}
        
        return str(result)
    except ValueError as ve:
        # Validation error from run_query
        error_msg = f"Query validation error: {str(ve)}"
        log_panel(title="Tool Error", content=error_msg, border_style="bold red")
        raise ToolException(error_msg)
    except Exception as e:
        error_msg = f"Error sampling table {table_name}: {str(e)}"
        log_panel(title="Tool Error", content=error_msg, border_style="bold red")
        raise ToolException(error_msg)

def get_available_tools() -> List[BaseTool]:
    """Returns a list of all available database tools."""
    return [list_db_tables, describe_db_table, execute_query, sample_table]

def load_tools() -> List[BaseTool]:
    """Loads and returns all available tools for the agent."""
    return get_available_tools()