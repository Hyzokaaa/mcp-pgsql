# app/agent/prompt_builder.py

from app.agent.schema_loader import load_db_schema

def build_system_prompt() -> str:
    schema = load_db_schema()
    lines = [
        "Eres un asistente profesional de SQL. El esquema actual de la base de datos es:"
    ]
    for table, info in schema.items():
        cols = ", ".join(col["name"] for col in info["columns"])
        lines.append(f"  • {table}({cols})")
    lines.append("")  # línea en blanco
    lines.append("Dispones de estas herramientas:")
    lines.append("- list_db_tables()")
    lines.append("- describe_db_table(table_name)")
    lines.append("- execute_query(query: str)")
    lines.append(
        "Nunca ejecutes consultas si no estás seguro de que las tablas existen. "
        "Responde en Markdown: explica la consulta y muestra los resultados en tablas."
    )
    return "\n".join(lines)
