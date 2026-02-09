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

def ask_gpt(question, context):
    """
    Generates a natural answer using GPT-3.5-turbo based on retrieved context.
    """
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    # Use chat completion (GPT-3.5-turbo)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful customer support assistant."},
            {"role": "user", "content": f"Answer the question based on the context below.\n\nContext: {context}\n\nQuestion: {question}"}
        ],
        temperature=0.2,
        max_tokens=200
    )

    return response.choices[0].message.content

# ----------------------------
# Connect to persistent Chroma DB
# ----------------------------
DB_PATH = "chroma_db"
COLLECTION_NAME = "support_docs"

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(name=COLLECTION_NAME)

# ----------------------------
# Chat loop
# ----------------------------
print("Hello! Ask me anything about the documents.")
print("Type 'exit' to quit.\n")

while True:
    question = input("> ").strip()

    if question.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    if not question:
        continue

    # Retrieve top 3 relevant documents
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    # Combine all relevant docs into a single context
    context = "\n\n".join(results["documents"][0])

    # Generate AI answer
    answer = ask_gpt(question, context)


    print("\nAI Answer:")
    print(answer)
    print("\n---\n")
