import os
import json
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not set")

client = OpenAI(api_key=API_KEY)

PROMPT = """
Suggest me the best laptop for coders.
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=PROMPT
)

# Extract text safely
output_text = response.output[0].content[0].text

try:
    data = json.loads(output_text)
    print(json.dumps(data, indent=2))
except json.JSONDecodeError:
    print("Model did not return clean JSON:\n")
    print(output_text)