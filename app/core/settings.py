# app/core/settings.py

from pydantic_settings import BaseSettings
from pydantic import AnyUrl, Field

class Settings(BaseSettings):
    # Target Database (database to be analyzed by the agent)
    target_database_url: AnyUrl = Field(..., env="TARGET_DATABASE_URL")
    target_db_backend: str = Field("postgres", env="TARGET_DB_BACKEND")

    # Modelo LLM
    llm_model_name: str = Field(..., env="LLM_MODEL_NAME")
    llm_temperature: float = Field(0.0, env="LLM_TEMPERATURE")
    ollama_context_window: int = Field(4096, env="OLLAMA_CONTEXT_WINDOW")

    # Server
    server_host: str = Field("0.0.0.0", env="SERVER_HOST")
    server_port: int = Field(8000, env="SERVER_PORT")
    server_sse_path: str = Field("/sse", env="SERVER_SSE_PATH")
    server_transport: str = Field("sse", env="SERVER_TRANSPORT")

    # API Configuration
    api_title: str = Field("SQL Agent API", env="API_TITLE")
    api_version: str = Field("0.1.0", env="API_VERSION")
    api_prefix: str = Field("/api/v1", env="API_PREFIX")
    
    # CORS
    cors_origins: list[str] = Field(
        env="CORS_ORIGINS"
    )
    
    # Security (for future auth implementation)
    secret_key: str = Field("your-secret-key-change-in-production", env="SECRET_KEY")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    


    # Agente
    agent_max_iterations: int = Field(5, env="AGENT_MAX_ITERATIONS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia global
settings = Settings()
