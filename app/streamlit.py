import asyncio
import random
from dotenv import load_dotenv
import nest_asyncio

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from app.agent.agent import ask, create_history
from app.agent.models import create_llm
from app.agent.tools import load_tools
from app.core.config import Config


# --- Carga de entorno y configuración ---
load_dotenv()
nest_asyncio.apply()

st.set_page_config(
    page_title="SEPSA ORACLE Assistant",
    page_icon="🖤",
    layout="centered"
)

# Mensajes de carga animada
LOADING_MESSAGES = [
    "Preparando tus tareas...",
    "Generando nuevas respuestas...",
    "Adaptando simulación..."
]

# --- Inicializar estado ---
if "llm" not in st.session_state:
    st.session_state.llm = create_llm(Config.MODEL)

if "tools" not in st.session_state:
    st.session_state.tools = load_tools()

if "messages" not in st.session_state:
    st.session_state.messages = create_history()


# --- Mostrar historial ---
for message in st.session_state.messages:
    if isinstance(message, SystemMessage):
        continue
    is_user = isinstance(message, HumanMessage)
    avatar = "😿" if is_user else "🎙️"
    with st.chat_message("user" if is_user else "ai", avatar=avatar):
        st.markdown(message.content)


# --- Entrada del usuario ---
if prompt := st.chat_input("¿Qué consulta SQL quieres hacer hoy?"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user", avatar="😿"):
        st.markdown(prompt)

    with st.chat_message("ai", avatar="🎙️"):
        message_placeholder = st.empty()
        message_placeholder.status(random.choice(LOADING_MESSAGES), state="running")

        # Vincular LLM con herramientas
        llm_with_tools = st.session_state.llm.bind_tools(st.session_state.tools)

        # Ejecutar consulta con el agente
        response = asyncio.run(
            ask(
                query=prompt,
                history=st.session_state.messages,
                llm=llm_with_tools,
                available_tools=st.session_state.tools,
            )
        )

        message_placeholder.markdown(response)
        st.session_state.messages.append(AIMessage(content=response))
