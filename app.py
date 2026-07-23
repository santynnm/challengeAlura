"""Interfaz web para el agente RAG.
Correr con: streamlit run app.py
"""
import os
import streamlit as st

from document_loader import load_and_split_document
from vector_store import build_vector_store, load_vector_store, vector_store_exists
from agent import build_rag_chain
import config

st.set_page_config(page_title="Agente RAG", page_icon="🤖")
st.title("🤖 Hola! Respondo sobre tu documento")

# Subida del documento 
archivo = st.file_uploader("Subí el archivo PDF o CSV", type=["pdf", "csv"])

if archivo is not None:
    os.makedirs("data", exist_ok=True)
    extension = os.path.splitext(archivo.name)[1]
    ruta_guardado = f"data/documento{extension}"
    with open(ruta_guardado, "wb") as f:
        f.write(archivo.getbuffer())
    config.DOCUMENT_PATH = ruta_guardado
    st.success(f"Documento guardado: {archivo.name}")

# Procesado del documento (solo si cambia o no existe índice) 
if st.button("Procesar documento"):
    with st.spinner("Generando embeddings e indexando..."):
        chunks = load_and_split_document(config.DOCUMENT_PATH)
        st.session_state.vector_store = build_vector_store(chunks)
    st.success(f"Documento procesado: {len(chunks)} fragmentos indexados.")

# Cargar índice al abrir 
if "vector_store" not in st.session_state and vector_store_exists():
    st.session_state.vector_store = load_vector_store()

# Chat 
if "vector_store" in st.session_state:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for role, texto in st.session_state.messages:
        with st.chat_message(role):
            st.write(texto)

    pregunta = st.chat_input("Preguntá lo que quieras sobre el documento...")
    if pregunta:
        st.session_state.messages.append(("user", pregunta))
        with st.chat_message("user"):
            st.write(pregunta)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                chain = build_rag_chain(st.session_state.vector_store)
                respuesta = chain.invoke(pregunta)
                st.write(respuesta)
        st.session_state.messages.append(("assistant", respuesta))
else:
    st.info("Subí un documento y hacé clic en 'Procesar documento' para empezar.")
