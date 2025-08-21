from app.config.config import pdf_directory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from app.core.vectorstore import get_vector_stores
import hashlib


def load_pdf(file):
    loader = PDFPlumberLoader(file)
    documents = loader.load()
    return documents

def index_docs(documents, materia):
    vectorstore = get_vector_stores(materia)
    vectorstore.add_documents(documents)
    vectorstore.persist()
    print("Documents  indexed successfully. Numbers of documents:", len(documents))

def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def is_pdf_already_indexed(file_path, materia):
    vectorstore = get_vector_stores(materia)
    result = vectorstore.similarity_search(file_path, k=1)
    if result:
        for doc in result:
            if doc.metadata.get("file_hash") == get_file_hash(file_path):
                return True
    return False


def retrieve_docs(query, coleccion):
    vectorstore = get_vector_stores(coleccion)
    docs = vectorstore.similarity_search(query, k=5)
    print("Retrieved documents:", len(docs))
    if docs:
        return docs
    else:
        return []