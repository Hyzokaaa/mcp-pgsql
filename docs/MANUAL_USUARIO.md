# Manual de Usuario - SQL Agent

## 🚀 Bienvenido a SQL Agent

SQL Agent es tu asistente inteligente para bases de datos que te permite hacer consultas en **lenguaje natural** y obtener resultados precisos sin necesidad de conocer SQL.

---

## 📋 Tabla de Contenidos

1. [¿Qué es SQL Agent?](#qué-es-sql-agent)
2. [Primeros Pasos](#primeros-pasos)
3. [Interfaces Disponibles](#interfaces-disponibles)
4. [Cómo Hacer Consultas](#cómo-hacer-consultas)
5. [Ejemplos Prácticos](#ejemplos-prácticos)
6. [Características Avanzadas](#características-avanzadas)
7. [Resolución de Problemas](#resolución-de-problemas)
8. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🤖 ¿Qué es SQL Agent?

SQL Agent es un **asistente conversacional inteligente** que te ayuda a:

- ✅ **Explorar bases de datos** sin conocer su estructura
- ✅ **Hacer consultas en español** como si hablaras con un experto
- ✅ **Obtener insights automáticos** sobre tus datos
- ✅ **Generar reportes** de manera intuitiva
- ✅ **Analizar tendencias** con explicaciones claras

### ¿Para quién es?
- 📊 **Analistas de datos** que necesitan consultas rápidas
- 👔 **Gerentes y directivos** que requieren reportes ejecutivos
- 🔍 **Investigadores** que exploran datos
- 💼 **Equipos de negocio** sin conocimientos técnicos

---

## 🏁 Primeros Pasos

### Verificar que el Servicio Esté Activo

Antes de usar SQL Agent, asegúrate de que esté funcionando:

```bash
# Verificar estado del servicio
curl http://localhost:8000/api/v1/health
```

**Respuesta esperada**:
```json
{
  "status": "healthy",
  "service": "SQL Agent API"
}
```

### Acceder a la Documentación

Una vez que el servicio esté activo, puedes acceder a:
- **📚 Documentación interactiva**: http://localhost:8000/docs
- **🔍 Explorador de API**: http://localhost:8000/redoc

---

## 💻 Interfaces Disponibles

### 1. 🌐 Interfaz Web (Streamlit) - **Recomendada**

La forma más fácil de usar SQL Agent es a través de la interfaz web:

**Acceso**: Ejecutar `pdm run ui` y abrir http://localhost:8501

**Características**:
- ✨ Chat interactivo en tiempo real
- 📱 Interfaz intuitiva y amigable
- 💾 Historial de conversaciones persistente
- 🎯 Sin configuración adicional necesaria

**Ideal para**: Usuarios que prefieren interfaces gráficas

### 2. 🔌 API REST

Para desarrolladores e integraciones:

**Acceso**: http://localhost:8000/api/v1/chat

**Ejemplo de uso**:
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "messages": [
    {
      "role": "user",
      "content": "Muéstrame las ventas del último mes"
    }
  ]
}'
```

**Ideal para**: Desarrolladores, automatización, integraciones

### 3. 💻 Cliente Directo (Línea de Comandos)

Para uso programático directo:

**Acceso**: `pdm run direct`

**Ideal para**: Scripts automatizados, pruebas rápidas

---

## 💬 Cómo Hacer Consultas

### Principios Básicos

SQL Agent entiende **lenguaje natural en español**. Puedes hacer preguntas como si estuvieras hablando con un experto en bases de datos:

### ✅ Ejemplos de Consultas Efectivas

#### 🔍 **Exploración Inicial**
```
"¿Qué tablas hay en la base de datos?"
"Muéstrame la estructura de la tabla usuarios"
"¿Cuántos registros tiene la tabla ventas?"
```

#### 📊 **Análisis de Datos**
```
"¿Cuáles son los productos más vendidos este año?"
"Muéstrame las ventas por mes de los últimos 6 meses"
"¿Qué clientes han gastado más de $1000?"
```

#### 🎯 **Consultas Específicas**
```
"Dame los empleados contratados en 2023"
"¿Cuál es el promedio de edad de nuestros clientes?"
"Muéstrame los pedidos pendientes de entrega"
```

#### 📈 **Análisis Avanzado**
```
"Compara las ventas de este año vs el año pasado"
"¿Qué productos tienen mejor margen de ganancia?"
"Identifica clientes que no han comprado en los últimos 3 meses"
```

### 🚫 Limitaciones de Seguridad

Por seguridad, SQL Agent **SOLO puede leer datos**:

- ✅ **Permitido**: SELECT, consultas de lectura
- ❌ **Bloqueado**: INSERT, UPDATE, DELETE, DROP

Esto garantiza que tus datos estén seguros.

---

## 📚 Ejemplos Prácticos

### Ejemplo 1: Exploración de Base de Datos

**🎯 Objetivo**: Entender qué datos tenemos disponibles

**Conversación**:
```
👤 Usuario: "Hola, no conozco esta base de datos. ¿Puedes ayudarme a explorarla?"

🤖 SQL Agent: "¡Por supuesto! Te ayudo a explorar la base de datos.
Primero voy a ver qué tablas están disponibles..."

[El agente lista las tablas disponibles]

🤖 SQL Agent: "Encontré las siguientes tablas:
- usuarios (información de clientes)
- productos (catálogo de productos)
- pedidos (órdenes de compra)
- detalle_pedidos (items específicos)

¿Te interesa alguna tabla en particular?"

👤 Usuario: "Cuéntame sobre la tabla de pedidos"

🤖 SQL Agent: "La tabla 'pedidos' tiene la siguiente estructura:
- id_pedido (identificador único)
- id_usuario (referencia al cliente)
- fecha_pedido (cuándo se realizó)
- total (monto total)
- estado (pendiente/completado/cancelado)

¿Quieres ver algunos ejemplos de datos?"
```

### Ejemplo 2: Análisis de Ventas

**🎯 Objetivo**: Generar reporte de ventas mensuales

**Conversación**:
```
👤 Usuario: "Necesito un reporte de ventas mensuales para el último trimestre"

🤖 SQL Agent: "Te voy a generar un reporte de ventas mensuales para el último trimestre.
Primero voy a explorar los datos disponibles..."

[El agente analiza la estructura y genera la consulta]

🤖 SQL Agent: "Aquí está el reporte de ventas del último trimestre:

| Mes        | Total Ventas | Número Pedidos | Promedio por Pedido |
|------------|--------------|----------------|---------------------|
| Octubre    | $45,230.50   | 156           | $289.94             |
| Noviembre  | $52,180.75   | 178           | $293.15             |
| Diciembre  | $61,445.20   | 201           | $305.70             |

**Insights principales:**
📈 Crecimiento constante: +35.8% de octubre a diciembre
🛒 Más pedidos: Incremento del 28.8% en volumen
💰 Mayor valor promedio: Los clientes gastan más por pedido

¿Te interesa algún análisis adicional sobre estos datos?"
```

### Ejemplo 3: Identificación de Patrones

**🎯 Objetivo**: Encontrar clientes VIP

**Conversación**:
```
👤 Usuario: "¿Quiénes son nuestros mejores clientes?"

🤖 SQL Agent: "Voy a analizar los datos para identificar a tus mejores clientes
basándome en diferentes criterios..."

[El agente realiza múltiples consultas]

🤖 SQL Agent: "He identificado a tus mejores clientes usando varios criterios:

**Top 5 por Monto Total Gastado:**
1. María García - $15,450.80 (28 pedidos)
2. Carlos López - $12,330.50 (22 pedidos)
3. Ana Martínez - $11,890.25 (31 pedidos)
4. Juan Rodríguez - $10,550.75 (19 pedidos)
5. Elena Sánchez - $9,780.40 (24 pedidos)

**Características de los clientes VIP:**
🏆 Compran en promedio cada 2.5 semanas
💎 Ticket promedio: $420 (vs $280 general)
⭐ Tasa de devolución: 2.1% (vs 8.3% general)
📅 Cliente desde hace: 2.8 años promedio

¿Quieres que analice algún segmento específico?"
```

---

## 🚀 Características Avanzadas

### 1. 🧠 Análisis Contextual

SQL Agent no solo ejecuta consultas, sino que **entiende el contexto**:

```
👤 Usuario: "¿Cómo van las ventas?"
🤖 SQL Agent: [Analiza tendencias, compara períodos, identifica patrones]

👤 Usuario: "¿Y el mes pasado?"
🤖 SQL Agent: [Recuerda el contexto y compara con el mes anterior]
```

### 2. 📊 Generación Automática de Insights

El agente proporciona análisis automáticos:

- 📈 **Tendencias**: "Las ventas crecieron 15% respecto al mes anterior"
- 🎯 **Patrones**: "Los martes son los días de mayor actividad"
- ⚠️ **Alertas**: "Hay 23 pedidos pendientes desde hace más de 7 días"

### 3. 🔄 Consultas Iterativas

Puedes refinar tus consultas progresivamente:

```
👤 "Muéstrame las ventas"
🤖 [Muestra ventas generales]

👤 "Solo de este año"
🤖 [Filtra por año actual]

👤 "Agrupadas por mes"
🤖 [Agrupa por mes]

👤 "Incluye comparación con el año pasado"
🤖 [Añade comparación temporal]
```

### 4. 🎨 Formato Inteligente

Los resultados se presentan de forma clara:

- 📋 **Tablas**: Para datos estructurados
- 📊 **Listas**: Para rankings y categorías
- 💰 **Números**: Formateados con monedas y porcentajes
- 📅 **Fechas**: En formato legible

---

## 🛠️ Resolución de Problemas

### Problema: "No se puede conectar al servicio"

**Síntomas**: Error de conexión o timeout

**Solución**:
1. Verificar que el servicio esté activo:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```
2. Si no responde, reiniciar el servicio:
   ```bash
   python start_api.py
   ```

### Problema: "El agente no entiende mi pregunta"

**Síntomas**: Respuestas irrelevantes o errores

**Solución**:
1. **Sé más específico**:
   - ❌ "Dame datos"
   - ✅ "Muéstrame las ventas del último mes"

2. **Usa nombres exactos**:
   - ❌ "tabla de clientes"
   - ✅ "tabla usuarios" (si ese es el nombre real)

3. **Pregunta sobre la estructura primero**:
   ```
   "¿Qué tablas hay disponibles?"
   "¿Cómo se llaman las columnas de la tabla X?"
   ```

### Problema: "Respuestas muy lentas"

**Síntomas**: El agente tarda mucho en responder

**Solución**:
1. **Consultas más específicas**: Evita preguntas muy amplias
2. **Verificar recursos**: El modelo LLM puede necesitar más memoria
3. **Simplificar**: Hacer preguntas una a la vez

### Problema: "Error de base de datos"

**Síntomas**: Mensajes de error de conexión DB

**Solución**:
1. Verificar configuración en `.env`
2. Comprobar que la base de datos esté accesible
3. Validar credenciales y permisos

---

## ❓ Preguntas Frecuentes

### ¿Puede SQL Agent modificar mis datos?

**No**. Por seguridad, SQL Agent **solo puede leer datos**. No puede:
- Insertar nuevos registros
- Modificar datos existentes
- Eliminar información
- Cambiar la estructura de la base de datos

### ¿Qué tipos de consultas puedo hacer?

Puedes hacer cualquier tipo de **consulta de lectura**:
- Listados y reportes
- Agregaciones (sumas, promedios, conteos)
- Filtros y búsquedas
- Análisis comparativos
- Identificación de patrones

### ¿SQL Agent recuerda conversaciones anteriores?

- **Interfaz Web**: Sí, mantiene el historial durante la sesión
- **API REST**: Debes enviar el historial en cada llamada
- **Cliente directo**: Solo durante la ejecución actual

### ¿Puedo usar SQL Agent con diferentes bases de datos?

Actualmente soporta:
- ✅ **PostgreSQL**
- ✅ **Oracle Database**

### ¿Qué pasa si hago una pregunta sobre datos que no existen?

SQL Agent te informará amablemente:
```
🤖 "No encontré una tabla llamada 'ventas_2025' en la base de datos.
Las tablas disponibles son: ventas, productos, usuarios..."
```

### ¿Puedo exportar los resultados?

Actualmente los resultados se muestran en la interfaz. Puedes:
- Copiar y pegar las tablas generadas
- Usar la API para obtener datos en JSON
- Solicitar consultas SQL específicas para usar en otras herramientas

### ¿Es seguro proporcionar acceso a mi base de datos?

Sí, SQL Agent implementa múltiples capas de seguridad:
- Solo consultas SELECT permitidas
- Validación estricta de comandos SQL
- Sin acceso a funciones administrativas
- Logging completo de todas las operaciones

### ¿Qué modelos de IA utiliza?

SQL Agent utiliza modelos locales a través de Ollama:
- **QWEN3**: Optimizado para tool calling
- **LLAMA**: Balance entre rendimiento y precisión
- **Ventaja**: Tus datos nunca salen de tu infraestructura

---

## 💡 Consejos para Mejores Resultados

### 🎯 Sé Específico
```
❌ "Dame información de ventas"
✅ "Muéstrame las ventas por producto del último trimestre"
```

### 📅 Incluye Contexto Temporal
```
❌ "¿Cuáles son los mejores productos?"
✅ "¿Cuáles son los productos más vendidos este año?"
```

### 🔍 Explora Antes de Analizar
```
1. "¿Qué tablas hay?"
2. "Muéstrame la estructura de la tabla ventas"
3. "Dame una muestra de datos"
4. "Ahora analiza las tendencias"
```

### 💬 Usa Lenguaje Natural
```
✅ "¿Qué clientes compraron más de $500 el mes pasado?"
✅ "Muéstrame los empleados contratados este año"
✅ "¿Cuál es el producto más popular por región?"
```

---

## 🎓 Ejemplos de Casos de Uso

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

### 🔍 Para Investigadores
```
"Explora patrones anómalos en los datos de usuarios"
"¿Qué factores influyen en la retención de clientes?"
"Analiza la distribución geográfica de nuestras ventas"
```

### 💼 Para Equipos de Negocio
```
"¿Cuántos nuevos clientes adquirimos este mes?"
"Muéstrame el inventario actual de productos"
"¿Qué pedidos están pendientes de entrega?"
```

---

## 📞 Soporte y Contacto

Si tienes problemas o sugerencias:

1. **Revisa este manual** para soluciones comunes
2. **Consulta la documentación técnica** para detalles avanzados
3. **Verifica los logs** del sistema para mensajes de error específicos

---
