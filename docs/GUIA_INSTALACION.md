# Guía de Instalación y Configuración - SQL Agent

## 🎯 Guía Rápida de Instalación

### Requisitos Previos

Antes de instalar SQL Agent, asegúrate de tener:

- ✅ **Python 3.11 o superior**
- ✅ **Git** para clonar el repositorio
- ✅ **Ollama** instalado y funcionando
- ✅ **Base de datos** (PostgreSQL u Oracle)
- ✅ **PDM** (Python Dependency Management) *recomendado*

---

## 📥 Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/usuario/mcp-pgsql.git
cd mcp-pgsql
```

### 2. Configurar Entorno Python

#### Opción A: Usando PDM (Recomendado)
```bash
# Instalar PDM si no lo tienes
pip install pdm

# Instalar dependencias
pdm install
```

#### Opción B: Usando pip tradicional
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -e .
```

### 3. Configurar Variables de Entorno

```bash
# Copiar template de configuración
cp .env.example .env

# Editar archivo .env con tu configuración
nano .env  # o tu editor preferido
```

### 4. Configurar Ollama

```bash
# Instalar modelo recomendado
ollama pull qwen3:0.6b

# Verificar que esté funcionando
ollama list
```

### 5. Verificar Instalación

```bash
# Iniciar API
python start_api.py

# En otra terminal, verificar estado
curl http://localhost:8000/api/v1/health
```

**✅ Si ves `{"status": "healthy"}`, ¡la instalación fue exitosa!**

---

## ⚙️ Configuración Detallada

### Archivo .env - Configuración Completa

```bash
# ==========================================
# CONFIGURACIÓN DE BASE DE DATOS OBJETIVO
# ==========================================

# PostgreSQL
TARGET_DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_bd
TARGET_DB_BACKEND=postgres

# Oracle (alternativa)
# TARGET_DATABASE_URL=oracle+oracledb://usuario:contraseña@localhost:1521/servicio
# TARGET_DB_BACKEND=oracle

# ==========================================
# CONFIGURACIÓN DEL MODELO LLM
# ==========================================

# Modelo a utilizar (debe estar instalado en Ollama)
LLM_MODEL_NAME=qwen3:0.6b

# Temperatura (0.0 = determinístico, 1.0 = creativo)
LLM_TEMPERATURE=0.0

# Tamaño de ventana de contexto
OLLAMA_CONTEXT_WINDOW=4096

# Máximo número de iteraciones del agente
AGENT_MAX_ITERATIONS=5

# ==========================================
# CONFIGURACIÓN DE LA API
# ==========================================

# Información de la API
API_TITLE=SQL Agent API
API_VERSION=0.1.0
API_PREFIX=/api/v1

# ==========================================
# CONFIGURACIÓN DEL SERVIDOR
# ==========================================

# Host y puerto del servidor
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# ==========================================
# CONFIGURACIÓN CORS
# ==========================================

# Orígenes permitidos para CORS (separados por comas)
# Ejemplo para desarrollo con React/Vue
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","https://miapp.com"]

# ==========================================
# CONFIGURACIÓN DE SEGURIDAD (FUTURO)
# ==========================================

# Clave secreta para JWT (cambiar en producción)
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion

# Tiempo de expiración de tokens (minutos)
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Configuración de Base de Datos

#### PostgreSQL

1. **Instalar PostgreSQL**:
   ```bash
   # Ubuntu/Debian
   sudo apt install postgresql postgresql-contrib

   # macOS
   brew install postgresql

   # Windows
   # Descargar desde https://www.postgresql.org/download/
   ```

2. **Crear base de datos y usuario**:
   ```sql
   -- Conectar como superusuario
   sudo -u postgres psql

   -- Crear usuario
   CREATE USER sql_agent WITH PASSWORD 'tu_contraseña';

   -- Crear base de datos
   CREATE DATABASE mi_empresa OWNER sql_agent;

   -- Otorgar permisos de lectura
   GRANT CONNECT ON DATABASE mi_empresa TO sql_agent;
   GRANT USAGE ON SCHEMA public TO sql_agent;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO sql_agent;
   ```

3. **URL de conexión**:
   ```bash
   TARGET_DATABASE_URL=postgresql://sql_agent:tu_contraseña@localhost:5432/mi_empresa
   ```

#### Oracle Database

1. **Instalar Oracle Client**:
   ```bash
   # Descargar Oracle Instant Client
   # https://www.oracle.com/database/technologies/instant-client.html

   # Instalar driver Python
   pip install oracledb
   ```

2. **Configurar usuario**:
   ```sql
   -- Conectar como SYSTEM o DBA
   sqlplus system/contraseña@localhost:1521/XE

   -- Crear usuario
   CREATE USER sql_agent IDENTIFIED BY tu_contraseña;

   -- Otorgar permisos básicos
   GRANT CONNECT, RESOURCE TO sql_agent;
   GRANT SELECT ANY TABLE TO sql_agent;
   ```

3. **URL de conexión**:
   ```bash
   TARGET_DATABASE_URL=oracle+oracledb://sql_agent:tu_contraseña@localhost:1521/XE
   ```

### Configuración de Ollama

1. **Instalar Ollama**:
   ```bash
   # Linux
   curl -fsSL https://ollama.com/install.sh | sh

   # macOS
   brew install ollama

   # Windows
   # Descargar desde https://ollama.com/download
   ```

2. **Iniciar servicio**:
   ```bash
   ollama serve
   ```

3. **Instalar modelos recomendados**:
   ```bash
   # Modelo ligero y rápido (recomendado para desarrollo)
   ollama pull qwen3:0.6b

   # Modelo más potente (recomendado para producción)
   ollama pull qwen3:8b

   # Alternativa con LLAMA
   ollama pull llama3:8b
   ```

4. **Verificar instalación**:
   ```bash
   ollama list
   ollama run qwen3:0.6b "Hola, ¿funcionas correctamente?"
   ```

---

## 🚀 Modos de Ejecución

### 1. API REST (Producción)

```bash
# Opción 1: Script personalizado
python start_api.py

