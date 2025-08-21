import chunk
from app.config.config import pdf_directory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.vectorstore import get_vector_stores
import hashlib
import os
from typing import List, Dict, Any
from langchain.schema import Document


def load_document(file_path: str) -> List[Document]:
    """Carga un documento PDF o DOCX y lo convierte en documentos para el procesamiento.
    
    Args:
        file_path: Ruta al archivo a cargar
        
    Returns:
        Lista de documentos procesados
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        loader = PDFPlumberLoader(file_path)
    elif file_extension == '.docx':
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Formato de archivo no soportado: {file_extension}. Solo se admiten .pdf y .docx")
        
    documents = loader.load()
    
    # Añadir metadatos adicionales a los documentos
    for doc in documents:
        doc.metadata["file_hash"] = get_file_hash(file_path)
        doc.metadata["file_path"] = file_path
        doc.metadata["file_extension"] = file_extension
    
    return documents

# Mantener compatibilidad con código existente
def load_pdf(file):
    return load_document(file)

def index_docs(documents, materia):
    vectorstore = get_vector_stores(materia)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100,
    )
    chunked_docs = text_splitter.split_documents(documents)
    vectorstore.add_documents(chunked_docs)
    vectorstore.persist()
    print("Documents  indexed successfully. Numbers of documents:", len(documents))

def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def is_document_already_indexed(file_path: str, materia: str) -> bool:
    """Verifica si un documento ya está indexado en la base de vectores.
    
    Args:
        file_path: Ruta al archivo a verificar
        materia: Materia o colección donde buscar
        
    Returns:
        True si el documento ya está indexado, False en caso contrario
    """
    vectorstore = get_vector_stores(materia)
    result = vectorstore.similarity_search(file_path, k=1)
    if result:
        for doc in result:
            if doc.metadata.get("file_hash") == get_file_hash(file_path):
                return True
    return False

# Mantener compatibilidad con código existente
def is_pdf_already_indexed(file_path, materia):
    return is_document_already_indexed(file_path, materia)


def retrieve_docs(query, coleccion):

    vectorstore = get_vector_stores(coleccion)

    docs = vectorstore.similarity_search(query, k=5)
    print("Retrieved documents:", len(docs), "recibido: ", query, coleccion)
    if docs:
        return docs
    else:
        return []