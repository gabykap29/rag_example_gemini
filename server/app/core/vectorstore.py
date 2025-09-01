from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import chromadb
import os
from app.config.config import db_directory, ollama_url


def get_vector_stores(materia):
    os.makedirs(db_directory, exist_ok=True)
    collection_name = materia.lower().replace(" ", "_")
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=ollama_url)
    client = chromadb.PersistentClient(path=db_directory)
    
    return Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=db_directory  
    )

def get_vector_store_cuestions(materia, unidad_elemento):

    os.makedirs(db_directory, exist_ok=True)
    collection_name = materia.lower().replace(" ", "_") + "_" + unidad_elemento
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=ollama_url)
    client = chromadb.PersistentClient(path=db_directory)

    return Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=db_directory 
    )