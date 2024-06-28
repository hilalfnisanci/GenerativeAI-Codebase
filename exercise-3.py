import os
from openai import OpenAI
import csv

api_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = api_key
client = OpenAI()

reviews = [
    "This product is amazing! It exceeded my expectations.",
    "I'm very disappointed with this purchase. It broke after one use.",
    "The product is okay, but not great. It works as advertised.",
    "Excellent quality and fast shipping. Very happy with this purchase.",
    "Terrible product. It didn't work at all.",
    "Good value for the money. Satisfied with my purchase.",
    "The product is decent, but I had issues with the customer service.",
    "Absolutely love it! Will buy again.",
    "Not worth the price. I expected better quality.",
    "Met all my expectations. Works perfectly."
]

def analyze_sentiment(review):

    prompt = f"""
    Please analyze the sentiment of the following product review and classify it as "positive", "negative", or "neutral":
    "{review}"
    Example: 
    Review: "Terrible quality. Do not buy."
    Sentiment: negative

    Review: "{review}"
    Sentiment:"""
    
    messages = [
        {"role": "system", "content": "You are an assistant that analyzes sentiment in product reviews. "},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-4", 
        messages=messages,
        max_tokens=10
    )
    sentiment = response.choices[0].message.content
    return sentiment

results = []
for review in reviews:
    sentiment = analyze_sentiment(review)
    results.append({'review': review, 'sentiment': sentiment})

csv_file = 'sentiment_analysis_results.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['review', 'sentiment'])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f'Sentiment analysis results saved to {csv_file}')