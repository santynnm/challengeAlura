"""Genera embeddings y arma/carga el índice vectorial FAISS."""
import os
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import config


def get_embeddings():
    return OllamaEmbeddings(model=config.EMBEDDING_MODEL)


def build_vector_store(chunks, save: bool = True):
    embeddings = get_embeddings()
    vs = FAISS.from_documents(chunks, embeddings)
    if save:
        os.makedirs(os.path.dirname(config.VECTOR_STORE_PATH), exist_ok=True)
        vs.save_local(config.VECTOR_STORE_PATH)
        print(f"Índice guardado en '{config.VECTOR_STORE_PATH}'.")
    return vs


def load_vector_store():
    embeddings = get_embeddings()
    return FAISS.load_local(
        config.VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True
    )


def vector_store_exists() -> bool:
    return os.path.exists(config.VECTOR_STORE_PATH)
