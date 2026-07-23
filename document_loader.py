"""Carga un PDF o CSV y lo divide en fragmentos (chunks)."""
import os
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config


def load_and_split_document(file_path: str = None):
    file_path = file_path or config.DOCUMENT_PATH
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró '{file_path}'. Poné tu PDF o CSV ahí.")

    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".csv":
        loader = CSVLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Formato '{ext}' no soportado (usá PDF o CSV).")

    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"'{file_path}': {len(documents)} páginas -> {len(chunks)} fragmentos.")
    return chunks


if __name__ == "__main__":
    chunks = load_and_split_document()
    print(chunks[0].page_content[:300])
