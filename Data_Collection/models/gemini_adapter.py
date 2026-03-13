# models/gemini_adapter.py

import os
import json
from google import genai
from dotenv import load_dotenv
load_dotenv()

def call_gemini(model_config: dict, prompt: str) -> dict:

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    model_name = model_config["name"]

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    text = getattr(response, "text", None)

    parsed_json = None
    if text:
        try:
            parsed_json = json.loads(text)
        except json.JSONDecodeError:
            parsed_json = None

    usage = getattr(response, "usage_metadata", None)

    return {
        "provider": "gemini",
        "model": model_name,
        "raw_text": text,
        "parsed_json": parsed_json,
        "usage": usage
    }