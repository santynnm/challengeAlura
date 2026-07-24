"""Arma la cadena RAG: retriever -> prompt -> Gemma -> respuesta."""
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import config

PROMPT_TEMPLATE = """Respondé SOLO con el contexto de abajo. Si no está la
respuesta en el contexto, decilo explícitamente, no inventes.

Contexto:
{context}

Pregunta: {question}

Respuesta:"""


def format_docs(docs) -> str:
    return "\n\n---\n\n".join(d.page_content for d in docs)


def build_rag_chain(vector_store):
    llm = ChatOllama(model=config.LLM_MODEL, temperature=0.2)
    retriever = vector_store.as_retriever(search_kwargs={"k": config.TOP_K})
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