# Opción 2: PDM
pdm run api

# Opción 3: Uvicorn directo
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Acceso**:
- 🌐 API: http://localhost:8000
- 📚 Documentación: http://localhost:8000/docs
- 🔍 Redoc: http://localhost:8000/redoc

### 2. Interfaz Web (Streamlit)

```bash
# Opción 1: PDM
pdm run ui

# Opción 2: Streamlit directo
streamlit run app/ui.py
```

**Acceso**: http://localhost:8501

### 3. Cliente Directo (Terminal)

```bash
# Opción 1: PDM
pdm run direct

# Opción 2: Python directo
python -m app.direct_client
```

---

## 🐳 Instalación con Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY pyproject.toml .
COPY README.md .

# Instalar PDM y dependencias
RUN pip install pdm
RUN pdm install --prod

# Copiar código de la aplicación
COPY app/ app/

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["pdm", "run", "api"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  sql-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - TARGET_DATABASE_URL=postgresql://user:password@db:5432/company
      - LLM_MODEL_NAME=qwen3:0.6b
      - OLLAMA_HOST=http://ollama:11434
    depends_on:
      - db
      - ollama
    volumes:
      - ./.env:/app/.env

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: company
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  postgres_data:
  ollama_data:
```

### Ejecutar con Docker

```bash
# Construir y ejecutar
docker-compose up -d

# Instalar modelo en Ollama
docker-compose exec ollama ollama pull qwen3:0.6b

# Verificar servicios
docker-compose ps
curl http://localhost:8000/api/v1/health
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno Adicionales

```bash
# ==========================================
# CONFIGURACIÓN DE LOGGING
# ==========================================

# Nivel de logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Archivo de log
LOG_FILE=logs/sql_agent.log

# ==========================================
# CONFIGURACIÓN DE RENDIMIENTO
# ==========================================

# Pool de conexiones de base de datos
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10

# Timeout para consultas SQL (segundos)
DB_QUERY_TIMEOUT=30

# Timeout para el modelo LLM (segundos)
LLM_TIMEOUT=60

# ==========================================
# CONFIGURACIÓN DE CACHE
# ==========================================

# Habilitar cache de respuestas
ENABLE_CACHE=true

# TTL del cache (segundos)
CACHE_TTL=300

# ==========================================
# CONFIGURACIÓN DE MONITOREO
# ==========================================

# Habilitar métricas de Prometheus
ENABLE_METRICS=false

# Puerto para métricas
METRICS_PORT=9090
```

### Configuración de Producción

#### 1. Seguridad

```bash
# Generar clave secreta segura
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Configurar en .env
SECRET_KEY=tu_clave_generada_aleatoriamente
```

#### 2. Base de Datos

```bash
# Usar pools de conexiones
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30

# SSL para conexiones seguras
TARGET_DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
```

#### 3. Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name sql-agent.miempresa.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 4. Proceso Manager (Systemd)

```ini
# /etc/systemd/system/sql-agent.service
[Unit]
Description=SQL Agent API
After=network.target

[Service]
Type=simple
User=sql-agent
WorkingDirectory=/opt/sql-agent
Environment=PATH=/opt/sql-agent/venv/bin
ExecStart=/opt/sql-agent/venv/bin/python start_api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar y iniciar servicio
sudo systemctl enable sql-agent
sudo systemctl start sql-agent
sudo systemctl status sql-agent
```

---

## 🧪 Verificación de Instalación

### Script de Verificación

```bash
#!/bin/bash
# verify_installation.sh

echo "🔍 Verificando instalación de SQL Agent..."

# Verificar Python
python_version=$(python --version 2>&1)
echo "✅ Python: $python_version"

# Verificar dependencias
echo "🔍 Verificando dependencias..."
python -c "import fastapi, sqlalchemy, langchain_ollama" && echo "✅ Dependencias principales OK"

# Verificar Ollama
if command -v ollama &> /dev/null; then
    echo "✅ Ollama está instalado"
    ollama list | grep -q "qwen3" && echo "✅ Modelo qwen3 disponible" || echo "⚠️  Modelo qwen3 no encontrado"
else
    echo "❌ Ollama no está instalado"
fi

# Verificar configuración
if [ -f ".env" ]; then
    echo "✅ Archivo .env encontrado"
    if grep -q "TARGET_DATABASE_URL" .env; then
        echo "✅ Configuración de base de datos presente"
    else
        echo "⚠️  Configuración de base de datos faltante"
    fi
else
    echo "❌ Archivo .env no encontrado"
fi

# Intentar iniciar API
echo "🚀 Intentando iniciar API..."
python -c "from app.main import app; print('✅ Aplicación FastAPI puede importarse')"

echo "🎉 Verificación completada"
```

### Tests de Funcionalidad

```python
# test_installation.py
import requests
import json

def test_health_endpoint():
    """Verificar que el endpoint de salud funciona"""
    try:
        response = requests.get("http://localhost:8000/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✅ Health endpoint OK")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")

def test_chat_endpoint():
    """Verificar que el endpoint de chat funciona"""
    try:
        payload = {
            "messages": [
                {"role": "user", "content": "¿Qué tablas hay en la base de datos?"}
            ]
        }
        response = requests.post(
            "http://localhost:8000/api/v1/chat",
            json=payload,
            timeout=30
        )
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        print("✅ Chat endpoint OK")
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")

if __name__ == "__main__":
    test_health_endpoint()
    test_chat_endpoint()
```

---

## 🚨 Solución de Problemas Comunes

### Error: "ModuleNotFoundError"

```bash
# Verificar que el entorno virtual esté activado
which python
pip list

# Reinstalar dependencias
pip install -e .
```

### Error: "Connection refused" (Ollama)

```bash
# Verificar que Ollama esté ejecutándose
ps aux | grep ollama

# Iniciar Ollama
ollama serve

# Verificar puerto
netstat -tlnp | grep 11434
```

### Error: "Database connection failed"

```bash
# Verificar conectividad
# PostgreSQL
psql -h localhost -U usuario -d basedatos

# Oracle
sqlplus usuario/contraseña@localhost:1521/servicio

# Verificar URL en .env
echo $TARGET_DATABASE_URL
```

### Error: "Port already in use"

```bash
# Encontrar proceso usando el puerto
lsof -i :8000

# Terminar proceso
kill -9 <PID>

# O usar puerto diferente
SERVER_PORT=8001 python start_api.py
```

---

## 📊 Monitoreo y Mantenimiento

### Logs

```bash
# Ver logs en tiempo real
tail -f logs/sql_agent.log

# Logs con docker-compose
docker-compose logs -f sql-agent
```

### Métricas

```python
# Habilitar métricas de Prometheus
ENABLE_METRICS=true
METRICS_PORT=9090
```

### Backup de Configuración

```bash
# Crear backup de configuración
tar -czf sql_agent_config_$(date +%Y%m%d).tar.gz .env pyproject.toml
```

---

## 🔄 Actualización

### Actualizar Código

```bash
# Obtener últimos cambios
git pull origin main

# Actualizar dependencias
pdm update

# Reiniciar servicios
sudo systemctl restart sql-agent
```

### Actualizar Modelos

```bash
# Actualizar modelo de Ollama
ollama pull qwen3:latest

# Verificar nueva versión
ollama list
```

---
