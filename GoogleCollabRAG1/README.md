Ollama RAG with Phi‑3 — Jupyter Notebook Project
This repository contains a Jupyter Notebook implementation of a Retrieval‑Augmented Generation (RAG) workflow using Ollama and Microsoft Phi‑3.
The notebook demonstrates how to install Ollama, load the Phi‑3 model locally, embed documents, build a vector store, and perform context‑aware question answering.

🚀 Features
Run Phi‑3 locally using Ollama

Build a complete RAG pipeline inside a single notebook
Process and chunk documents for retrieval
Create embeddings using FAISS
Perform semantic search and context retrieval
Generate grounded answers using your own data
Works in Google Colab or on your local machine

📂 Repository Structure
Code
.
├── OllamaRAGPhi3.ipynb     # Main notebook
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

🛠️ Prerequisites
1. Install Ollama
Download and install Ollama from:
https://ollama.com/download
Then pull the Phi‑3 model:

Code
ollama pull phi3
2. Install Python Dependencies
Install the required Python packages:

Code
pip install -r requirements.txt
▶️ How to Run the Notebook
Option A — Run Locally
Install Python 3.10+

Install dependencies
Start Ollama in the background
Launch the notebook:

Code
jupyter notebook OllamaRAGPhi3.ipynb
Option B — Run in Google Colab
Upload the notebook to Google Colab

Run the setup cells (system installs + pip installs)
Connect Colab to your local machine’s Ollama instance
Execute the RAG pipeline cells
Note: The notebook includes all required installation commands.

📚 What the Notebook Covers

Installing system dependencies (zstd, Ollama)
Installing Python libraries (FAISS, pandas, numpy, requests)
Starting and interacting with Ollama
Loading the Phi‑3 model
Document ingestion and chunking
Embedding creation using FAISS
Vector search for relevant context
RAG‑based question answering

🧠 Model Used
Phi‑3 — a compact, efficient, high‑quality model ideal for local RAG applications.
Runs fully offline using Ollama.

🤝 Contributing
Contributions, improvements, and suggestions are welcome.
Feel free to open an issue or submit a pull request.

📄 License
This project is open‑source under the MIT License.