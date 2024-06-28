import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = api_key
client = OpenAI()

prompt = "Can you provide a summary of the latest advancements in artificial intelligence as of 2024?"

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=150
)
summary = response.choices[0].message.content

print(summary)
with open('ai_advancements_summary.txt', 'w') as file:
    file.write(summary)
