from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import chromadb
from config.config import db_directory


def get_vector_stores(materia):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    client = chromadb.PersistentClient(path=db_directory)
    return Chroma(
        client=client,
        collection_name=materia.lower().replace(" ", "_"),
        embedding_function=embeddings,
    )
