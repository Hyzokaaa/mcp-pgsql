# Documentación Técnica - SQL Agent

## 📋 Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Módulos y Componentes](#módulos-y-componentes)
3. [Base de Datos](#base-de-datos)
4. [Agente SQL](#agente-sql)
5. [API REST](#api-rest)
6. [Configuración](#configuración)
7. [Seguridad](#seguridad)
8. [Logging y Monitoreo](#logging-y-monitoreo)
9. [Desarrollo](#desarrollo)
10. [Troubleshooting](#troubleshooting)

---

## 🏗️ Arquitectura del Sistema

### Visión General
SQL Agent es un sistema de agente conversacional que permite interactuar con bases de datos usando lenguaje natural. Utiliza modelos LLM (Large Language Models) con capacidades de tool calling para ejecutar consultas SQL de manera segura.

### Componentes Principales

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API REST      │    │   Agente SQL    │
│                 │    │                 │    │                 │
│ • Streamlit UI  │◄──►│ • FastAPI       │◄──►│ • LangChain     │
│ • Chat Interface│    │ • CORS Config   │    │ • Ollama LLM    │
│ • Real-time     │    │ • Validation    │    │ • Tool Calling  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Herramientas   │
                                               │                 │
                                               │ • list_tables   │
                                               │ • describe_table│
                                               │ • execute_query │
                                               │ • sample_table  │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │ Base de Datos   │
                                               │                 │
                                               │ • PostgreSQL    │
                                               │ • Oracle        │
                                               │ • SQLAlchemy    │
                                               └─────────────────┘
```

### Stack Tecnológico

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **LLM**: Ollama (modelos locales como QWEN, LLAMA)
- **Frontend**: Streamlit para UI web
- **Base de Datos**: PostgreSQL, Oracle (soporte multi-motor)
- **Validación**: Pydantic, SQLparse
- **Async**: asyncio para operaciones asíncronas

---

## 🧩 Módulos y Componentes

### app/main.py
**Propósito**: Aplicación FastAPI principal
- Configuración de CORS
- Inclusión de rutas
- Middleware de autenticación (futuro)
- Endpoint raíz con información

### app/core/settings.py
**Propósito**: Configuración centralizada
- Validación con Pydantic Settings
- Variables de entorno
- Configuración por tipo de base de datos
- Valores por defecto seguros

### app/agent/agent.py
**Propósito**: Lógica principal del agente
- Ciclo iterativo de procesamiento
- Gestión de herramientas
- Control de iteraciones máximas
- Logging detallado

### app/agent/tools.py
**Propósito**: Herramientas SQL del agente
```python
# Herramientas disponibles:
- list_db_tables()      # Lista tablas de usuario
- describe_db_table()   # Describe estructura de tabla
- execute_query()       # Ejecuta consultas SELECT
- sample_table()        # Obtiene muestra de datos
```

### app/db/db.py
**Propósito**: Capa de acceso a datos
- Abstracción sobre SQLAlchemy
- Soporte multi-motor (PostgreSQL/Oracle)
- Operaciones de introspección
- Manejo seguro de conexiones

### app/db/validators.py
**Propósito**: Validaciones de seguridad
- Solo consultas SELECT permitidas
- Prevención de inyección SQL
- Bloqueo de comentarios
- Validación de sintaxis

---

## 🗄️ Base de Datos

### Soporte Multi-Motor

#### PostgreSQL
```python
# Configuración
TARGET_DATABASE_URL=postgresql://user:password@localhost:5432/database
TARGET_DB_BACKEND=postgres

# Características soportadas:
- LIMIT para paginación
- Tipos JSON nativos
- Arrays
- Window functions
- COALESCE, NOW()
```

#### Oracle
```python
# Configuración
TARGET_DATABASE_URL=oracle+oracledb://user:password@localhost:1521/service
TARGET_DB_BACKEND=oracle

# Características soportadas:
- ROWNUM para paginación
- SYSDATE
- DECODE, NVL
- Sequences
- Tablespaces
```

### Operaciones Soportadas

#### Introspección
- **Listar tablas**: Obtiene solo tablas de usuario (excluye sistema)
- **Describir tabla**: Columnas, tipos, claves primarias
- **Muestreo**: Datos representativos con paginación

#### Consultas
- **Solo SELECT**: Política de solo lectura estricta
- **Validación**: SQLparse para análisis sintáctico
- **Sanitización**: Eliminación de comentarios y caracteres peligrosos

---

## 🤖 Agente SQL

### Flujo de Procesamiento

```
1. Recepción de consulta en lenguaje natural
   ├── Validación de entrada
   └── Contexto del historial

2. Análisis por LLM
   ├── Comprensión de intención
   ├── Planificación estratégica
   └── Selección de herramientas

3. Ejecución de herramientas
   ├── list_tables (exploración)
   ├── describe_table (esquema)
   ├── sample_table (datos)
   └── execute_query (consulta final)

4. Síntesis de respuesta
   ├── Análisis de resultados
   ├── Generación de insights
   └── Formateo en Markdown
```

### Características del LLM

#### Configuración Ollama
```python
ChatOllama(
    model="qwen3:0.6b",           # Modelo ligero y eficiente
    temperature=0.0,              # Respuestas determinísticas
    num_ctx=4096,                 # Ventana de contexto amplia
    disable_streaming=True,       # Compatibilidad con tools
    keep_alive=-1                 # Persistencia en memoria
)
```

#### Modelos Recomendados
- **QWEN3:0.5B/8B**: Óptimo para tool calling
- **LLAMA:3B**: Balance rendimiento/precisión
- **Criterios**: Soporte nativo para function calling

### Prompt Engineering

#### System Prompt Dinámico
```python
def build_system_prompt():
    # Adapta automáticamente según:
    - Tipo de base de datos (PostgreSQL/Oracle)
    - Fecha actual para contexto temporal
    - Instrucciones específicas del motor
    - Audiencia objetivo (analistas/científicos de datos)
```

---

## 🌐 API REST

### Endpoints Disponibles

#### POST /api/v1/chat
**Propósito**: Endpoint principal de conversación
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

**Respuesta**:
```json
{
  "response": "Análisis completo con resultados",
  "status": "success"
}
```

#### GET /api/v1/health
**Propósito**: Verificación de estado del servicio
```json
{
  "status": "healthy",
  "service": "SQL Agent API"
}
```

### Configuración CORS
```python
# Permitir requests desde frontends
allow_origins=["http://localhost:3000", "https://miapp.com"]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

### Manejo de Errores
```python
# Errores comunes:
- 400: Mensaje de usuario faltante
- 500: Error en procesamiento del agente
- Validación: Consultas SQL inválidas
```

---

## ⚙️ Configuración

### Variables de Entorno

#### Base de Datos Objetivo
```bash
# PostgreSQL
TARGET_DATABASE_URL=postgresql://user:password@localhost:5432/company_data
TARGET_DB_BACKEND=postgres

# Oracle
TARGET_DATABASE_URL=oracle+oracledb://user:password@localhost:1521/service_name
TARGET_DB_BACKEND=oracle
```

#### Modelo LLM
```bash
LLM_MODEL_NAME=qwen3:0.6b
LLM_TEMPERATURE=0.0
OLLAMA_CONTEXT_WINDOW=4096
AGENT_MAX_ITERATIONS=5
```

#### API
```bash
API_TITLE=SQL Agent API
API_VERSION=0.1.0
API_PREFIX=/api/v1
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

#### CORS
```bash
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

### Archivos de Configuración

#### .env.example
Template con todas las variables necesarias y documentación

#### pyproject.toml
```toml
[project]
name = "sql-agent"
dependencies = [
    "fastapi>=0.104.0",
    "langchain-ollama>=0.3.3",
    "sqlalchemy>=2.0.41",
    "pydantic>=2.11.5"
]

[tool.pdm.scripts]
api = "uvicorn app.main:app --reload"
ui = "streamlit run app/ui.py"
direct = "python -m app.direct_client"
```

---

## 🔒 Seguridad

### Políticas de Seguridad

#### Solo Lectura
- **Únicamente SELECT**: Bloqueo estricto de INSERT, UPDATE, DELETE
- **Sin DDL**: Prevención de DROP, ALTER, TRUNCATE
- **Sin privilegios**: Bloqueo de GRANT, REVOKE

#### Validación SQL
```python
def validate_select_only(sql: str):
    # 1. Prohibir comentarios (-- y /* */)
    # 2. Un solo statement por consulta
    # 3. Debe comenzar con SELECT
    # 4. Sin keywords peligrosas
```

#### Prevención de Inyección
- **SQLparse**: Análisis sintáctico robusto
- **Sanitización**: Eliminación de caracteres peligrosos
- **SQLAlchemy text()**: Consultas parametrizadas

### Límites y Controles

#### Iteraciones del Agente
```python
AGENT_MAX_ITERATIONS=5  # Prevenir bucles infinitos
```

#### Validación de Configuración
```python
# Verificar coherencia URL/backend
if "postgresql" not in url and backend == "postgres":
    raise ValueError("URL inconsistente con backend")
```

---

## 📊 Logging y Monitoreo

### Sistema de Logging

#### Logging Local (app/agent/logging_local.py)
```python
# Paneles informativos con colores:
log_panel(
    title="Tool Call",
    content={"tool": name, "args": args},
    border_style="magenta"
)
```

#### Niveles de Log
- **User Request**: Verde - Consultas de entrada
- **Tool Call**: Magenta - Llamadas a herramientas
- **Tool Result**: Amarillo - Resultados exitosos
- **Tool Error**: Rojo - Errores en herramientas

### Monitoreo

#### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

#### Métricas Sugeridas
- Tiempo de respuesta por consulta
- Número de tool calls por sesión
- Errores de validación SQL
- Uso de herramientas

---

## 💻 Desarrollo

### Estructura del Proyecto
```
mcp-pgsql/
├── app/
│   ├── agent/          # Lógica del agente
│   ├── api/            # Endpoints REST
│   ├── core/           # Configuración
│   ├── db/             # Acceso a datos
│   ├── tests/          # Pruebas unitarias
│   ├── main.py         # App FastAPI
│   ├── ui.py           # Interfaz Streamlit
│   └── direct_client.py # Cliente directo
├── docs/               # Documentación
├── examples/           # Ejemplos de uso
├── .env.example        # Template configuración
└── pyproject.toml      # Dependencias
```

### Comandos de Desarrollo

#### Instalación
```bash
git clone <repository>
cd mcp-pgsql
pip install -e .
cp .env.example .env
# Editar .env con tu configuración
```

#### Ejecución
```bash
# API REST
pdm run api
# o python start_api.py

# Interfaz Streamlit
pdm run ui

# Cliente directo
pdm run direct
```

#### Testing
```bash
pytest app/tests/
```

### Extensibilidad

#### Nuevas Herramientas
```python
@tool(parse_docstring=True)
def nueva_herramienta(parametro: str) -> str:
    """Descripción de la herramienta."""
    # Implementación
    return resultado
```

#### Nuevos Backends
```python
# En app/db/db.py
elif Config.TARGET_DB_BACKEND == DbBackend.MYSQL:
    query = f"SELECT * FROM {table_name} LIMIT {row_sample_size}"
```

---

## 🔧 Troubleshooting

### Problemas Comunes

#### Error de Conexión a Ollama
```bash
# Verificar que Ollama esté ejecutándose
ollama list
ollama pull qwen3:0.6b
```

#### Error de Base de Datos
```bash
# Verificar conectividad
psql -h localhost -U user -d database
sqlplus user/password@localhost:1521/service
```

#### Error de Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Logs de Diagnóstico

#### Habilitar Verbose
```python
# En app/agent/models.py
ChatOllama(verbose=True)  # Para debugging
```

#### Verificar Configuración
```python
from app.core.settings import settings
print(settings.model_dump())
```

### Rendimiento

#### Optimizaciones
- Mantener modelo en memoria (`keep_alive=-1`)
- Usar modelos ligeros (QWEN3:0.5B)
- Limitar ventana de contexto según necesidad
- Cachear conexiones de base de datos

#### Monitoreo de Recursos
```bash
# CPU/Memoria del modelo
ollama ps

# Conexiones de base de datos
SELECT * FROM pg_stat_activity;  -- PostgreSQL
SELECT * FROM v$session;        -- Oracle
```

---

## 📝 Notas de Desarrollo

### Principios de Diseño
1. **Seguridad por defecto**: Solo lectura, validación estricta
2. **Configurabilidad**: Adaptable a diferentes entornos
3. **Extensibilidad**: Fácil agregar nuevas funcionalidades
4. **Observabilidad**: Logging detallado para debugging
5. **Rendimiento**: Optimizado para respuestas rápidas

### Roadmap Futuro
- [ ] Autenticación y autorización
- [ ] Múltiples bases de datos simultáneas
- [ ] Cache de consultas frecuentes
- [ ] Exportación de resultados
- [ ] Dashboard de analytics
- [ ] Integración con BI tools

---
