import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

# Load environment variables 
load_dotenv()

DOCS_FOLDER = "data/docs/"    # Folder containing all data

DB_PATH = "chroma_db"        
COLLECTION_NAME = "support_docs"


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Connect to persistent Chroma DB
client_chroma = chromadb.PersistentClient(path=DB_PATH)


# If collection exists, delete it first (for fresh ingestion)
try:
    client_chroma.delete_collection(name=COLLECTION_NAME)
except:
    pass


collection = client_chroma.create_collection(name=COLLECTION_NAME)

for filename in os.listdir(DOCS_FOLDER):
    if not filename.endswith(".txt"):
        continue
    file_path = os.path.join(DOCS_FOLDER, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split text into small chunks (1 paragraph per chunk)
    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

    # Add each chunk to Chroma collection
    for chunk in chunks:
        collection.add(
            documents=[chunk],
            metadatas=[{"source": filename}],
            ids=[f"{filename}-{chunks.index(chunk)}"]
            )

print("✅ Ingestion complete. Chroma DB created.")