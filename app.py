"""Interfaz web para el agente RAG.
Correr con: streamlit run app.py (o py -m streamlit run app.py en Windows)
"""
import os
import shutil
import streamlit as st

from document_loader import load_and_split_document
from vector_store import build_vector_store, load_vector_store, vector_store_exists
from agent import build_rag_chain
import config

UPLOADED_INDEX_PATH = "data/faiss_index_subido"

st.set_page_config(page_title="Agente RAG", page_icon="🤖")
st.title("🤖 Agente que responde sobre tu documento")

# --- Documento por defecto: se carga solo la primera vez que se abre la app ---
if "vector_store" not in st.session_state:
    if os.path.exists(config.DOCUMENT_PATH):
        with st.spinner("Cargando documento por defecto..."):
            if vector_store_exists(config.VECTOR_STORE_PATH):
                st.session_state.vector_store = load_vector_store(config.VECTOR_STORE_PATH)
            else:
                chunks = load_and_split_document(config.DOCUMENT_PATH)
                st.session_state.vector_store = build_vector_store(
                    chunks, save=True, path=config.VECTOR_STORE_PATH
                )
        st.session_state.doc_label = os.path.basename(config.DOCUMENT_PATH)

if "doc_label" in st.session_state:
    st.caption(f"📄 Documento activo: {st.session_state.doc_label}")

# --- Subir un documento distinto (opcional, reemplaza al default en esta sesión) ---
archivo = st.file_uploader("¿Querés usar otro documento? Subí un PDF o CSV", type=["pdf", "csv"])

if archivo is not None:
    os.makedirs("data", exist_ok=True)
    extension = os.path.splitext(archivo.name)[1]
    ruta_guardado = f"data/documento_subido{extension}"
    with open(ruta_guardado, "wb") as f:
        f.write(archivo.getbuffer())

    if st.button("Procesar documento subido"):
        with st.spinner("Generando embeddings e indexando..."):
            if os.path.exists(UPLOADED_INDEX_PATH):
                shutil.rmtree(UPLOADED_INDEX_PATH)
            chunks = load_and_split_document(ruta_guardado)
            st.session_state.vector_store = build_vector_store(
                chunks, save=True, path=UPLOADED_INDEX_PATH
            )
        st.session_state.doc_label = archivo.name
        st.success(f"Documento procesado: {len(chunks)} fragmentos indexados.")
        st.rerun()

# --- Chat ---
if "vector_store" in st.session_state:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for role, texto in st.session_state.messages:
        with st.chat_message(role):
            st.write(texto)

    pregunta = st.chat_input("Preguntá algo sobre el documento...")
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
    st.info("No se encontró un documento por defecto. Subí uno y hacé clic en 'Procesar documento subido'.")