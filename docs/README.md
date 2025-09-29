# Documentación SQL Agent

Bienvenido a la documentación completa de **SQL Agent**, tu asistente inteligente para bases de datos que permite realizar consultas en lenguaje natural.

## 📚 Documentos Disponibles

### 👥 Para Usuarios
- **[Manual de Usuario](MANUAL_USUARIO.md)** - Guía completa para usar SQL Agent
  - Cómo hacer consultas en lenguaje natural
  - Ejemplos prácticos de uso
  - Interfaces disponibles (Web, API, Terminal)
  - Resolución de problemas comunes

### 🔧 Para Administradores
- **[Guía de Instalación](GUIA_INSTALACION.md)** - Configuración paso a paso
  - Instalación en desarrollo y producción
  - Configuración de bases de datos
  - Setup de Ollama y modelos LLM
  - Docker y docker-compose
  - Configuración avanzada y monitoreo

### 👨‍💻 Para Desarrolladores
- **[Documentación Técnica](DOCUMENTACION_TECNICA.md)** - Arquitectura y componentes
  - Arquitectura del sistema
  - Módulos y componentes detallados
  - Características de seguridad
  - Extensibilidad y desarrollo

- **[Referencia de API](API_REFERENCE.md)** - Documentación completa de la API REST
  - Endpoints y parámetros
  - Ejemplos de requests/responses
  - SDKs en Python y JavaScript
  - Testing y colecciones Postman

## 🚀 Inicio Rápido

### 1. Instalación Básica
```bash
# Clonar repositorio
git clone <repository>
cd mcp-pgsql

# Configurar entorno
cp .env.example .env
# Editar .env con tu configuración

# Instalar dependencias
pdm install

# Iniciar servicio
python start_api.py
```

### 2. Verificar Instalación
```bash
curl http://localhost:8000/api/v1/health
```

### 3. Usar Interfaz Web
```bash
pdm run ui
# Abrir http://localhost:8501
```

## 🎯 ¿Qué es SQL Agent?

SQL Agent es un **asistente conversacional inteligente** que:

✅ **Convierte lenguaje natural en SQL** - "¿Cuáles son las ventas del último mes?" → consulta SQL optimizada

✅ **Explora bases de datos automáticamente** - Descubre tablas, esquemas y relaciones sin conocimiento previo

✅ **Proporciona insights automáticos** - No solo datos, sino análisis y conclusiones

✅ **Mantiene conversaciones contextuales** - Recuerda el hilo de la conversación

✅ **Es seguro por diseño** - Solo consultas de lectura, validación estricta

## 🏗️ Arquitectura

```
Frontend (Streamlit/API) → Agente SQL → Herramientas → Base de Datos
                             ↓
                        Modelo LLM (Ollama)
```

## 🛠️ Tecnologías

- **Backend**: Python, FastAPI, SQLAlchemy
- **IA**: Ollama (modelos locales), LangChain
- **Bases de Datos**: PostgreSQL, Oracle
- **Frontend**: Streamlit
- **Seguridad**: Validación SQL, solo lectura

## 📖 Casos de Uso

### 👔 Para Gerentes
```
"Dame un resumen ejecutivo de ventas del último trimestre"
"¿Cuáles son nuestros productos con mejor rendimiento?"
"Identifica oportunidades de crecimiento en nuestros datos"
```

### 📊 Para Analistas
```
"Analiza la estacionalidad en las ventas"
"¿Hay correlación entre el día de la semana y las ventas?"
"Segmenta nuestros clientes por comportamiento de compra"
```

### 💼 Para Equipos de Negocio
```
"¿Cuántos nuevos clientes adquirimos este mes?"
"Muéstrame el inventario actual de productos"
"¿Qué pedidos están pendientes de entrega?"
```

## 🔐 Seguridad

SQL Agent implementa múltiples capas de seguridad:

- **Solo lectura**: Únicamente consultas SELECT permitidas
- **Validación SQL**: Análisis sintáctico con SQLparse
- **Sin privilegios administrativos**: Acceso limitado a datos de usuario
- **Logging completo**: Registro de todas las operaciones
- **Datos locales**: Los modelos LLM ejecutan localmente

## 🌟 Características Destacadas

### 🧠 Inteligencia Contextual
- Comprende el contexto de conversaciones anteriores
- Genera consultas SQL optimizadas automáticamente
- Proporciona explicaciones en español claro

### 🔍 Exploración Automática
- Descubre la estructura de bases de datos desconocidas
- Identifica relaciones entre tablas
- Sugiere consultas relevantes

### 📊 Análisis Inteligente
- Calcula automáticamente métricas importantes
- Identifica tendencias y patrones
- Compara períodos temporales

### 🚀 Múltiples Interfaces
- **Web UI**: Interfaz de chat intuitiva
- **API REST**: Integración programática
- **Terminal**: Acceso directo por línea de comandos

## 📋 Requisitos del Sistema

### Mínimos
- Python 3.11+
- 4GB RAM
- Ollama instalado
- Base de datos accesible

### Recomendados
- Python 3.12+
- 8GB RAM
- SSD para mejor rendimiento
- GPU para modelos grandes (opcional)

## 🆘 Soporte

### Documentación
1. Revisar este índice para encontrar la guía apropiada
2. Consultar ejemplos en cada documento
3. Verificar sección de troubleshooting

### Recursos Adicionales
- **Logs del sistema**: Información detallada de errores
- **Documentación de Ollama**: https://ollama.com/docs
- **SQLAlchemy Docs**: Para configuración avanzada de DB

## 🔄 Actualizaciones

Para mantener SQL Agent actualizado:

```bash
git pull origin main
pdm update
sudo systemctl restart sql-agent  # si está configurado como servicio
```

## 🎯 Roadmap

### Próximas Características
- [ ] Autenticación y autorización
- [ ] Soporte para múltiples bases de datos simultáneas
- [ ] Cache inteligente de consultas
- [ ] Exportación de resultados (Excel, CSV, PDF)
- [ ] Dashboard de analytics
- [ ] Integración con herramientas de BI

### Mejoras Planificadas
- [ ] Modelos LLM más especializados
- [ ] Optimización de rendimiento
- [ ] Interfaz móvil
- [ ] Alertas automáticas
- [ ] Reportes programados
