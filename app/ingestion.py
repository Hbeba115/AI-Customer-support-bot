import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

# Load environment variables 
load_dotenv()

DOCS_FOLDER = "data/docs/"    # Folder containing all data

DB_PATH = "chroma_db"        
COLLECTION_NAME = "support_docs"

embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"],
    model_name="text-embedding-3-small"
)

# Connect to persistent Chroma DB
client = chromadb.PersistentClient(path=DB_PATH)

# Create or get collection
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)

# Ingest all text files
files = [f for f in os.listdir(DOCS_FOLDER) if f.endswith(".txt")]

if not files:
    print("No text files found in data/docs/! Add some and try again.")
else:
    for i, file in enumerate(files):
        file_path = os.path.join(DOCS_FOLDER, file)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Add document to collection
        collection.add(
            documents=[text],
            ids=[f"doc{i}"]  # Unique ID for each document
        )
        print(f"✅ Added {file} to collection.")

    print("\n🎉 Ingestion complete. Chroma DB created and persisted!")
