🚀 AIRAG Project – Local Setup & Run Guide
Created by NextNexa Creator

✅ Step 1: Start the FastAPI Backend
Run the backend server using Uvicorn (Open terminal window inside AIRAGPROJECT folder):

uvicorn main:app --reload --port 8000

This launches your FastAPI API at:
http://127.0.0.1:8000 

Mainold.py has only RAG
Main.py has stwitch RAG vs Local LLM 

✅ Step 2: Start the Local Frontend Server
Run a simple local HTTP server (Open terminal window inside Frontend folder):

python -m http.server 5500

This serves your frontend files at:
http://127.0.0.1:5500 

✅ Step 3: Running LLMs Locally
Depending on your setup, this may involve (Open terminal window inside Frontend folder):

Starting an LLM engine (Ollama, LM Studio, GPT4All, etc.)
Loading your model (e.g., llama3, mistral, phi3, etc.)
Ensuring your backend connects to the local model endpoint
Example (Ollama):

ollama run llama3
Make sure your FastAPI backend points to the correct local LLM endpoint.

✅ Step 4: Open the Real‑Time Streaming UI
Once both servers are running:

Backend → http://127.0.0.1:8000 

Frontend → http://127.0.0.1:5500 

Open the main UI:

👉 http://127.0.0.1:5500/index.html

This page will stream responses from your locally running LLM in real time.


Fore more detailed steps visit: 
https://www.youtube.com/channel/UCbGaQ3pPquBe7FNgM0SOfrQ 
