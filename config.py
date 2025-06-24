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


QWEN3_8B = ModelConfig("qwen3:8b", temperature=0.0, provider=ModelProvider.OLLAMA)
QWEN3_06B = ModelConfig("qwen3:0.6b", temperature=0.0, provider=ModelProvider.OLLAMA)
QWEN_CODER_7B = ModelConfig("qwen2.5-coder:7b", temperature=0.0, provider=ModelProvider.OLLAMA)
QWEN_CODER_3B = ModelConfig("qwen2.5-coder:3b", temperature=0.0, provider=ModelProvider.OLLAMA)
GRANITE_8B = ModelConfig("granite3.3:8b", temperature=0.0, provider=ModelProvider.OLLAMA)
GRANITE_2B = ModelConfig("granite3.3:2b", temperature=0.0, provider=ModelProvider.OLLAMA)
MISTRAL_7B = ModelConfig("mistral:7b", temperature=0.0, provider=ModelProvider.OLLAMA)
LLAMA3_3B = ModelConfig("llama3.2:3b", temperature=0.0, provider=ModelProvider.OLLAMA)
LLAMA3_1B = ModelConfig("llama3.2:1b", temperature=0.0, provider=ModelProvider.OLLAMA)
COGITO_8B = ModelConfig("cogito:8b", temperature=0.0, provider=ModelProvider.OLLAMA)
DEEPSEEK_1_5B = ModelConfig("deepseek-r1:1.5b", temperature=0.0, provider=ModelProvider.OLLAMA)
DEEPSEEK_8B = ModelConfig("deepseek-r1:8b", temperature=0.0, provider=ModelProvider.OLLAMA)

class Config:
    SEED = 42
    MODEL = ModelConfig(
        name=settings.llm_model_name,
        temperature=settings.llm_temperature,
        provider=ModelProvider.OLLAMA,
    )

    OLLAMA_CONTEXT_WINDOW = settings.ollama_context_window

    DB_BACKEND = DbBackend(settings.db_backend)
    DATABASE_URL = str(settings.database_url)

    class Server:
        HOST = settings.server_host
        PORT = settings.server_port
        SSE_PATH = settings.server_sse_path
        TRANSPORT = settings.server_transport

    class Agent:
        MAX_ITERATIONS = settings.agent_max_iterations
