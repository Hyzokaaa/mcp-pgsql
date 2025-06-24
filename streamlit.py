import asyncio
import random

import nest_asyncio
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import streamlit as st
from agent import ask, create_history
from client_config import connect_to_server
from config import Config
from models import create_llm
from tools import load_tools

load_dotenv()

LOADING_MESSAGES = [
    "Preparando tus tareas...",
    "Generando nuevas respuestas...",
    "Adaptando simulación"
]

async def get_response_async(user_query: str, history: list, llm):
    async with connect_to_server() as session:
        tools = await load_tools(session)
        llm_with_tools = llm.bind_tools(tools)
        response_content = await ask(user_query, history.copy(), llm_with_tools, tools)
        return response_content

nest_asyncio.apply()

st.set_page_config(
    page_title="Tareitas",
    page_icon="🖤",
    layout="centered"
)

st.title("SEPSA ORACLE Assistant")
st.subheader("Consulta el data warehouse utilizando inteligencia artificial")

if "llm" not in st.session_state:
    st.session_state.llm = create_llm(Config.MODEL)

if "messages" not in st.session_state:
    st.session_state.messages = create_history()

for message in st.session_state.messages:
    if type(message) is SystemMessage:
        continue
    is_user = type(message) is HumanMessage
    avatar = "😿" if is_user else "🎙️"
    with st.chat_message("user" if is_user else "ai", avatar=avatar):
        st.markdown(message.content)

if prompt := st.chat_input("¿Qué consulta SQL quieres hacer hoy?"):
    st.session_state.messages.append(HumanMessage(prompt))
    with st.chat_message("human", avatar="😿"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🎙️"):
        message_placeholder = st.empty()
        message_placeholder.status(random.choice(LOADING_MESSAGES), state= "running")

        response = asyncio.run(
            get_response_async(prompt, st.session_state.messages, st.session_state.llm)
        )
        message_placeholder.markdown(response)
        st.session_state.messages.append(AIMessage(response))
