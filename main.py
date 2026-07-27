"""Punto de entrada: python main.py"""
from document_loader import load_and_split_document
from vector_store import build_vector_store, load_vector_store, vector_store_exists
from agent import build_rag_chain


def get_vector_store():
    if vector_store_exists():
        print("Índice encontrado, cargando...")
        return load_vector_store()
    print("Procesando documento por primera vez...")
    chunks = load_and_split_document()
    return build_vector_store(chunks)


def main():
    vector_store = get_vector_store()
    chain = build_rag_chain(vector_store)
    print("\nAgente listo. Escribí 'salir' para terminar.\n")

    while True:
        question = input("Pregunta: ").strip()
        if question.lower() in ("salir", "exit", "quit"):
            print("¡Listo!")
            break
        if not question:
            continue
        try:
            print(f"\nRespuesta: {chain.invoke(question)}\n")
        except Exception as e:
            print(f"\nError: {e}\n¿Está Ollama corriendo? Probá: ollama serve\n")


if __name__ == "__main__":
    main()
