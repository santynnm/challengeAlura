"""Configuración del agente RAG."""

LLM_MODEL = "gemma4:e2b"          # genera las respuestas
EMBEDDING_MODEL = "embeddinggemma"  # convierte texto a vectores

DOCUMENT_PATH = "data/documento.pdf"
VECTOR_STORE_PATH = "data/faiss_index"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4  # fragmentos que se pasan como contexto
