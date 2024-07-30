import os
import re
import streamlit as st
from dotenv import load_dotenv
from langsmith import Client
from llama_parse import LlamaParse
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables from a .env file
load_dotenv()

# Initialize LangSmith API client
langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")
langsmith_client = Client(api_key=langsmith_api_key)

# Load OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Load LlamaParse API key and initialize parser
llama_parse_api_key = os.getenv('LLAMA_PARSE_API_KEY')
parser = LlamaParse(
    api_key=llama_parse_api_key,
    result_type="text"
)

# Load and parse the PDF document
pdf_path = './staples_faq.pdf'
document = parser.load_data(pdf_path)

# Split the document text into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=200
)
chunks = text_splitter.split_text(document[0].text)

# Initialize the embedding model and vector store
embedding_model = OpenAIEmbeddings()
vector_store = FAISS.from_texts(chunks, embedding=embedding_model)

# Function to get the most relevant FAQ based on the user's query
def get_relevant_faq(query):
    search_results = vector_store.similarity_search(query=query, k=1)
    selected_chunk = search_results[0].page_content.strip()
    full_faq = selected_chunk
    match = re.search(r'(?<=\?)[^.]*\.', full_faq)
    return match.group(0).strip() if match else full_faq, selected_chunk

# -----------------------------------------------
# Streamlit App
# -----------------------------------------------

# Set the title of the Streamlit app
st.title("FAQ Bot")

# Get the user's query from a text input field
user_query = st.text_input("Ask a question:")
if user_query:
    # Retrieve the relevant FAQ and the selected chunk of text
    relevant_faq, selected_chunk = get_relevant_faq(user_query)
    print("Selected Chunk:", selected_chunk)
    
    # Initialize the OpenAI chat model
    model = ChatOpenAI(api_key=openai_api_key, model='gpt-4o')

    # Define the system message for the AI assistant
    system = """You are an AI assistant that helps people by examining sections \
of the FAQ document to answer their questions. Your responses should be clear and concise.
    """

    # Define the AI message template
    ai = "I used the following section to answer this question:\n\n{selected_chunk}"

    # Create the chat prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "{user_query}"),
        ("ai", ai)
    ])

    # Initialize the output parser
    output_parser = StrOutputParser()

    # Create the chain of operations
    chain = prompt | model | output_parser

    # Get the response from the AI model
    response = chain.invoke({"user_query": user_query, "selected_chunk": selected_chunk})
    
    # Display the answer in the Streamlit app
    st.write("Answer:", response)
