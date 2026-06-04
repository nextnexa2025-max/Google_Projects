import os
import pickle
import requests
import PyPDF2

ATTACHMENT_FOLDER = "attachments"
VECTOR_STORE = "vectors.pkl"

EMBED_MODEL = "nomic-embed-text"


# -----------------------------
# Simple custom text splitter
# -----------------------------
def split_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


# -----------------------------
# Load documents
# -----------------------------
def load_documents():
    docs = []
    for filename in os.listdir(ATTACHMENT_FOLDER):
        path = os.path.join(ATTACHMENT_FOLDER, filename)

        # -----------------------------
        # TXT
        # -----------------------------
        if filename.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                docs.append(f.read())

        # -----------------------------
        # PDF
        # -----------------------------
        elif filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            docs.append(text)

        # -----------------------------
        # CSV
        # -----------------------------
        elif filename.endswith(".csv"):
            try:
                import csv
                text = ""
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        # Join each row into a readable line
                        text += " ".join(row) + "\n"
                docs.append(text)
            except Exception as e:
                print(f"Error reading CSV {filename}: {e}")

    return docs



# -----------------------------
# Embed text using Ollama
# -----------------------------
def embed_text(text):
    response = requests.post(
        "http://127.0.0.1:11434/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text}
    )
    return response.json()["embedding"]


# -----------------------------
# Main processing
# -----------------------------
def process_documents():
    print("Loading documents...")
    docs = load_documents()

    print("Splitting into chunks...")
    chunks = []
    for doc in docs:
        chunks.extend(split_text(doc))

    print("Embedding chunks with Ollama...")
    embeddings = [embed_text(chunk) for chunk in chunks]

    print("Saving vector store...")
    with open(VECTOR_STORE, "wb") as f:
        pickle.dump({"chunks": chunks, "embeddings": embeddings}, f)

    print("Done! Vector store saved.")


if __name__ == "__main__":
    process_documents()
