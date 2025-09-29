# app/db/validators.py
"""
Validadores de seguridad para consultas SQL.

Este módulo implementa validaciones estrictas de seguridad para garantizar que
el agente SQL solo pueda ejecutar consultas de lectura seguras. Utiliza el
parser SQLparse para analizar la sintaxis SQL y detectar patrones potencialmente
peligrosos.

Características de seguridad implementadas:
- Solo permite consultas SELECT (lectura únicamente)
- Bloquea operaciones de modificación (INSERT, UPDATE, DELETE)
- Previene operaciones de esquema (DROP, ALTER, TRUNCATE)
- Bloquea operaciones de permisos (GRANT, REVOKE)
- Prohíbe comentarios SQL que podrían ocultar código malicioso
- Valida que solo se ejecute un statement por consulta

Esta capa de seguridad es fundamental para prevenir que el agente pueda
modificar datos o esquemas de la base de datos, manteniendo un entorno
de solo lectura seguro.
"""

import sqlparse
from sqlparse.tokens import Keyword, DML

class InvalidQueryError(Exception):
    """
    Excepción lanzada cuando una consulta SQL no pasa las validaciones de seguridad.

    Esta excepción se utiliza para indicar que una consulta SQL contiene
    elementos no permitidos por las políticas de seguridad del agente,
    como operaciones de escritura, comentarios, o múltiples statements.
    """
    pass

def validate_select_only(sql: str) -> None:
    """
    Valida que una consulta SQL sea segura para ejecución por el agente.

    Realiza múltiples verificaciones de seguridad para garantizar que la consulta:
    1. No contenga comentarios que podrían ocultar código malicioso
    2. Sea un único statement SQL (no consultas múltiples)
    3. Comience con SELECT (solo operaciones de lectura)
    4. No contenga palabras clave peligrosas para modificación de datos

    Args:
        sql: La consulta SQL a validar

    Raises:
        InvalidQueryError: Si la consulta no pasa alguna validación de seguridad

    Example:
        >>> validate_select_only("SELECT * FROM users")  # ✓ Válida
        >>> validate_select_only("DELETE FROM users")   # ✗ InvalidQueryError

    Security Checks:
        - Comentarios: Prohíbe -- y /* */ para prevenir inyección
        - Statements: Solo permite un único statement por consulta
        - Comando: Debe comenzar con SELECT
        - Keywords: Bloquea INSERT, UPDATE, DELETE, DROP, ALTER, etc.
    """
    # 1) Validación de comentarios
    # Los comentarios pueden ser usados para ocultar código malicioso
    # o para evadir otras validaciones, por lo que se prohíben completamente
    if "--" in sql or "/*" in sql or "*/" in sql:
        raise InvalidQueryError("Los comentarios no están permitidos.")

    # 2) Parsear SQL y validar número de statements
    # Solo se permite un único statement para prevenir inyección de múltiples comandos
    parsed = sqlparse.parse(sql)
    if len(parsed) != 1:
        raise InvalidQueryError("Sólo se permite un único statement SQL.")

    stmt = parsed[0]

    # 3) Validar que el primer comando sea SELECT
    # Buscar el primer token que no sea whitespace para identificar el comando
    first_token = next((t for t in stmt.tokens if not t.is_whitespace), None)

    # Verificar que el token existe, es un comando DML y específicamente SELECT
    if not first_token or first_token.ttype is not DML or first_token.value.lower() != "select":
        raise InvalidQueryError("La consulta debe empezar con SELECT.")

    # 4) Buscar y bloquear keywords peligrosas
    # Define lista de palabras clave que permiten modificar datos o esquemas
    forbidden = {
        # Operaciones de modificación de datos
        "delete", "update", "insert",
        # Operaciones de esquema
        "drop", "alter", "truncate",
        # Operaciones de permisos
        "grant", "revoke"
    }

    # Revisar todos los tokens del statement en busca de keywords prohibidas
    for token in stmt.tokens:
        if token.ttype is Keyword and token.value.lower() in forbidden:
            raise InvalidQueryError(f"Keyword no permitida: {token.value}")
