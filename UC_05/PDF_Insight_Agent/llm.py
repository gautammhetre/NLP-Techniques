"""LLM integration: Groq (default) or OpenAI, chosen with LLM_PROVIDER in .env."""
from config import (API_KEY, API_KEY_NAME, GROQ_MODEL, LLM_PROVIDER,
                    OPENAI_MODEL)
from prompts import SYSTEM_PROMPT

_client = None


def _get_client():
    global _client
    if not API_KEY:
        raise RuntimeError(f"{API_KEY_NAME} is missing. Add it to the .env file.")
    if _client is None:
        if LLM_PROVIDER == "openai":
            from openai import OpenAI
            _client = OpenAI(api_key=API_KEY)
        else:
            from groq import Groq
            _client = Groq(api_key=API_KEY)
    return _client


def ask_llm(user_prompt, system_prompt=SYSTEM_PROMPT, temperature=0.1):
    """Send one prompt to the LLM and return the text reply."""
    model = OPENAI_MODEL if LLM_PROVIDER == "openai" else GROQ_MODEL
    response = _get_client().chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()
