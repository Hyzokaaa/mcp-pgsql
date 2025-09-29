# app/ui.py
"""
Interfaz de usuario Streamlit para el agente SQL.

Esta aplicación web proporciona una interfaz de chat intuitiva para interactuar
con el agente SQL. Los usuarios pueden hacer consultas en lenguaje natural y
recibir respuestas procesadas por el agente que incluyen análisis de base de
datos y ejecución de consultas SQL.

Características de la interfaz:
- Chat interactivo con historial persistente
- Indicadores de carga con mensajes animados
- Avatares personalizados para usuario y asistente
- Integración completa con el agente SQL
- Manejo de sesiones de Streamlit para estado persistente

La aplicación utiliza nest_asyncio para compatibilidad entre Streamlit
(síncrono) y el agente SQL (asíncrono).

Uso:
    streamlit run app/ui.py
    # o usando PDM:
    pdm run ui
"""

import streamlit as st
import asyncio
import random
from dotenv import load_dotenv
import nest_asyncio

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from app.agent.agent import ask, create_history
from app.agent.models import create_llm
from app.agent.tools import load_tools
from app.core.config import Config

# === CONFIGURACIÓN INICIAL ===

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Aplicar nest_asyncio para permitir bucles de eventos anidados
# Necesario para ejecutar código asíncrono dentro de Streamlit
nest_asyncio.apply()

# Configurar página de Streamlit con metadatos
st.set_page_config(
    page_title="SEPSA ORACLE Assistant",  # Título en la pestaña del navegador
    page_icon="🖤",                       # Ícono en la pestaña del navegador
    layout="centered"                     # Layout centrado para mejor UX
)

# === CONFIGURACIÓN DE INTERFAZ ===

# Mensajes de carga que se muestran aleatoriamente durante el procesamiento
LOADING_MESSAGES = [
    "Preparando tus tareas...",
    "Generando nuevas respuestas...",
    "Adaptando simulación..."
]

# === INICIALIZACIÓN DE ESTADO DE SESIÓN ===

# Inicializar modelo de lenguaje si no existe en la sesión
# Se mantiene en session_state para evitar reinicializaciones costosas
if "llm" not in st.session_state:
    st.session_state.llm = create_llm(Config.MODEL)

# Inicializar herramientas SQL si no existen en la sesión
if "tools" not in st.session_state:
    st.session_state.tools = load_tools()

# Inicializar historial de mensajes vacío si no existe
if "messages" not in st.session_state:
    st.session_state.messages = create_history()

# === RENDERIZADO DEL HISTORIAL DE CHAT ===

# Mostrar todos los mensajes previos en la interfaz de chat
for message in st.session_state.messages:
    # Omitir mensajes del sistema (no relevantes para el usuario)
    if isinstance(message, SystemMessage):
        continue

    # Determinar si el mensaje es del usuario o del asistente
    is_user = isinstance(message, HumanMessage)
    avatar = "😿" if is_user else "🎙️"

    # Renderizar mensaje con avatar apropiado
    with st.chat_message("user" if is_user else "ai", avatar=avatar):
        st.markdown(message.content)

# === MANEJO DE ENTRADA DEL USUARIO ===

# Input de chat con placeholder descriptivo
if prompt := st.chat_input("¿Qué consulta SQL quieres hacer hoy?"):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append(HumanMessage(content=prompt))

    # Mostrar mensaje del usuario inmediatamente
    with st.chat_message("user", avatar="😿"):
        st.markdown(prompt)

    # Procesar respuesta del agente
    with st.chat_message("ai", avatar="🎙️"):
        # Crear placeholder para mostrar estado de carga
        message_placeholder = st.empty()
        message_placeholder.status(
            random.choice(LOADING_MESSAGES),
            state="running"
        )

        # Vincular herramientas al modelo para habilitar tool calling
        llm_with_tools = st.session_state.llm.bind_tools(st.session_state.tools)

        # Ejecutar consulta usando el agente SQL de forma asíncrona
        # asyncio.run() es necesario para ejecutar código async en Streamlit
        response = asyncio.run(
            ask(
                query=prompt,                           # Consulta del usuario
                history=st.session_state.messages,     # Historial de conversación
                llm=llm_with_tools,                     # Modelo con herramientas
                available_tools=st.session_state.tools # Herramientas disponibles
            )
        )

        # Reemplazar indicador de carga con la respuesta real
        message_placeholder.markdown(response)

        # Agregar respuesta del agente al historial para futura referencia
        st.session_state.messages.append(AIMessage(content=response))
