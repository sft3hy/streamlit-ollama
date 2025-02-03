import ollama
import streamlit as st
import os

local = os.getenv("SAM_COMPUTER")
if local == 'True':
    HOST = 'http://localhost:11434'
else:
    HOST = 'http://172.30.11.204:30001'

OLLAMA_CLIENT = ollama.Client(
    host='http://localhost:11434'
)

def refresh_model_list():
   return [model["model"] for model in OLLAMA_CLIENT.list()["models"]]

def unload_models():
   for mod_info in refresh_model_list():
       with st.spinner(f"Unloading {mod_info}..."):
           OLLAMA_CLIENT.delete(mod_info)