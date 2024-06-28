import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = api_key
client = OpenAI()

prompt = "Generate a list of 5 innovative business ideas based on AI technologies. Each idea should be unique, feasible, and have a brief description."

# prompt = """
# Please generate a list of 5 innovative business ideas based on AI technologies. For each idea, provide the following details:
# 1. Business Idea Name
# 2. Description
# 3. Target Market
# 4. Potential Benefits
# 5. Implementation Strategy
# """

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
]

response = client.chat.completions.create(
    model="gpt-4",  
    messages=messages,
    max_tokens=500, 
    n=1,
    temperature=0.7
)

response_text = response.choices[0].message.content
business_ideas = response_text.split('\n')

structured_ideas = []
for i, idea in enumerate(business_ideas):
    if idea.strip():
        structured_ideas.append(f"{idea.strip()}\n")

for idea in structured_ideas:
    print(idea)
