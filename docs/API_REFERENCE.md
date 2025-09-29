# Referencia de API - SQL Agent

## 📋 Índice

1. [Visión General](#visión-general)
2. [Autenticación](#autenticación)
3. [Endpoints](#endpoints)
4. [Modelos de Datos](#modelos-de-datos)
5. [Códigos de Respuesta](#códigos-de-respuesta)
6. [Ejemplos de Uso](#ejemplos-de-uso)
7. [SDKs y Bibliotecas](#sdks-y-bibliotecas)
8. [Rate Limiting](#rate-limiting)
9. [Webhooks](#webhooks)
10. [Testing](#testing)

---

## 🌐 Visión General

La API REST de SQL Agent proporciona una interfaz programática para interactuar con el agente conversacional de bases de datos. Permite integrar las capacidades del agente en aplicaciones externas, automatizaciones y workflows.

### URL Base
```
http://localhost:8000
```

### Formato de Datos
- **Request**: `application/json`
- **Response**: `application/json`
- **Encoding**: UTF-8

### Versioning
- **Versión actual**: v1
- **Prefijo**: `/api/v1`
- **Header**: `Accept: application/json`

---

## 🔐 Autenticación

**Estado actual**: La API no requiere autenticación.

**Futuras versiones** incluirán:
- JWT Bearer tokens
- API Keys
- OAuth 2.0

```http
# Futuro formato de autenticación
Authorization: Bearer <token>
```

---

## 🛠️ Endpoints

### 1. Health Check

#### `GET /api/v1/health`

Verifica el estado del servicio.

**Parámetros**: Ninguno

**Respuesta**:
```json
{
  "status": "healthy",
  "service": "SQL Agent API"
}
```

**Códigos de estado**:
- `200`: Servicio funcionando correctamente
- `503`: Servicio no disponible

**Ejemplo**:
```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

---

### 2. Chat Endpoint

#### `POST /api/v1/chat`

Envía una consulta al agente SQL y recibe una respuesta procesada.

**Content-Type**: `application/json`

**Parámetros del body**:

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `messages` | Array[Message] | Sí | Lista de mensajes de la conversación |

**Modelo Message**:
```json
{
  "role": "user | assistant | system",
  "content": "string"
}
```

**Respuesta exitosa**:
```json
{
  "response": "string",
  "status": "success"
}
```

**Códigos de estado**:
- `200`: Consulta procesada exitosamente
- `400`: Solicitud inválida (mensaje de usuario faltante)
- `422`: Error de validación de datos
- `500`: Error interno del servidor

**Ejemplo básico**:
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "¿Qué tablas hay en la base de datos?"
      }
    ]
  }'
```

**Ejemplo con historial**:
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "¿Qué tablas hay en la base de datos?"
      },
      {
        "role": "assistant",
        "content": "Encontré las siguientes tablas: usuarios, productos, pedidos..."
      },
      {
        "role": "user",
        "content": "Muéstrame la estructura de la tabla usuarios"
      }
    ]
  }'
```

---

## 📊 Modelos de Datos

### ChatMessage

Representa un mensaje individual en la conversación.

```json
{
  "role": "user | assistant | system",
  "content": "string"
}
```

**Campos**:
- `role` (string, requerido): Rol del mensaje
  - `"user"`: Mensaje del usuario
  - `"assistant"`: Respuesta del agente
  - `"system"`: Instrucciones del sistema
- `content` (string, requerido): Contenido textual del mensaje

### ChatRequest

Modelo para solicitudes al endpoint de chat.

```json
{
  "messages": [
    {
      "role": "user",
      "content": "string"
    }
  ]
}
```

**Campos**:
- `messages` (Array[ChatMessage], requerido): Lista de mensajes de la conversación

### ChatResponse

Modelo para respuestas del endpoint de chat.

```json
{
  "response": "string",
  "status": "success | error"
}
```

**Campos**:
- `response` (string): Respuesta generada por el agente
- `status` (string): Estado de la operación (default: "success")

### ErrorResponse

Modelo para respuestas de error.

```json
{
  "detail": "string",
  "error_code": "string",
  "timestamp": "string"
}
```

---

## 📋 Códigos de Respuesta

### Códigos de Éxito

| Código | Descripción |
|--------|-------------|
| `200 OK` | Solicitud procesada exitosamente |

### Códigos de Error del Cliente

| Código | Descripción | Detalles |
|--------|-------------|----------|
| `400 Bad Request` | Solicitud malformada | Mensaje de usuario faltante |
| `422 Unprocessable Entity` | Error de validación | Datos de entrada inválidos |

### Códigos de Error del Servidor

| Código | Descripción | Detalles |
|--------|-------------|----------|
| `500 Internal Server Error` | Error interno | Error en procesamiento del agente |
| `503 Service Unavailable` | Servicio no disponible | Base de datos o LLM no disponible |

### Estructura de Errores

```json
{
  "detail": "Descripción específica del error",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🚀 Ejemplos de Uso

### Ejemplo 1: Consulta Simple

**Request**:
```http
POST /api/v1/chat HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "¿Cuántos usuarios hay en la base de datos?"
    }
  ]
}
```

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "response": "He consultado la base de datos y encontré **1,247 usuarios** registrados.\n\nDetalles de la consulta:\n- Tabla consultada: `usuarios`\n- Query ejecutada: `SELECT COUNT(*) FROM usuarios`\n- Resultado: 1,247 registros\n\n¿Te gustaría conocer algún detalle específico sobre estos usuarios?",
  "status": "success"
}
```

### Ejemplo 2: Análisis de Ventas

**Request**:
```http
POST /api/v1/chat HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "Analiza las ventas del último mes y compáralas con el mes anterior"
    }
  ]
}
```

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "response": "## Análisis de Ventas - Último Mes\n\nHe analizado las ventas y aquí están los resultados:\n\n### Resumen Comparativo\n\n| Período | Total Ventas | Número Pedidos | Promedio por Pedido |\n|---------|--------------|----------------|---------------------|\n| Mes Actual | $58,420.75 | 189 | $309.00 |\n| Mes Anterior | $52,180.50 | 167 | $312.45 |\n\n### Insights Principales\n\n📈 **Crecimiento en ventas**: +11.95% ($6,240.25 adicionales)\n📊 **Más pedidos**: +13.17% (22 pedidos adicionales)\n💰 **Ticket promedio**: -1.10% (ligera disminución)\n\n### Conclusiones\n\n✅ **Positivo**: Aumento significativo en volumen y valor total\n⚠️ **Observación**: El ticket promedio bajó ligeramente, pero se compensó con mayor cantidad de pedidos\n\n¿Te gustaría profundizar en algún aspecto específico del análisis?",
  "status": "success"
}
```

### Ejemplo 3: Conversación con Contexto

**Request 1**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "¿Qué productos son más populares?"
    }
  ]
}
```

**Request 2** (con contexto):
```json
{
  "messages": [
    {
      "role": "user",
      "content": "¿Qué productos son más populares?"
    },
    {
      "role": "assistant",
      "content": "Los productos más populares por número de ventas son:\n\n1. **Laptop Pro X1** - 156 unidades vendidas\n2. **Mouse Inalámbrico** - 134 unidades vendidas\n3. **Teclado Mecánico** - 98 unidades vendidas..."
    },
    {
      "role": "user",
      "content": "¿Y cuáles generan más ingresos?"
    }
  ]
}
```

### Ejemplo 4: Manejo de Errores

**Request con error**:
```json
{
  "messages": []
}
```

**Response de error**:
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "detail": "No se encontró mensaje del usuario"
}
```

---

## 🧩 SDKs y Bibliotecas

### Python SDK

```python
import requests

class SQLAgentClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.messages = []

    def chat(self, message: str) -> str:
        """Envía un mensaje al agente y devuelve la respuesta"""
        self.messages.append({"role": "user", "content": message})

        response = self.session.post(
            f"{self.base_url}/api/v1/chat",
            json={"messages": self.messages}
        )
        response.raise_for_status()

        result = response.json()
        assistant_message = result["response"]

        # Agregar respuesta al historial
        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def clear_history(self):
        """Limpia el historial de conversación"""
        self.messages = []

    def health_check(self) -> bool:
        """Verifica el estado del servicio"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/health")
            return response.status_code == 200
        except:
            return False

# Ejemplo de uso
client = SQLAgentClient()

if client.health_check():
    response = client.chat("¿Qué tablas hay en la base de datos?")
    print(response)

    response = client.chat("Muéstrame la estructura de la tabla usuarios")
    print(response)
else:
    print("Servicio no disponible")
```

### JavaScript SDK

```javascript
class SQLAgentClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
        this.messages = [];
    }

    async chat(message) {
        this.messages.push({ role: 'user', content: message });

        const response = await fetch(`${this.baseUrl}/api/v1/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ messages: this.messages })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        const assistantMessage = result.response;

        // Agregar respuesta al historial
        this.messages.push({
            role: 'assistant',
            content: assistantMessage
        });

        return assistantMessage;
    }

    clearHistory() {
        this.messages = [];
    }

    async healthCheck() {
        try {
            const response = await fetch(`${this.baseUrl}/api/v1/health`);
            return response.ok;
        } catch {
            return false;
        }
    }
}

