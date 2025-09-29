#!/usr/bin/env python3
# start_api.py

"""
Script de inicio para la API del agente SQL.

Este script realiza verificaciones previas al inicio, valida la configuración
y lanza el servidor FastAPI con Uvicorn. Proporciona un punto de entrada
simplificado para ejecutar la aplicación con validaciones de seguridad.

Funcionalidades:
- Validación de variables de entorno requeridas
- Información de configuración al usuario
- Inicio del servidor con configuración optimizada
- Mensajes informativos sobre endpoints disponibles
"""

import os
import sys
from dotenv import load_dotenv

def main():
    """
    Función principal que valida la configuración e inicia el servidor API.

    Realiza las siguientes operaciones:
    1. Carga las variables de entorno desde .env
    2. Verifica que existan las variables críticas
    3. Muestra información de configuración
    4. Inicia el servidor Uvicorn con la aplicación FastAPI

    Exits:
        1: Si faltan variables de entorno críticas
    """
    # Cargar variables de entorno desde archivo .env
    load_dotenv()

    # Definir variables de entorno requeridas para el funcionamiento
    required_vars = [
        "TARGET_DATABASE_URL",  # URL de conexión a la base de datos objetivo
        "LLM_MODEL_NAME"        # Nombre del modelo LLM en Ollama
    ]

    # Verificar que todas las variables críticas estén configuradas
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    # Si faltan variables, mostrar error y salir
    if missing_vars:
        print("❌ Faltan las siguientes variables de entorno:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Crea un archivo .env basado en .env.example")
        sys.exit(1)

    # Mostrar información de configuración validada
    print("✅ Variables de entorno verificadas")
    print(f"🗄️  Base de datos: {os.getenv('TARGET_DATABASE_URL')}")
    print(f"🤖 Modelo LLM: {os.getenv('LLM_MODEL_NAME')}")

    # Importar uvicorn y iniciar el servidor
    import uvicorn
    print("\n🚀 Iniciando API...")
    print("📚 Documentación: http://localhost:8000/docs")
    print("❤️  Health check: http://localhost:8000/api/v1/health")

    # Ejecutar servidor con configuración para desarrollo
    uvicorn.run(
        "app.main:app",          # Ruta a la aplicación FastAPI
        host="0.0.0.0",          # Permitir conexiones desde cualquier IP
        port=8000,               # Puerto estándar para desarrollo
        reload=True              # Recarga automática en cambios de código
    )

if __name__ == "__main__":
    main()
