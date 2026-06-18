"""LLM Basics + First API Call"""

# importing libraries
import time
import csv
from datetime import datetime
from ollama import chat
import streamlit as st
import tiktoken

# Configure the Streamlit page and application title
st.set_page_config(page_title="Local LLM App")
st.title("Local LLM App")

# Collect user inputs
name = st.text_input("Enter your name")
models = ["mistral:7b", "llama2:7b"]
choice = st.selectbox("select your model:", models)
prompt = st.text_area("Enter your prompt")


# Model generation parameters
temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
top_p = st.slider("Top-P", min_value=0.0, max_value=1.0, value=0.9, step=0.1)

def get_response(model, user_text, user_name, set_temperature, set_top_p):
    """Send a prompt to the selected Ollama model and return the response."""
    start_time = time.time()
    response = chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"The user's name is {user_name}. Greet them by name when appropriate.",
            },
            {"role": "user", "content": user_text},
        ],
        options={"temperature": set_temperature, "top_p": set_top_p},
    )
    end_time = time.time()
    return response["message"]["content"], end_time - start_time

def count_tokens(text):
    """Count the number of tokens in the given text using tiktoken."""
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def rate(model):
    """Retrieve the pricing"""
    model_costs = {
        "mistral:7b": {"input": 0.25, "output": 0.75},
        "llama2:7b": {"input": 0.15, "output": 0.60},
    }
    return model_costs[model]["input"], model_costs[model]["output"]

def save_log(model, user_text, input_token, output_token, time_taken, api_call_cost, temperature, top_p, ):
    """Store interaction details in a CSV log file."""
    with open("logs.csv", "a", newline="", encoding="utf-8") as file:
        content = csv.writer(file)
        content.writerow(
            [
                datetime.now(),
                model,
                user_text,
                input_token,
                output_token,
                round(time_taken, 2),
                round(api_call_cost, 8),
                temperature,
                top_p,
            ]
        )

# Generate a response when the user submits a prompt
if st.button("Generate") and prompt:
    # Display a loading indicator
    with st.spinner("Generating response..."):
        output_text, elapsed_time = get_response(
            choice, prompt, name, temperature, top_p
        )
    # Calculate estimated token usage and API cost
    INPUT_RATE, OUTPUT_RATE = rate(choice)
    input_tokens = count_tokens(prompt)
    output_tokens = count_tokens(output_text)
    input_cost = input_tokens * INPUT_RATE / 1000000
    output_cost = output_tokens * OUTPUT_RATE / 1000000
    total_cost = input_cost + output_cost
    # Save interaction details for analysis
    save_log(choice, prompt, input_tokens, output_tokens, elapsed_time, total_cost,temperature,top_p,)
    # Display model response and generation statistics
    st.subheader("Response")
    st.write(output_text)
    st.subheader("Statistics")
    st.write(f"Input Tokens : {input_tokens}")
    st.write(f"Output Tokens: {output_tokens}")
    st.write(f"Elapsed Time : {elapsed_time:.2f} seconds")
    st.write(f"Inference Cost : ${total_cost:.6f}")
