"""Groq API integration."""
from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL
from prompts import SYSTEM_PROMPT

_client = None


def ask_llm(user_prompt, system_prompt=SYSTEM_PROMPT, temperature=0.1):
    """Send one prompt to Groq and return the text reply."""
    global _client
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing. Copy .env.example to .env and add your key.")
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    response = _client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()
