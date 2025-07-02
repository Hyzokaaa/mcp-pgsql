#!/usr/bin/env python3
# start_api.py

"""
Script para iniciar la API del agente SQL
"""

import os
import sys
from dotenv import load_dotenv

def main():
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar variables críticas
    required_vars = [
        "TARGET_DATABASE_URL",
        "LLM_MODEL_NAME"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Faltan las siguientes variables de entorno:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Crea un archivo .env basado en .env.example")
        sys.exit(1)
    
    print("✅ Variables de entorno verificadas")
    print(f"🗄️  Base de datos: {os.getenv('TARGET_DATABASE_URL')}")
    print(f"🤖 Modelo LLM: {os.getenv('LLM_MODEL_NAME')}")
    
    # Iniciar servidor
    import uvicorn
    print("\n🚀 Iniciando API...")
    print("📚 Documentación: http://localhost:8000/docs")
    print("❤️  Health check: http://localhost:8000/api/v1/health")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()
