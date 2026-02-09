import os
from dotenv import load_dotenv
import chromadb
import openai

# Load environment variables
load_dotenv()

# ----------------------------
# OpenAI setup
# ----------------------------
openai.api_key = os.environ.get("OPENAI_API_KEY")

from openai import OpenAI
import os

openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def ask_gpt(question, context):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",  # better, cheaper, safer
        messages=[
            {
                "role": "system",
                "content": "You are a helpful customer support assistant. Answer ONLY using the provided context. If the answer is not in the context, say you don't know."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ],
        temperature=0.2,
        max_tokens=250
    )

    return response.choices[0].message.content


# ----------------------------
# Connect to persistent Chroma DB
# ----------------------------
DB_PATH = "chroma_db"
COLLECTION_NAME = "support_docs"

chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_collection(name=COLLECTION_NAME)

def get_ai_answer(question, collection):
    if not question:
        return "", []

    results = collection.query(query_texts=[question], n_results=3)

    if results and results["documents"]:
        docs = results["documents"][0]
        metadatas = results["metadatas"][0]
        context = "\n\n".join(docs)
        sources = list({m["source"] for m in metadatas})
    else:
        context = ""
        sources = []

    answer = ask_gpt(question, context)
    return answer, sources
