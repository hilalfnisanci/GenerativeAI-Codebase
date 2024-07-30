# Import required libraries and modules
import os
import pandas as pd
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the ChatOpenAI model with the API key and specify the GPT-4 model
model = ChatOpenAI(api_key=api_key, model='gpt-4o')

# Define the system message for the AI assistant
system = """
You are an AI assistant performing sentiment analysis on product reviews.
You should analyze each review as "positive", "negative", or "neutral".
For example;
Review: This product is very useful. It met all my expectations. You should definitely buy it.
Sentiment Analysis: Positive
"""

# Create a prompt template for the chat model
prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "{reviews}"),
])

# Initialize the output parser
output_parser = StrOutputParser()

# Create a chain that connects the prompt, model, and output parser
chain = prompt | model | output_parser

# Define a list of reviews
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

# Combine reviews into a single string separated by newline characters
reviews_str = "\n".join(reviews)

# Invoke the chain with the reviews and get the response
response = chain.invoke({"reviews": reviews_str})

# Print the response
print(response)

# Initialize lists to store reviews and their sentiments
yorumlar = []
duygular = []

# Process the response to extract reviews and their sentiments
lines = response.strip().split("\n")
for i in range(0, len(lines), 3):
    yorum = lines[i].replace("Review: ", "").strip()
    duygu = lines[i+1].replace("Sentiment Analysis: ", "").strip()
    yorumlar.append(yorum)
    duygular.append(duygu)

# Create a DataFrame to store the reviews and their sentiments
df = pd.DataFrame({
    "Review": yorumlar,
    "Sentiment Analysis": duygular
})

# Save the DataFrame to a CSV file
df.to_csv("sentiment_analysis_results.csv", index=False)

# Print a confirmation message
print("Sentiment analysis results saved")