// Ejemplo de uso
const client = new SQLAgentClient();

async function main() {
    if (await client.healthCheck()) {
        const response1 = await client.chat('¿Qué tablas hay en la base de datos?');
        console.log(response1);

        const response2 = await client.chat('Muéstrame los productos más vendidos');
        console.log(response2);
    } else {
        console.log('Servicio no disponible');
    }
}

main();
```

### cURL Examples

```bash
#!/bin/bash
# sql_agent_client.sh

BASE_URL="http://localhost:8000"

# Función para health check
health_check() {
    curl -s "$BASE_URL/api/v1/health" | grep -q "healthy"
}

# Función para enviar mensaje
send_message() {
    local message="$1"
    curl -s -X POST "$BASE_URL/api/v1/chat" \
        -H "Content-Type: application/json" \
        -d "{\"messages\":[{\"role\":\"user\",\"content\":\"$message\"}]}" \
        | jq -r '.response'
}

# Script principal
if health_check; then
    echo "✅ Servicio disponible"

    echo "📊 Consultando tablas..."
    send_message "¿Qué tablas hay en la base de datos?"

    echo "🔍 Analizando ventas..."
    send_message "Muéstrame las ventas del último mes"
else
    echo "❌ Servicio no disponible"
    exit 1
fi
```

---

## ⚡ Rate Limiting

**Estado actual**: Sin límites de rate.

**Futuras versiones** incluirán:
- Límites por IP: 100 requests/minuto
- Límites por usuario: 1000 requests/día
- Headers de respuesta:
  ```http
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1640995200
  ```

---

## 🔗 Webhooks

**Estado actual**: No implementado.

**Futuras funcionalidades**:
- Notificaciones de consultas completadas
- Alertas de errores críticos
- Eventos de análisis automáticos

---

## 🧪 Testing

### Colección Postman

```json
{
  "info": {
    "name": "SQL Agent API",
    "description": "Colección de pruebas para SQL Agent"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/api/v1/health",
          "host": ["{{base_url}}"],
          "path": ["api", "v1", "health"]
        }
      }
    },
    {
      "name": "Simple Chat",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"messages\":[{\"role\":\"user\",\"content\":\"¿Qué tablas hay en la base de datos?\"}]}"
        },
        "url": {
          "raw": "{{base_url}}/api/v1/chat",
          "host": ["{{base_url}}"],
          "path": ["api", "v1", "chat"]
        }
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    }
  ]
}
```

### Tests con pytest

```python
import pytest
import requests

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test del endpoint de salud"""
    response = requests.get(f"{BASE_URL}/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "SQL Agent API"

def test_chat_endpoint_simple():
    """Test básico del endpoint de chat"""
    payload = {
        "messages": [
            {"role": "user", "content": "¿Qué tablas hay en la base de datos?"}
        ]
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["status"] == "success"
    assert len(data["response"]) > 0

def test_chat_endpoint_with_history():
    """Test del endpoint de chat con historial"""
    payload = {
        "messages": [
            {"role": "user", "content": "Hola"},
            {"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte?"},
            {"role": "user", "content": "¿Qué tablas hay?"}
        ]
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat", json=payload)
    assert response.status_code == 200

def test_chat_endpoint_empty_messages():
    """Test de error con mensajes vacíos"""
    payload = {"messages": []}
    response = requests.post(f"{BASE_URL}/api/v1/chat", json=payload)
    assert response.status_code == 400

def test_chat_endpoint_no_user_message():
    """Test de error sin mensaje de usuario"""
    payload = {
        "messages": [
            {"role": "system", "content": "Eres un asistente"}
        ]
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat", json=payload)
    assert response.status_code == 400

@pytest.mark.timeout(30)
def test_chat_endpoint_performance():
    """Test de rendimiento del endpoint de chat"""
    payload = {
        "messages": [
            {"role": "user", "content": "¿Qué tablas hay en la base de datos?"}
        ]
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat", json=payload)
    assert response.status_code == 200
    # La respuesta debe llegar en menos de 30 segundos
```

### Load Testing con Locust

```python
from locust import HttpUser, task, between

class SQLAgentUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Verificar que el servicio esté disponible"""
        self.client.get("/api/v1/health")

    @task(3)
    def simple_query(self):
        """Consulta simple frecuente"""
        payload = {
            "messages": [
                {"role": "user", "content": "¿Qué tablas hay en la base de datos?"}
            ]
        }
        self.client.post("/api/v1/chat", json=payload)

    @task(2)
    def complex_query(self):
        """Consulta compleja menos frecuente"""
        payload = {
            "messages": [
                {"role": "user", "content": "Analiza las ventas del último trimestre"}
            ]
        }
        self.client.post("/api/v1/chat", json=payload)

    @task(1)
    def health_check(self):
        """Health check ocasional"""
        self.client.get("/api/v1/health")
```

---

## 📚 Documentación Interactiva

### Swagger UI
Accede a la documentación interactiva en:
```
http://localhost:8000/docs
```

### ReDoc
Documentación alternativa en:
```
http://localhost:8000/redoc
```

### OpenAPI Schema
Esquema JSON disponible en:
```
http://localhost:8000/openapi.json
```

---

## 🔧 Configuración de CORS

Para uso desde frontends web, configura CORS en `.env`:

```bash
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","https://miapp.com"]
```

---

## 📝 Notas Importantes

1. **Timeouts**: Las consultas complejas pueden tomar hasta 60 segundos
2. **Límites**: El agente tiene un máximo de 5 iteraciones por consulta
3. **Seguridad**: Solo consultas SELECT están permitidas
4. **Encoding**: Siempre usar UTF-8 para caracteres especiales
5. **Historial**: El contexto se mantiene solo durante la sesión

---
