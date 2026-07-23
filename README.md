# Challenge Alura Agente

Agente de IA que responde preguntas sobre el contenido de un documento (PDF o CSV), usando Gemma corriendo localmente vía Ollama + LangChain + FAISS.

## Cómo correrlo

```bash
ollama pull gemma4:e2b
ollama pull embeddinggemma
pip install -r requirements.txt
# Colocar documentacion en data/documento.pdf
python main.py
```

## Arquitectura

`document_loader.py` carga y troceo del documento → `vector_store.py` genera embeddings y arma el índice FAISS → `agent.py` arma la cadena RAG (busca contexto + genera respuesta con Gemma) → `main.py` es el loop de preguntas.
