# app/db/validators.py

import sqlparse
from sqlparse.tokens import Keyword, DML

class InvalidQueryError(Exception):
    """Consulta no válida o potencialmente peligrosa."""

def validate_select_only(sql: str) -> None:
    """
    Valida que la consulta SQL:
    1. Sea sólo un único statement.
    2. Comience con SELECT.
    3. No contenga keywords peligrosas (DELETE, UPDATE, INSERT, DROP, ALTER…).
    4. No contenga comentarios (— o /* */).
    Lanza InvalidQueryError en caso contrario.
    """
    # 1) Sin comentarios
    if "--" in sql or "/*" in sql or "*/" in sql:
        raise InvalidQueryError("Los comentarios no están permitidos.")

    # 2) Parseo y conteo de statements
    parsed = sqlparse.parse(sql)
    if len(parsed) != 1:
        raise InvalidQueryError("Sólo se permite un único statement SQL.")

    stmt = parsed[0]
    # 3) El primer token DML debe ser SELECT
    first_token = next((t for t in stmt.tokens if not t.is_whitespace), None)
    if not first_token or first_token.ttype is not DML or first_token.value.lower() != "select":
        raise InvalidQueryError("La consulta debe empezar con SELECT.")

    # 4) Buscar keywords no permitidas
    forbidden = {"delete", "update", "insert", "drop", "alter", "truncate", "grant", "revoke"}
    for token in stmt.tokens:
        if token.ttype is Keyword and token.value.lower() in forbidden:
            raise InvalidQueryError(f"Keyword no permitida: {token.value}")
