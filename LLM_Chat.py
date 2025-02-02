import streamlit as st
import ollama
from typing import Dict, Generator
from config import OLLAMA_CLIENT




def ollama_generator(model_name: str, messages: Dict) -> Generator:
   stream = OLLAMA_CLIENT.chat(
       model=model_name, messages=messages, stream=True)
   for chunk in stream:
       yield chunk['message']['content']


models = [model["model"] for model in OLLAMA_CLIENT.list()["models"]]


if "selected_model" not in st.session_state:
   st.session_state.selected_model = ""
if "messages" not in st.session_state:
   st.session_state.messages = []
st.session_state.selected_model = models[0]
st.write(f"Chatting with {models[0]}")


for message in st.session_state.messages:
   with st.chat_message(message["role"]):
       st.markdown(message["content"])


if prompt := st.chat_input("Ask me anything"):
   # Add user message to chat history
   st.session_state.messages.append({"role": "user", "content": prompt})
   # Display user message in chat message container
   with st.chat_message("user"):
       st.markdown(prompt)


   with st.chat_message("assistant"):
       response = st.write_stream(ollama_generator(
           st.session_state.selected_model, st.session_state.messages))
   st.session_state.messages.append(
       {"role": "assistant", "content": response})








