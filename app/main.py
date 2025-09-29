# app/main.py
"""
Módulo principal de la aplicación FastAPI para SQL Agent.

Este módulo configura y inicializa la aplicación FastAPI que proporciona una API REST
para interactuar con un agente SQL basado en LLM (Large Language Model) que puede
analizar y consultar bases de datos.

Funcionalidades principales:
- Configuración de FastAPI con metadatos y documentación
- Configuración de middleware CORS para permitir requests cross-origin
- Inclusión de rutas de la API
- Endpoint raíz de información
- Configuración del servidor con Uvicorn
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.settings import settings

# Crear aplicación FastAPI con configuración centralizada
app = FastAPI(
    title=settings.api_title,              # Título de la API desde configuración
    version=settings.api_version,          # Versión de la API desde configuración
    description="API para agente SQL que analiza bases de datos usando LLM"
)

# Configurar CORS (Cross-Origin Resource Sharing)
# Permite que aplicaciones frontend desde diferentes dominios accedan a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,   # Orígenes permitidos configurables
    allow_credentials=True,                # Permitir cookies y headers de autenticación
    allow_methods=["*"],                   # Permitir todos los métodos HTTP
    allow_headers=["*"],                   # Permitir todos los headers
    expose_headers=["*"]                   # Exponer todos los headers en la respuesta
)

# Incluir rutas de la API con prefijo configurado
app.include_router(router, prefix=settings.api_prefix)

# Endpoint raíz que proporciona información básica de la API
@app.get("/")
async def root():
    """
    Endpoint raíz que retorna información básica sobre la API.

    Returns:
        dict: Información básica incluyendo mensaje, versión y link a documentación
    """
    return {
        "message": "SQL Agent API",
        "version": settings.api_version,
        "docs": "/docs"
    }

# Punto de entrada para ejecutar la aplicación directamente
if __name__ == "__main__":
    import uvicorn
    # Ejecutar servidor con configuración desde settings
    uvicorn.run(
        "app.main:app",                    # Ruta a la aplicación FastAPI
        host=settings.server_host,         # Host desde configuración
        port=settings.server_port,         # Puerto desde configuración
        reload=True                        # Recarga automática en desarrollo
    )
