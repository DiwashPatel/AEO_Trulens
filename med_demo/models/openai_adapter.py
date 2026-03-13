# models/openai_adapter.py

import os
import json
from openai import OpenAI


def call_openai(model_config: dict, prompt: str) -> dict:

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    client = OpenAI(api_key=api_key)

    model_name = model_config["name"]
    search_enabled = model_config.get("search_enabled", False)

    tools = [{"type": "web_search"}] if search_enabled else None

    response = client.responses.create(
        model=model_name,
        tools=tools,
        tool_choice="auto" if search_enabled else None,
        input=prompt,
        temperature=0.7
    )

    output_text = ""

    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if content.type == "output_text":
                    output_text += content.text

    parsed_json = None
    try:
        parsed_json = json.loads(output_text)
    except json.JSONDecodeError:
        parsed_json = None

    tool_calls = [
        item.model_dump()
        for item in response.output
        if item.type == "tool_call"
    ]

    return {
        "provider": "openai",
        "model": model_name,
        "raw_text": output_text,
        "parsed_json": parsed_json,
        "tool_calls": tool_calls,
        "usage": response.usage.model_dump() if response.usage else None
    }