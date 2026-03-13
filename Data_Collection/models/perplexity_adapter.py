# models/perplexity_adapter.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def call_perplexity(model_config: dict, prompt: str) -> dict:

    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY not set")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.perplexity.ai"
    )

    model_name = model_config["name"]

    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    text = response.choices[0].message.content

    parsed_json = None
    try:
        parsed_json = json.loads(text)
    except json.JSONDecodeError:
        parsed_json = None

    return {
        "provider": "perplexity",
        "model": model_name,
        "raw_text": text,
        "parsed_json": parsed_json,
        "usage": response.usage.__dict__ if response.usage else None
    }