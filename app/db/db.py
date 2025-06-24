# db.py
from sqlalchemy import create_engine, text, inspect
from app.core.config import Config

engine = create_engine(Config.DATABASE_URL, future=True)
inspector = inspect(engine)

def list_tables() -> list[str]:
    return inspector.get_table_names()

def describe_table(table: str) -> dict:
    return {
        "columns": [
            {"name": c["name"], "type": str(c["type"]), "nullable": c["nullable"]}
            for c in inspector.get_columns(table)
        ],
        "pk": inspector.get_pk_constraint(table).get("constrained_columns", []),
    }

def run_query(sql: str) -> list[dict]:
    """
    Ejecuta la consulta SQL y devuelve siempre una lista de diccionarios,
    usando result.mappings() para que cada fila sea un mapping limpio.
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        # Aquí obligamos a SQLAlchemy a darnos cada fila como RowMapping
        filas_map = result.mappings().all()
        return [dict(row) for row in filas_map]
