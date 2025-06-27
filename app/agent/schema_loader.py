# app/agent/schema_loader.py

from app.db.db import list_tables, describe_table

def load_db_schema() -> dict[str, dict]:
    """
    Devuelve un diccionario con la descripción de cada tabla:
    {
      "tabla1": {"columns":[{"name":..., "type":..., "nullable":...},…], "pk":[…]},
      …
    }
    """
    schema: dict[str, dict] = {}
    for table in list_tables():
        schema[table] = describe_table(table)
    return schema
