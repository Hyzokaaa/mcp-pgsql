# app/agent/prompt_builder.py
"""
Constructor de prompts del sistema para el agente SQL.

Este módulo genera dinámicamente los prompts del sistema que guían el comportamiento
del modelo de lenguaje. Los prompts se adaptan automáticamente según el tipo de
base de datos configurada y incluyen instrucciones específicas para optimizar
la interacción con bases de datos.

Funcionalidades:
- Generación dinámica de prompts basados en configuración
- Adaptación automática a diferentes tipos de base de datos
- Inclusión de instrucciones específicas por motor (Oracle/PostgreSQL)
- Contextualización con fecha actual
- Configuración de formato de respuesta y audiencia objetivo

El prompt resultante instruye al modelo sobre:
- Estrategias de exploración de base de datos
- Validación de consultas SQL
- Uso eficiente de herramientas
- Sintaxis específica del motor de base de datos
- Formato de respuesta esperado
"""

from datetime import datetime
from app.agent.schema_loader import load_db_schema
from app.core.config import Config, DbBackend

def build_system_prompt() -> str:
    """
    Construye un prompt del sistema personalizado para el agente SQL.

    Genera un prompt dinámico que adapta las instrucciones del agente según
    el tipo de base de datos configurada. El prompt incluye:

    - Identidad del asistente (tipo de base de datos)
    - Propósito y objetivos del agente
    - Instrucciones estratégicas para exploración de BD
    - Instrucciones específicas del motor de base de datos
    - Configuración de formato y audiencia

    Returns:
        str: Prompt del sistema completo y personalizado

    Example:
        Para PostgreSQL:
        ```
        You are a professional PostgreSQL assistant.

        Your purpose is to transform natural language requests into precise,
        efficient PostgreSQL SQL queries that deliver exactly what the user needs.

        <instructions>
          <instruction>Use PostgreSQL-specific SQL syntax including functions
          like NOW(), LIMIT, COALESCE, etc.</instruction>
          ...
        </instructions>

        Today is 2024-01-15
        Your responses should be formatted as Markdown and always respond in Spanish.
        ```

    Note:
        El prompt se genera dinámicamente en cada invocación para incluir
        la fecha actual y cualquier cambio en la configuración.
    """
    # Cargar esquema de base de datos (actualmente no utilizado pero disponible)
    schema = load_db_schema()

    # Determinar el tipo de base de datos objetivo basado en configuración
    db_type = "Oracle" if Config.TARGET_DB_BACKEND == DbBackend.ORACLE else "PostgreSQL"

    # Construir prompt línea por línea para mejor legibilidad
    lines = [
        f"You are a professional {db_type} assistant."
    ]
    lines.append("")
    lines.append(f"Your purpose is to transform natural language requests into precise, efficient {db_type} SQL queries that deliver exactly what the user needs.")
    lines.append("")

    # === INSTRUCCIONES ESTRATÉGICAS ===
    lines.append("<instructions>")
    lines.append("  <instruction>Devise your own strategic plan to explore and understand the database before constructing queries.</instruction>")
    lines.append("  <instruction>Determine the most efficient sequence of database investigation steps based on the specific user request.</instruction>")
    lines.append("  <instruction>Independently identify which database elements require examination to fulfill the query requirements.</instruction>")
    lines.append(f"  <instruction>Formulate and validate your {db_type} SQL query approach based on your professional judgment of the database structure.</instruction>")
    lines.append("  <instruction>Only execute the final SQL query when you've thoroughly validated its correctness and efficiency.</instruction>")
    lines.append("  <instruction>Balance comprehensive exploration with efficient tool usage to minimize unnecessary operations.</instruction>")
    lines.append("  <instruction>For every tool call, include a detailed reasoning parameter explaining your strategic thinking.</instruction>")
    lines.append("  <instruction>Be sure to specify every required parameter for each tool call.</instruction>")

    # === INSTRUCCIONES ESPECÍFICAS POR MOTOR DE BASE DE DATOS ===
    if Config.TARGET_DB_BACKEND == DbBackend.ORACLE:
        # Instrucciones específicas para Oracle Database
        lines.append("  <instruction>Use Oracle-specific SQL syntax including functions like SYSDATE, ROWNUM, DECODE, NVL, etc.</instruction>")
        lines.append("  <instruction>Consider Oracle-specific features like sequences, triggers, and tablespaces when relevant.</instruction>")
    else:  # PostgreSQL
        # Instrucciones específicas para PostgreSQL
        lines.append("  <instruction>Use PostgreSQL-specific SQL syntax including functions like NOW(), LIMIT, COALESCE, etc.</instruction>")
        lines.append("  <instruction>Consider PostgreSQL-specific features like arrays, JSON types, and window functions when relevant.</instruction>")

    lines.append("</instructions>")
    lines.append("")

    # === CONTEXTO Y CONFIGURACIÓN DE RESPUESTA ===
    # Incluir fecha actual para contexto temporal
    lines.append(f"Today is {datetime.now().strftime('%Y-%m-%d')}")

    # Configurar formato de respuesta y idioma
    lines.append("Your responses should be formatted as Markdown and always respond in Spanish. Prefer using tables or lists for displaying data where appropriate.")

    # Definir audiencia objetivo para ajustar nivel técnico
    lines.append(f"Your target audience is business analysts and data scientists who may not be familiar with {db_type} SQL syntax.")
    lines.append("")

    # Unir todas las líneas en un prompt cohesivo
    return "\n".join(lines)
