import re
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import chromadb
import os
from app.config.config import db_directory, ollama_url


def sanitize_name(name: str) -> str:
    """Convierte cualquier cadena a un nombre válido para Chroma."""
    sanitized = name.lower()  # minúsculas
    sanitized = re.sub(r"[^a-z0-9._-]", "_", sanitized)  # reemplaza caracteres inválidos por _
    sanitized = re.sub(r"^[^a-z0-9]+", "", sanitized)    # asegura que empiece con letra/número
    sanitized = re.sub(r"[^a-z0-9]+$", "", sanitized)    # asegura que termine con letra/número
    return sanitized

def get_vector_stores(materia: str):
    os.makedirs(db_directory, exist_ok=True)
    collection_name = sanitize_name(materia)
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=ollama_url)
    client = chromadb.PersistentClient(path=db_directory)
    
    return Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=db_directory  
    )

def get_vector_store_cuestions(materia: str, unidad_elemento: str):
    os.makedirs(db_directory, exist_ok=True)
    collection_name = sanitize_name(f"{materia}_{unidad_elemento}")
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=ollama_url)
    client = chromadb.PersistentClient(path=db_directory)

    return Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=db_directory 
    )
