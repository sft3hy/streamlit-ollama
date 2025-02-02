import streamlit as st


client_creation = """
from ollama import Client
client = Client(
 host='http://172.30.11.204:11434',
)
"""


models = """
models = [model["model"] for model in client.list()["models"]]
print(models)
"""


model_call = """
response = client.chat(model='llama3.2', messages=[
 {
   'role': 'user',
   'content': 'Why is the sky blue?',
   'stream': True,
 },
])


"""




st.write("Create an Ollama client:")
st.code(client_creation, language="python")


st.write("Get a list of models currently running on the Ollama server:")
st.code(models, language="python")


st.write("Get a streaming object of the chat response:")
st.code(model_call, language="python")








