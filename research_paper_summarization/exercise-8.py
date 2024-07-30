import os
from pinecone import Pinecone, ServerlessSpec
from unstructured.partition.pdf import partition_pdf
from sentence_transformers import SentenceTransformer

# -----------------------------------------------
# Vector Database Setup
# -----------------------------------------------

# Initialize Pinecone with API key
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Define index names for different sections of documents
index_names = ["abstract-index", "introduction-index", "methodology-index", "results-index", "conclusion-index"]
for index_name in index_names:
    # Create index if it doesn't exist
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="euclidean",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

# Assign indexes to variables for easy access
abstract_index = pc.Index("abstract-index")
introduction_index = pc.Index("introduction-index")
methodology_index = pc.Index("methodology-index")
results_index = pc.Index("results-index")
conclusion_index = pc.Index("conclusion-index")

print("\nVector Database Setup Done\n")

# -----------------------------------------------
# Document Processing
# -----------------------------------------------

# Directory containing the research papers
directory = "research_papers"

# Function to process documents and extract sections
def process_documents(directory):
    document_sections = {}
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            sections = partition_pdf(filepath)
            document_sections[filename] = sections
    return document_sections

document_sections = process_documents(directory)
print(f"Document Sections:\n {document_sections}")

# Function to split sections of documents based on keywords
def split_sections(sections):
    section_dict = {
        "abstract": "",
        "introduction": "",
        "methodology": "",
        "results": "",
        "conclusion": ""
    }

    current_section = None
    for section in sections:
        text = section.text
        # Identify section based on keywords
        if "abstract" in text.lower():
            current_section = "abstract"
        elif "introduction" in text.lower():
            current_section = "introduction"
        elif "methodology" in text.lower() or "methods" in text.lower():
            current_section = "methodology"
        elif "results" in text.lower():
            current_section = "results"
        elif "conclusion" in text.lower() or "discussion" in text.lower():
            current_section = "conclusion"
        
        # Append text to the corresponding section
        if current_section:
            section_dict[current_section] += text + "\n"
    return section_dict

split_documents = {filename: split_sections(sections) for filename, sections in document_sections.items()}
print(f"Split Documents:\n {split_documents}")

print("\nDocument Processing Done\n")

# -----------------------------------------------
# Vector Storage and Retrieval
# -----------------------------------------------

# Initialize the Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Function to split text into chunks
def chunk_content(text, chunk_size=1000):
    chunks = []
    words = text.split()
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Function to get vectors for each section
def get_section_vectors(sections, chunk_size=1000):
    section_vectors = {}
    for section_name, section_content in sections.items():
        chunks = chunk_content(section_content, chunk_size)
        for idx, chunk in enumerate(chunks):
            vector = model.encode([chunk])[0]
            vector_id = f"{section_name}_{idx}"
            section_vectors[vector_id] = (vector, chunk)
    return section_vectors

document_vectors = {filename: get_section_vectors(sections) for filename, sections in split_documents.items()}
print(f"Document Vectors:\n {document_vectors}")

# Function to upload vectors to Pinecone
def upload_vectors_to_pinecone(document_vectors):
    for doc_id, sections in document_vectors.items():
        for vector_id, (vector, section_content) in sections.items():
            section_name, chunk_idx = vector_id.rsplit('_', 1)
            metadata = {
                "document_id": doc_id,
                "section": section_name,
                "chunk_index": chunk_idx,
                "text": section_content
            }
            index_name = f"{section_name}-index"
            pc.Index(index_name).upsert(vectors=[(f"{doc_id}_{vector_id}", vector, metadata)])

upload_vectors_to_pinecone(document_vectors)

print("\nVector Storage and Retrieval Done\n")
