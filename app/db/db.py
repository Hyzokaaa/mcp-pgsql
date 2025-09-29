# app/db/db.py
"""
Módulo de acceso a base de datos para el agente SQL.

Este módulo maneja todas las operaciones de base de datos que el agente necesita
para analizar y consultar la base de datos objetivo. Proporciona una abstracción
sobre SQLAlchemy que permite trabajar con diferentes tipos de bases de datos
(PostgreSQL, Oracle) de manera uniforme.

Funcionalidades principales:
- Conexión segura a la base de datos objetivo
- Validación de configuración de backend
- Operaciones de introspección (listar tablas, describir esquemas)
- Ejecución segura de consultas con validación
- Muestreo de datos compatible con diferentes motores
- Manejo robusto de errores

Características de seguridad:
- Validación estricta de consultas (solo SELECT)
- Configuración validada al inicio
- Uso de SQLAlchemy text() para prevenir inyección SQL
- Conexiones manejadas con context managers
"""

from sqlalchemy import create_engine, text, inspect
from app.core.config import Config, DbBackend
from app.db.validators import validate_select_only, InvalidQueryError

# === VALIDACIÓN DE CONFIGURACIÓN DE BASE DE DATOS ===

# Validar que la URL de base de datos coincida con el backend configurado
if Config.TARGET_DB_BACKEND == DbBackend.ORACLE:
    if "oracle" not in Config.TARGET_DATABASE_URL.lower():
        raise ValueError("TARGET_DATABASE_URL debe contener 'oracle' cuando TARGET_DB_BACKEND=oracle")
elif Config.TARGET_DB_BACKEND == DbBackend.POSTGRES:
    if "postgresql" not in Config.TARGET_DATABASE_URL.lower():
        raise ValueError("TARGET_DATABASE_URL debe contener 'postgresql' cuando TARGET_DB_BACKEND=postgres")

# === CONFIGURACIÓN DE SQLALCHEMY ===

# Engine para la base de datos objetivo (la que analiza el agente)
# Utiliza future=True para API moderna de SQLAlchemy
target_engine = create_engine(Config.TARGET_DATABASE_URL, future=True)

# Inspector para operaciones de metadatos e introspección
target_inspector = inspect(target_engine)

# === FUNCIONES DE OPERACIONES DE BASE DE DATOS ===

def list_tables() -> list[str]:
    """
    Lista todas las tablas de usuario en la base de datos objetivo.

    Utiliza el inspector de SQLAlchemy para obtener metadatos de la base de datos
    y retorna solo las tablas creadas por el usuario (excluye tablas del sistema).

    Returns:
        list[str]: Lista de nombres de tablas disponibles

    Raises:
        Exception: Si hay problemas de conexión o permisos insuficientes
    """
    return target_inspector.get_table_names()

def describe_table(table: str) -> dict:
    """
    Describe la estructura completa de una tabla específica.

    Obtiene información detallada sobre columnas, tipos de datos, restricciones
    y claves primarias de la tabla especificada. Esencial para que el agente
    entienda cómo estructurar consultas SQL correctamente.

    Args:
        table: Nombre de la tabla a describir

    Returns:
        dict: Diccionario con información del esquema conteniendo:
            - columns: Lista de columnas con nombre, tipo y nullabilidad
            - pk: Lista de columnas que forman la clave primaria

    Example:
        {
            "columns": [
                {"name": "id", "type": "INTEGER", "nullable": False},
                {"name": "name", "type": "VARCHAR(50)", "nullable": True}
            ],
            "pk": ["id"]
        }

    Raises:
        Exception: Si la tabla no existe o hay problemas de acceso
    """
    return {
        "columns": [
            {"name": c["name"], "type": str(c["type"]), "nullable": c["nullable"]}
            for c in target_inspector.get_columns(table)
        ],
        "pk": target_inspector.get_pk_constraint(table).get("constrained_columns", []),
    }

def run_query(sql: str) -> list[dict]:
    """
    Ejecuta una consulta SQL en la base de datos objetivo con validación de seguridad.

    Esta función es el punto central para ejecutar consultas SQL. Incluye validación
    estricta que solo permite consultas SELECT para garantizar que el agente solo
    pueda leer datos, nunca modificarlos.

    Args:
        sql: Consulta SQL a ejecutar (debe ser una declaración SELECT)

    Returns:
        list[dict]: Lista de filas como diccionarios con nombres de columna como claves

    Raises:
        ValueError: Si la consulta no es válida (no es SELECT) o tiene sintaxis incorrecta
        Exception: Si hay errores de conexión o ejecución en la base de datos

    Example:
        >>> run_query("SELECT id, name FROM users LIMIT 5")
        [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]
    """
    try:
        # Validar que la consulta sea solo SELECT antes de ejecutar
        validate_select_only(sql)
    except InvalidQueryError as e:
        raise ValueError(f"Consulta inválida: {e}")

    # Ejecutar consulta con context manager para manejo seguro de conexiones
    with target_engine.connect() as conn:
        result = conn.execute(text(sql))
        filas_map = result.mappings().all()
        return [dict(row) for row in filas_map]

def sample_table(table_name: str, row_sample_size: int = 10) -> list[dict]:
    """
    Obtiene una muestra de filas de una tabla, compatible con diferentes motores de base de datos.

    Esta función construye consultas SQL optimizadas según el backend de base de datos
    para obtener muestras representativas de datos. Útil para exploración inicial
    sin sobrecargar las respuestas con demasiados datos.

    Args:
        table_name: Nombre de la tabla a muestrear
        row_sample_size: Número de filas a retornar (default: 10)

    Returns:
        list[dict]: Lista de filas muestreadas como diccionarios

    Raises:
        ValueError: Si el backend de base de datos no es soportado
        Exception: Si hay errores en la ejecución de la consulta

    Example:
        >>> sample_table("users", 3)
        [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}, {"id": 3, "name": "Bob"}]

    Note:
        Las consultas generadas son específicas del motor:
        - Oracle: Usa ROWNUM para compatibilidad con versiones antiguas
        - PostgreSQL: Usa LIMIT nativo para mejor rendimiento
    """
    if Config.TARGET_DB_BACKEND == DbBackend.ORACLE:
        # Consulta compatible con todas las versiones de Oracle usando ROWNUM
        # Se utiliza una subconsulta con ORDER BY para resultados determinísticos
        query = f"""
        SELECT * FROM (
            SELECT * FROM {table_name} ORDER BY 1
        ) WHERE ROWNUM <= {row_sample_size}
        """
    elif Config.TARGET_DB_BACKEND == DbBackend.POSTGRES:
        # PostgreSQL usa LIMIT directamente, más eficiente
        query = f"SELECT * FROM {table_name} LIMIT {row_sample_size}"
    else:
        raise ValueError(f"Backend no soportado: {Config.TARGET_DB_BACKEND}")

    # Ejecutar la consulta usando la función validada run_query
    return run_query(query)

def get_target_engine():
    """
    Retorna la instancia del engine de SQLAlchemy para la base de datos objetivo.

    Proporciona acceso directo al engine para casos de uso avanzados que requieren
    control de bajo nivel sobre las conexiones o transacciones.

    Returns:
        Engine: Instancia de SQLAlchemy Engine configurada para la base de datos objetivo

    Note:
        Generalmente no debería ser necesario usar esta función directamente.
        Las funciones de alto nivel (run_query, list_tables, etc.) son preferibles.
    """
    return target_engine
