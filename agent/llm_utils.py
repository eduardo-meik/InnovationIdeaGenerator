#llm_utils.py
import streamlit as st
import json
import openai
import logging
from prompts import auto_agent_instructions

openai_api_key = st.secrets["general"]["openai_api_key"]

temperature = st.secrets["general"]["temperature"]
smart_llm_model = st.secrets.get("smart_llm_model", "default_model_name")  # the `get` method provides a fallback in case the key doesn't exist


def create_chat_completion(
    messages: list,
    model: str,
    temperature: float = st.secrets["general"]["temperature"],
    max_tokens: int = None,
) -> str:
    """Create a chat completion using the OpenAI API."""
    
    # Validate input
    if model is None:
        raise ValueError("Model cannot be None")
    if max_tokens is not None and max_tokens > 8001:
        raise ValueError(f"Max tokens cannot be more than 8001, but got {max_tokens}")

    # Create response
    for attempt in range(10):  # Maximum of 10 attempts
        response = send_chat_completion_request(
            messages, model, temperature, max_tokens
        )
        return response

    logging.error("Failed to get response from OpenAI API")
    raise RuntimeError("Failed to get response from OpenAI API")


def send_chat_completion_request(messages, model, temperature, max_tokens):
    result = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return result["choices"][0]["message"]["content"]

def choose_agent(task: str) -> str:
    """Determines what agent should be used."""
    try:
        response = create_chat_completion(
            model=st.secrets["smart_llm_model"],
            messages=[
                {"role": "system", "content": f"{auto_agent_instructions()}"},
                {"role": "user", "content": f"task: {task}"}],
            temperature=0,
        )
        return json.loads(response)
    except Exception as e:
        logging.error(f"Error in choose_agent: {e}")
        return {
            "agent": "Default Agent",
            "agent_role_prompt": "You are an AI critical thinker research assistant. Your sole purpose is to write well written, critically acclaimed, objective and structured reports on given text."
        }

