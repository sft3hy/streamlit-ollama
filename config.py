import ollama
import streamlit as st

OLLAMA_CLIENT = ollama.Client(
    host='http://172.30.11.204:30001'
)

def refresh_model_list():
   return [model["model"] for model in OLLAMA_CLIENT.list()["models"]]

def unload_models():
   for mod_info in refresh_model_list():
       with st.spinner(f"Unloading {mod_info}..."):
           OLLAMA_CLIENT.delete(mod_info)