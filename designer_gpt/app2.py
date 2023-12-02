import asyncio
import queue
import threading
import time

import nest_asyncio
from dotenv import load_dotenv
from pyee.base import EventEmitter

load_dotenv()


nest_asyncio.apply()


import os

import streamlit as st
from agents.trackable_agent import TrackableAssistantAgent, TrackableUserProxyAgent

llm_config = {
    "timeout": 600,
    "config_list": [
        {
            "model": "gpt-4",
            "api_key": os.environ["OPENAI_API_KEY"],
        }
    ],
}


emitter = EventEmitter()

queue = asyncio.Queue()

assistant = TrackableAssistantAgent(
    emitter,
    queue,
    name="assistant",
    llm_config=llm_config,
)
user_proxy = TrackableUserProxyAgent(
    emitter,
    queue,
    name="user",
    human_input_mode="ALWAYS",
    llm_config=llm_config,
)


st.title("Designer GPT")
st.markdown(
    "This is a demo of the Designer GPT app. You can type in the box below to chat with the AI."
)


user_input = st.chat_input("Type something...")


def handle_message(inp):
    sender, message = inp
    with st.chat_message(sender):
        st.write(message)


def get_human_input(prompt: str):
    st.write(prompt)
    with st.form("human_input"):
        st.write(prompt)
        human_input = st.text_input("Type something...")
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            queue.put_nowait(human_input)


emitter.on("message", handle_message)

emitter.on("test", lambda prompt: print("Test event:", prompt))
emitter.on("get_human_input", get_human_input)


if user_input:
    # Define an asynchronous function
    async def initiate_chat2():
        await user_proxy.a_initiate_chat(
            assistant,
            message=user_input,
        )

    def initiate_chat():
        user_proxy.initiate_chat(
            assistant,
            message=user_input,
        )

    # asyncio.run(initiate_chat2())
    initiate_chat()

    # Create a thread

    # chat_thread = threading.Thread(target=initiate_chat)
    # chat_thread.start()


#     # Create a thread
#     chat_thread = threading.Thread(target=initiate_chat)
#     chat_thread.start()

#     while True:
#         print("Waiting for output...")
#         if not output_queue.empty():
#             op, data = output_queue.get()
#             if op == "message":
#                 sender, message = data
#                 with st.chat_message(sender):
#                     st.write(message)
#             elif op == "get_human_input":
#                 prompt = data
#                 with st.form("human_input"):
#                     st.write(prompt)
#                     human_input = st.text_input("Type something...")
#                     submit_button = st.form_submit_button("Submit")
#                     if submit_button:
#                         input_queue.put(human_input)
#                         break
