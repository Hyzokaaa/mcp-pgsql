# mcp-pgsql

Sistema de agente que permite la comunicación con bases de datos utilizando LLM en Ollama.

## Actualmente funcionan con tool_calling los modelos:

- QWEN3:0.5B
- QWEN3:8B
- LLAMA:3B

## 🚀 Inicio Rápido

### 1. Configuración

```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar las variables de entorno
# - TARGET_DATABASE_URL: URL de tu base de datos
# - LLM_MODEL_NAME: Modelo de Ollama a usar
```

### 2. Modos de Ejecución

#### API REST

```bash
# Iniciar servidor API
python start_api.py

# O usando PDM
pdm run api
```

- **Documentación**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/api/v1/health

#### Cliente Directo

```bash
pdm run direct
```

#### Interfaz Streamlit

```bash
pdm run ui
```

## 📡 API Usage

### Endpoint Principal: `/api/v1/chat`

```json
{
  "messages": [
    {
      "role": "user",
      "content": "¿Qué tablas hay en la base de datos?"
    }
  ]
}
```

Ver más ejemplos en `examples/API_EXAMPLES.md`
