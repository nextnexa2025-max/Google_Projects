from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn
import pickle
import numpy as np

# -----------------------------
# FastAPI Setup
# -----------------------------
app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Load Vector Store
# -----------------------------
try:
    with open("vectors.pkl", "rb") as f:
        vector_store = pickle.load(f)

    chunks = vector_store["chunks"]
    embeddings = np.array(vector_store["embeddings"])

    print("Vector store loaded successfully!")

except Exception as e:
    print("Could not load vector store:", e)
    chunks = []
    embeddings = None


# -----------------------------
# Embedding Function (Ollama)
# -----------------------------
def embed_query(text):
    response = requests.post(
        "http://127.0.0.1:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    return np.array(response.json()["embedding"])


# -----------------------------
# Retrieval Function
# -----------------------------
def retrieve_relevant_chunks(query, top_k=3):
    if embeddings is None:
        return None

    query_emb = embed_query(query)

    # Cosine similarity
    scores = np.dot(embeddings, query_emb) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_emb)
    )

    # If all scores are extremely low, context is useless
    if np.max(scores) < 0.15:   # threshold
        return None

    top_indices = np.argsort(scores)[-top_k:][::-1]
    return "\n\n".join([chunks[i] for i in top_indices])


# -----------------------------
# Request Model
# -----------------------------
class ChatRequest(BaseModel):
    prompt: str


# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    user_prompt = request.prompt

    # Retrieve context
    context = retrieve_relevant_chunks(user_prompt)

    # -----------------------------
    # FALLBACK: No context → normal LLM
    # -----------------------------
    if (
        context is None
        or context.strip() == ""
        or len(context) < 20
    ):
        print("⚠️ No relevant context found — using normal LLM response.")

        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": user_prompt,
                "stream": False
            }
        )
        data = response.json()
        return {"response": data.get("response", "No response from AI.")}

    # -----------------------------
    # RAG MODE (context found)
    # -----------------------------
    final_prompt = f"""
Use the following context to answer the question.

CONTEXT:
{context}

QUESTION:
{user_prompt}

ANSWER:
"""

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3.2:1b",
            "prompt": final_prompt,
            "stream": False
        }
    )

    data = response.json()
    return {"response": data.get("response", "No response from AI.")}


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
