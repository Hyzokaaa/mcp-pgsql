# app/core/settings.py
from pydantic_settings import BaseSettings
from pydantic import AnyUrl, Field

class Settings(BaseSettings):
    # Base de datos
    database_url: AnyUrl = Field(..., env="DATABASE_URL")
    db_backend: str = Field("postgres", env="DB_BACKEND")

    # Modelo LLM
    llm_model_name: str = Field(..., env="LLM_MODEL_NAME")
    llm_temperature: float = Field(0.0, env="LLM_TEMPERATURE")
    ollama_context_window: int = Field(4096, env="OLLAMA_CONTEXT_WINDOW")

    # Server
    server_host: str = Field("0.0.0.0", env="SERVER_HOST")
    server_port: int = Field(8000, env="SERVER_PORT")
    server_sse_path: str = Field("/sse", env="SERVER_SSE_PATH")
    server_transport: str = Field("sse", env="SERVER_TRANSPORT")

    # Agente
    agent_max_iterations: int = Field(5, env="AGENT_MAX_ITERATIONS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia global
settings = Settings()
