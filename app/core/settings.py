# app/core/settings.py
"""
Configuración centralizada de la aplicación usando Pydantic Settings.

Este módulo define todas las configuraciones de la aplicación, incluyendo
conexiones a bases de datos, configuración del LLM, servidor, API y seguridad.
Utiliza Pydantic para validación de tipos y carga automática desde variables
de entorno y archivos .env.

Grupos de configuración:
- Base de datos objetivo (la que analiza el agente)
- Configuración del modelo LLM (Ollama)
- Configuración del servidor web
- Configuración de la API
- Configuración CORS
- Configuración de seguridad
- Configuración del agente
"""

from pydantic_settings import BaseSettings
from pydantic import AnyUrl, Field

class Settings(BaseSettings):
    """
    Clase de configuración principal que agrupa todos los settings de la aplicación.

    Utiliza Pydantic Settings para validación automática de tipos y carga
    de variables desde el entorno y archivo .env.
    """

    # === CONFIGURACIÓN DE BASE DE DATOS OBJETIVO ===
    # Base de datos que será analizada por el agente SQL
    target_database_url: AnyUrl = Field(..., env="TARGET_DATABASE_URL",
                                       description="URL de conexión a la base de datos objetivo")
    target_db_backend: str = Field("postgres", env="TARGET_DB_BACKEND",
                                 description="Tipo de base de datos (postgres, oracle, etc.)")

    # === CONFIGURACIÓN DEL MODELO LLM ===
    # Configuración para el modelo de lenguaje en Ollama
    llm_model_name: str = Field(..., env="LLM_MODEL_NAME",
                               description="Nombre del modelo LLM en Ollama")
    llm_temperature: float = Field(0.0, env="LLM_TEMPERATURE",
                                  description="Temperatura para generación (0.0 = determinística)")
    ollama_context_window: int = Field(4096, env="OLLAMA_CONTEXT_WINDOW",
                                      description="Tamaño de ventana de contexto para Ollama")

    # === CONFIGURACIÓN DEL SERVIDOR ===
    # Configuración del servidor web Uvicorn
    server_host: str = Field("0.0.0.0", env="SERVER_HOST",
                            description="Host del servidor")
    server_port: int = Field(8000, env="SERVER_PORT",
                            description="Puerto del servidor")
    server_sse_path: str = Field("/sse", env="SERVER_SSE_PATH",
                                description="Ruta para Server-Sent Events")
    server_transport: str = Field("sse", env="SERVER_TRANSPORT",
                                 description="Tipo de transporte para comunicación")

    # === CONFIGURACIÓN DE LA API ===
    # Metadatos y configuración de la API FastAPI
    api_title: str = Field("SQL Agent API", env="API_TITLE",
                          description="Título de la API")
    api_version: str = Field("0.1.0", env="API_VERSION",
                            description="Versión de la API")
    api_prefix: str = Field("/api/v1", env="API_PREFIX",
                           description="Prefijo para todas las rutas de la API")

    # === CONFIGURACIÓN CORS ===
    # Cross-Origin Resource Sharing para permitir requests desde frontends
    cors_origins: list[str] = Field(
        default=["*"], env="CORS_ORIGINS",
        description="Lista de orígenes permitidos para CORS"
    )

    # === CONFIGURACIÓN DE SEGURIDAD ===
    # Configuración para autenticación y autorización (implementación futura)
    secret_key: str = Field("your-secret-key-change-in-production", env="SECRET_KEY",
                           description="Clave secreta para JWT y encriptación")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES",
                                            description="Tiempo de expiración de tokens de acceso")

    # === CONFIGURACIÓN DEL AGENTE ===
    # Parámetros de comportamiento del agente SQL
    agent_max_iterations: int = Field(5, env="AGENT_MAX_ITERATIONS",
                                     description="Máximo número de iteraciones del agente")

    class Config:
        """Configuración de Pydantic Settings."""
        env_file = ".env"                    # Archivo de variables de entorno
        env_file_encoding = "utf-8"          # Codificación del archivo .env

# Instancia global de configuración disponible en toda la aplicación
settings = Settings()
