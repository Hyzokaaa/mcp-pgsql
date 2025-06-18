import os
from dataclasses import dataclass
from enum import Enum


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
    MODEL = QWEN3_8B
    OLLAMA_CONTEXT_WINDOW = 4096

    DB_BACKEND = os.getenv("DB_BACKEND", "postgres").lower()

    if DB_BACKEND == DbBackend.POSTGRES:
        DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:*Hyzoka01021268345@localhost:5432/rentacar"
        )
    elif DB_BACKEND == DbBackend.ORACLE:
        DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "oracle+oracledb://USER_DWH:Systemanager2020@10.0.0.32:1521/?service_name=ORCL"
        )
    else:
        raise ValueError(f"Unsupported DB_BACKEND: {DB_BACKEND}")

    class Server:
        HOST = "localhost"
        PORT = 8000
        SSE_PATH = "/sse"
        TRANSPORT = "sse"

    class Agent:
        MAX_ITERATIONS = 5
