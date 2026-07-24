# Challenge Alura - Agente RAG

Este es mi proyecto para el Challenge Alura Agente: un agente que responde preguntas basándose en el contenido de un documento (PDF o CSV), corriendo con modelos open source en mi propia máquina.

## Por qué este stack

Elegí Gemma porque es gratis y corre localmente con Ollama, así no dependo de una API paga. Para buscar la info relevante dentro del documento uso embeddings (embeddinggemma) y los guardo en un índice FAISS. LangChain conecta todas las piezas.

## Arquitectura

El flujo es:

1. `document_loader.py` lee el PDF/CSV y lo corta en fragmentos más chicos (chunks), porque el modelo no puede procesar el documento entero de una.
2. `vector_store.py` convierte cada fragmento en un vector (embedding) y arma un índice FAISS para poder buscar rápido cuál fragmento es más relevante para una pregunta.
3. `agent.py` toma la pregunta, busca los fragmentos más relevantes en el índice, y se los pasa como contexto a Gemma para que arme la respuesta.
4. `main.py` es la versión por consola, y `app.py` es la interfaz web hecha con Streamlit.

## Tecnologías

- Python
- LangChain + langchain-ollama
- Ollama (Gemma 4: `gemma4:e2b` para generar respuestas, `embeddinggemma` para los embeddings)
- FAISS (búsqueda vectorial)
- Streamlit (interfaz web)

## Cómo correrlo

```bash
# Instalar Ollama y bajar los modelos
ollama pull gemma4:e2b
ollama pull embeddinggemma

# Instalar dependencias de Python
py -m pip install -r requirements.txt

# Poner tu PDF o CSV en data/documento.pdf

# Opción 1: por consola
py main.py

# Opción 2: interfaz web
py -m streamlit run app.py
```

## Ejemplos de uso

Probé el agente con un documento de ejemplo que tiene información de una empresa ficticia,  (políticas internas, productos, soporte técnico). Algunas preguntas y respuestas:

**Pregunta:** ¿Cuál es el SLA garantizado de CloudNode?
**Respuesta:** *(99.99% de tiempo de actividad garantizado.)*

**Pregunta:** ¿Cuántas semanas de licencia por paternidad se otorgan?
**Respuesta:** *(16 semanas pagas, extensibles a 20 semanas en caso de nacimientos múltiples.)*

**Pregunta:** ¿Qué hago si NexusGuard bloquea tráfico de IPs internas?
**Respuesta:** *(Acceder al panel de control de NexusGuard mediante credenciales de administrador. Navegar a Configuración de Red > Reglas de Filtrado. Seleccionar la opción Añadir Excepción (Whitelisting). Ingresar el rango de IPs internas utilizando notación CIDR (ejemplo: 192.168.1.0/24). Reiniciar el servicio de monitoreo ejecutando el comando systemctl restart nexusguard-monitor en el servidor principal.)*

## Deploy

*(Falta Completar con el link público)*

