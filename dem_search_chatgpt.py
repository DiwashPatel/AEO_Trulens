import os
import json
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not set")

client = OpenAI(api_key=API_KEY)

PROMPT = """
I want to buy the best laptop for coding.
Please search the web and recommend top options.
Include:
- product name
- why recommended
- direct URL source used
Return results strictly in JSON format like this:

{
  "recommendations": [
    {
      "product": "",
      "reason": "",
      "source_url": ""
    }
  ]
}
"""

response = client.responses.create(
    model="gpt-4.1",  # IMPORTANT: use full model, not mini
    tools=[{"type": "web_search"}],  # Enables real-time search
    tool_choice="auto",
    input=PROMPT,
    temperature=0.7
)

# Extract final text output
output_text = ""

for item in response.output:
    if item.type == "message":
        for content in item.content:
            if content.type == "output_text":
                output_text += content.text

try:
    data = json.loads(output_text)
    print("\nStructured JSON Output:\n")
    print(json.dumps(data, indent=2))
except json.JSONDecodeError:
    print("\nModel did not return clean JSON:\n")
    print(output_text)

# Optional: print citations from tool usage (if available)
print("\n---- TOOL CALLS (Search Evidence) ----\n")

for item in response.output:
    if item.type == "tool_call":
        print(item)