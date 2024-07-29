import os
import streamlit as st
from pinecone import Pinecone
from langchain.chat_models import ChatOpenAI
from sentence_transformers import SentenceTransformer
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load API keys from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Define index names for different sections of the research papers
index_names = {
    "abstract": "abstract-index",
    "introduction": "introduction-index",
    "methodology": "methodology-index",
    "results": "results-index",
    "conclusion": "conclusion-index"
}

# Initialize the sentence transformer model for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------------------------
# Streamlit App
# -----------------------------------------------

# Set the title and description for the Streamlit app
st.title("Research Paper Summarization")
st.write("Enter a query to get a summary for a specific section.")

# Get the query from the user
query = st.text_input("Query:")

# Define the sections of the research papers
sections = ["abstract", "introduction", "methodology", "results", "conclusion"]

# When the button is clicked, process the query
if st.button("Get Summary"):
    if query:
        # Identify the section specified in the query
        identified_section = None
        for section in sections:
            if section in query.lower():
                identified_section = section
                break
        
        if not identified_section:
            st.write("Please specify a valid section (abstract, introduction, methodology, results, conclusion) in your query.")
        else:
            # Encode the query to a vector
            query_vector = model.encode(query).tolist()
            index_name = index_names[identified_section]
            index = pc.Index(index_name)
            
            # Query the Pinecone index for the most relevant sections
            results = index.query(vector=query_vector, top_k=5, include_metadata=True)
            
            sections_content = ""
            for result in results['matches']:
                vector_id = result['id']
                doc_id, chunk_id = vector_id.rsplit('_', 1)
                
                section_content = result['metadata']['text']
                sections_content += f"{section_content}\n\n"
            
            if sections_content:
                # Initialize the OpenAI chat model
                model = ChatOpenAI(api_key=openai_api_key, model='gpt-4o')

                # Define the system message for the AI assistant
                system = """
You are an AI assistant that helps university students by summarizing specific sections of research papers. \
When students ask for a summary of a section, you provide a concise summary. \
When preparing the summary, you should include information about the document and section. 
For example;
Document Name: "Generative AI"
Section: Abstract
"""
                # Define the AI message template
                ai = """Document: {doc_id}
Section: {identified_section}
Text: {sections_content}
"""
      
                # Create the chat prompt template
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system),
                    ("human", "{query}"),
                    ("ai", ai),
                ]).with_config({"run_name": "exercise_8", "tags": ["exercise_8"]})

                # Initialize the output parser
                output_parser = StrOutputParser()
                
                # Create the chain of operations
                chain = prompt | model | output_parser

                # Get the response from the AI model
                response = chain.invoke({"query": query, "doc_id": doc_id, "identified_section": identified_section, "sections_content": sections_content})

                # Display the summary in the Streamlit app
                st.write("Summary:")
                st.write(response)
            else:
                st.write(f"No content found for the section: {identified_section}")
    else:
        st.write("Please enter a valid query.")