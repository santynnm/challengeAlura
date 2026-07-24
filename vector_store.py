"""Genera embeddings y arma/carga el índice vectorial FAISS."""
import os
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import config


def get_embeddings():
    return OllamaEmbeddings(model=config.EMBEDDING_MODEL)


def build_vector_store(chunks, save: bool = True, path: str = None):
    path = path or config.VECTOR_STORE_PATH
    embeddings = get_embeddings()
    vs = FAISS.from_documents(chunks, embeddings)
    if save:
        os.makedirs(path, exist_ok=True)
        vs.save_local(path)
        print(f"Índice guardado en '{path}'.")
    return vs


def load_vector_store(path: str = None):
    path = path or config.VECTOR_STORE_PATH
    embeddings = get_embeddings()
    return FAISS.load_local(
        path, embeddings, allow_dangerous_deserialization=True
    )


def vector_store_exists(path: str = None) -> bool:
    path = path or config.VECTOR_STORE_PATH
    return os.path.exists(path)