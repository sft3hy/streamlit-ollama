import streamlit as st
from config import OLLAMA_CLIENT


# Function to refresh the list of available models
def refresh_model_list():
   return [model["model"] for model in OLLAMA_CLIENT.list()["models"]]




# Initialize session state variables
if "models" not in st.session_state:
   st.session_state.models = refresh_model_list()


if "selected_model" not in st.session_state:
   st.session_state.selected_model = None


# Refresh dropdown options dynamically
def get_refreshed_model_choices():
   all_models = ["llama3.2:1B", "llama3.2:3B", "llama3.1:8B", "mistral:latest"]
   if st.session_state.models:
       # Exclude the currently running model from the dropdown
       return [model for model in all_models if model != st.session_state.models[0]]
   return all_models




# Display the currently running model
if st.session_state.models:
   st.write(f"Currently running model: {st.session_state.models[0]}")
else:
   st.write("No model is currently running.")


# Dropdown for model selection
selected_model = st.selectbox(
   label="Select a model to pull",
   options=get_refreshed_model_choices(),
   key="selected_model"
)


def unload_models():
   for mod_info in st.session_state.models:
       with st.spinner(f"Unloading {mod_info}..."):
           OLLAMA_CLIENT.delete(mod_info)


# Button to load a new model
if st.button("Load new model") and st.session_state.selected_model:
   if not st.session_state.models:
       # No model is currently loaded
       with st.spinner(f"Loading {st.session_state.selected_model} from Ollama..."):
           OLLAMA_CLIENT.pull(st.session_state.selected_model)
       st.success(
           f"Done! You can now chat with {st.session_state.selected_model} in the 'LLM Chat' page"
       )
   else:
       # Unload the currently loaded model
       unload_models()
       # Load the new model
       with st.spinner(f"Loading {st.session_state.selected_model} from Ollama..."):
           OLLAMA_CLIENT.pull(st.session_state.selected_model)
       st.success(
           f"Done! You can now chat with {st.session_state.selected_model} in the 'LLM Chat' page"
       )


   # Refresh the models list in session state
   st.session_state.models = refresh_model_list()










