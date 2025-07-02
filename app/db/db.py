# app/db/db.py

from sqlalchemy import create_engine, text, inspect
from app.core.config import Config, DbBackend
from app.db.validators import validate_select_only, InvalidQueryError

# Validación de backend de base de datos TARGET
if Config.TARGET_DB_BACKEND == DbBackend.ORACLE:
    if "oracle" not in Config.TARGET_DATABASE_URL.lower():
        raise ValueError("TARGET_DATABASE_URL debe contener 'oracle' cuando TARGET_DB_BACKEND=oracle")
elif Config.TARGET_DB_BACKEND == DbBackend.POSTGRES:
    if "postgresql" not in Config.TARGET_DATABASE_URL.lower():
        raise ValueError("TARGET_DATABASE_URL debe contener 'postgresql' cuando TARGET_DB_BACKEND=postgres")

# Engine para la base de datos TARGET (la que analiza el agente)
target_engine = create_engine(Config.TARGET_DATABASE_URL, future=True)
target_inspector = inspect(target_engine)


# Funciones para la base de datos TARGET (usadas por el agente)
def list_tables() -> list[str]:
    """Lista tablas de la base de datos TARGET"""
    return target_inspector.get_table_names()

def describe_table(table: str) -> dict:
    """Describe tabla de la base de datos TARGET"""
    return {
        "columns": [
            {"name": c["name"], "type": str(c["type"]), "nullable": c["nullable"]}
            for c in target_inspector.get_columns(table)
        ],
        "pk": target_inspector.get_pk_constraint(table).get("constrained_columns", []),
    }

def run_query(sql: str) -> list[dict]:
    """
    Ejecuta consulta en la base de datos TARGET
    """
    try:
        validate_select_only(sql)
    except InvalidQueryError as e:
        raise ValueError(f"Consulta inválida: {e}")
    with target_engine.connect() as conn:
        result = conn.execute(text(sql))
        filas_map = result.mappings().all()
        return [dict(row) for row in filas_map]

def get_target_engine():
    """Retorna engine de la base de datos TARGET"""
    return target_engine
