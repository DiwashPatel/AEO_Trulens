# models/claude_adapter.py

import os
import json
import anthropic


def call_claude(model_config: dict, prompt: str) -> dict:

    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        raise ValueError("CLAUDE_API_KEY not set")

    client = anthropic.Anthropic(api_key=api_key)

    model_name = model_config["name"]

    response = client.messages.create(
        model=model_name,
        max_tokens=2048,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text

    parsed_json = None
    try:
        parsed_json = json.loads(text)
    except json.JSONDecodeError:
        parsed_json = None

    return {
        "provider": "claude",
        "model": model_name,
        "raw_text": text,
        "parsed_json": parsed_json,
        "usage": response.usage.__dict__ if response.usage else None
    }