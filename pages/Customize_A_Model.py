import streamlit as st
import ollama
from config import OLLAMA_CLIENT, refresh_model_list, unload_models
import time

st.title("Create a Custom Model")

models = refresh_model_list()

# if models == []:
#     with st.spinner("Loading llama3.2:1B..."):
#         OLLAMA_CLIENT.pull("llama3.2:1B")
st.write("Note: all fields except model name are optional")

all_models = ["llama3.2:1B", "llama3.2:3B", "llama3.1:8B", "mistral:latest"]

selected_model = st.selectbox(
   label="Select a base model",
   options=all_models,
   key="base_model"
)

# Define fields with label, key, type, min_value, max_value, step, default, and help text
fields = [
    ("Enable Mirostat:", "mirostat", int, 0, 2, 1, 0, "Enable Mirostat sampling for controlling perplexity. (default: 0, 0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0)"),
    ("Mirostat Eta:", "mirostat_eta", float, 0.0, 1.0, 0.01, 0.1, "Influences how quickly the algorithm responds to feedback from the generated text. (Default: 0.1)"),
    ("Mirostat Tau:", "mirostat_tau", float, 0.0, 10.0, 0.1, 5.0, "Controls the balance between coherence and diversity of the output. (Default: 5.0)"),
    ("Context Window Size:", "num_ctx", int, 1, 8192, 1, 2048, "Sets the size of the context window used to generate the next token. (Default: 2048)"),
    ("Repeat Last N:", "repeat_last_n", int, -1, 8192, 1, 64, "Sets how far back for the model to look back to prevent repetition. (Default: 64, 0 = disabled, -1 = num_ctx)"),
    ("Repeat Penalty:", "repeat_penalty", float, 0.1, 2.0, 0.1, 1.1, "Sets how strongly to penalize repetitions. (Default: 1.1)"),
    ("Temperature:", "temperature", float, 0.0, 2.0, 0.01, 0.5, "The temperature of the model. Increasing the temperature will make the model answer more creatively. (Default: 0.5)"),
    ("Seed:", "seed", int, 0, 10000, 1, 0, "Sets the random number seed to use for generation. Setting this to a specific number will make the model generate the same text for the same prompt. (Default: 0)"),
    ("Number of Predictions:", "num_predict", int, -1, 10000, 1, 1024, "Maximum number of tokens to output when generating text. (Default: 1024)"),
    ("Top K:", "top_k", int, 1, 1000, 1, 40, "Reduces the probability of generating nonsense. A higher value (e.g. 100) will give more diverse answers, while a lower value (e.g. 10) will be more conservative. (Default: 40)"),
    ("Top P:", "top_p", float, 0.0, 1.0, 0.01, 0.9, "Works together with top-k. A higher value (e.g., 0.95) will lead to more diverse text, while a lower value (e.g., 0.5) will generate more focused and conservative text. (Default: 0.9)"),
    ("Min P:", "min_p", float, 0.0, 1.0, 0.01, 0.0, "Alternative to top_p, and aims to ensure a balance of quality and variety. (Default: 0.0)"),
]

# Create the layout with two columns
for label, key, dtype, min_val, max_val, step, default, help_text in fields:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.text(label, help=help_text)
    with col2:
        if dtype == int:
            st.number_input(
                "A",
                key=key,
                value=default,  # Default value
                min_value=min_val,
                max_value=max_val,
                step=step,
                label_visibility="collapsed",
            )
        elif dtype == float:
            st.number_input(
                "A",
                key=key,
                value=default,  # Default value
                min_value=min_val,
                max_value=max_val,
                step=step,
                format="%.2f",
                label_visibility="collapsed",
            )

params = {}
for _, key, _, _, _, _, _, _ in fields:
    params['key'] = st.session_state.get(key)

st.text_input("Set a system prompt", key="sys_prompt")
st.text_input("Name your new model", key="model_name")

create = st.button("Create and load custom model")

new_name = st.session_state.get('model_name')
if create and new_name:
    base_model = st.session_state.get('base_model')
    print(base_model)
    # Create and load the custom model
    with st.spinner("Unloading previous model..."):
        unload_models()
    with st.spinner(f"Loading base model ({base_model})..."):
        OLLAMA_CLIENT.pull(base_model)
    with st.spinner(f"Creating new custom model {new_name}..."):
        OLLAMA_CLIENT.create( 
            model=new_name,
            from_=base_model,
            system=st.session_state.get('sys_prompt'),
            parameters=params
            )
    with st.spinner(f"Unloading base model ({base_model})"):
        time.sleep(0.5)
        OLLAMA_CLIENT.delete(base_model)
    # with st.spinner(f"Loading new model into memory..."):
    #     OLLAMA_CLIENT.pull(new_name+':latest')
    st.success("Model created and loaded successfully.")
