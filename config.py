"""Configuración del agente RAG."""
import os

LLM_MODEL = "gemini-flash-latest"           # genera las respuestas
EMBEDDING_MODEL = "gemini-embedding-001"  # convierte texto a vectores

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

DOCUMENT_PATH = "data/documento.pdf"
VECTOR_STORE_PATH = "data/faiss_index"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4  # fragmentos que se pasan como contexto