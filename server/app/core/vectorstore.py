from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import chromadb
import os
from app.config.config import db_directory, ollama_url


def get_vector_stores(materia):
    # Asegurar que el directorio de base de datos existe
    os.makedirs(db_directory, exist_ok=True)
    
    # Crear el nombre de la colección a partir de la materia
    collection_name = materia.lower().replace(" ", "_")

    # Inicializar embeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=ollama_url)
    
    # Crear cliente persistente
    client = chromadb.PersistentClient(path=db_directory)
    
    # Crear o recuperar el almacén de vectores
    return Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=db_directory  # Usar el directorio de base de datos principal
    )
