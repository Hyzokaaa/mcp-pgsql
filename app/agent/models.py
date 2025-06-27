from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from app.core.config import Config, ModelConfig
import httpx

http_client = httpx.AsyncClient(
    proxy="http://10.0.14.1:8080",
    timeout=300  # Aumenta timeout
)
def create_llm(model_config: ModelConfig) -> BaseChatModel:
    return ChatOllama(
        model=model_config.name,
        temperature=model_config.temperature,
        num_ctx=Config.OLLAMA_CONTEXT_WINDOW,
        verbose=False,
        keep_alive=-1,
        disable_streaming=True,
        http_client=http_client
    )