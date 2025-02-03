import streamlit as st
import ollama
from typing import Dict, Generator
from config import OLLAMA_CLIENT, refresh_model_list, unload_models
import time


def ollama_generator(model_name: str, messages: Dict) -> Generator:
   stream = OLLAMA_CLIENT.chat(
       model=model_name, messages=messages, stream=True)
   for chunk in stream:
       yield chunk['message']['content']


models = refresh_model_list()
print(models)
if models == []:
    with st.spinner("Loading llama3.2:1B..."):
        OLLAMA_CLIENT.pull("llama3.2:1B")
    time.sleep(1)


if "selected_model" not in st.session_state:
   st.session_state.selected_model = ""
if "messages" not in st.session_state:
    st.session_state.messages = []


st.session_state.selected_model = refresh_model_list()[0]

if models != []:
    st.write(f"Chatting with {st.session_state.selected_model}")

    for message in st.session_state.messages:
        if message is not None:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


    if prompt := st.chat_input("Ask me anything"):
        # Add user message to chat history
        if prompt is not None:
            st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
            with st.chat_message("user"):
                if prompt is not None:
                    st.markdown(prompt)


            with st.chat_message("assistant"):
                response = st.write_stream(ollama_generator(
                    st.session_state.selected_model, st.session_state.messages))
            if response is not None:
                st.session_state.messages.append(
                    {"role": "assistant", "content": response})

else:
    st.write("""No model loaded, please refresh the page""")


with st.sidebar:
    model_options = ["llama3.2:1B", "llama3.2:3B", "llama3.1:8B", "mistral:latest"]
    print('SELECTED MODEL', st.session_state.selected_model)
    if st.session_state.selected_model in model_options:
        model_options.remove(st.session_state.selected_model)

    # Dropdown for model selection
    new_model = st.selectbox(
        label="Select a model to load",
        options=model_options,
        key="new_model"
    )


    # Button to load a new model
    if st.button("Load new model") and new_model:
        # Unload the currently loaded model
        with st.spinner("Unloading model..."):
            unload_models()
            time.sleep(0.2)
        # Load the new model
        with st.spinner(f"Loading {new_model} from Ollama..."):
            OLLAMA_CLIENT.pull(new_model)
        st.success(
            f"Done! You can now chat with {new_model}"
        )

        # Refresh the models list in session state
        st.session_state.selected_model = new_model
