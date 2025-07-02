# app/core/config.py

import os
from dataclasses import dataclass
from enum import Enum

from app.core.settings import settings


class ModelProvider(str, Enum):
    OLLAMA = "ollama"

class DbBackend(str, Enum):
    POSTGRES = "postgres"
    ORACLE = "oracle"

@dataclass
class ModelConfig:
    name: str
    temperature: float
    provider: ModelProvider

class Config:
    env_file = ".env"
    SEED = 42
    MODEL = ModelConfig(
        name=settings.llm_model_name,
        temperature=settings.llm_temperature,
        provider=ModelProvider.OLLAMA,
    )

    OLLAMA_CONTEXT_WINDOW = settings.ollama_context_window

    # Target Database (for agent queries)
    TARGET_DB_BACKEND = DbBackend(settings.target_db_backend)
    TARGET_DATABASE_URL = str(settings.target_database_url)

    class Server:
        HOST = settings.server_host
        PORT = settings.server_port
        SSE_PATH = settings.server_sse_path
        TRANSPORT = settings.server_transport

    class Agent:
        MAX_ITERATIONS = settings.agent_max_iterations
