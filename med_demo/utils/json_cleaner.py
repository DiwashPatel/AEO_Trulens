# utils/json_cleaner.py

import json
import re


def extract_json_block(text: str):
    """
    Extracts first JSON object found inside text.
    Useful when model wraps JSON inside explanations.
    """

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


def safe_parse_json(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return extract_json_block(text)