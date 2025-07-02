# API Examples

## Ejemplos de uso de la API SQL Agent

### Configuración CORS para React

Para agregar orígenes, configura la variable de entorno `CORS_ORIGINS`:

```bash
CORS_ORIGINS=["http://localhost:3000","https://miapp.com","https://otro-dominio.com"]
```

### 1. Health Check

```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

### 2. Chat Simple

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

### 3. Chat con Historial

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Lista las tablas"
      },
      {
        "role": "assistant",
        "content": "Las tablas disponibles son: users, orders, products"
      },
      {
        "role": "user",
        "content": "Describe la estructura de la tabla users"
      }
    ]
  }'
```

### 4. Consulta SQL específica

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Ejecuta SELECT * FROM users LIMIT 5 y explícame los resultados"
      }
    ]
  }'
```

## Formato de Response

### Respuesta exitosa:

```json
{
  "response": "Aquí está la respuesta del agente...",
  "status": "success"
}
```

### Respuesta de error:

```json
{
  "detail": "Error procesando consulta: mensaje de error"
}
```

## Swagger/OpenAPI

Una vez que la API esté ejecutándose, puedes acceder a la documentación interactiva en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
