import chunk
from app.config.config import pdf_directory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.vectorstore import get_vector_store_cuestions
from app.core.vectorstore import get_vector_stores
import hashlib
import os
import time
from typing import List, Dict, Any
from langchain.schema import Document
from app.utils.logging import core_logger


def load_document(file_path: str) -> List[Document]:
    """Carga un documento PDF o DOCX y lo convierte en documentos para el procesamiento.
    
    Args:
        file_path: Ruta al archivo a cargar
        
    Returns:
        Lista de documentos procesados
    """
    start_time = time.time()
    core_logger.info(f"Iniciando carga de documento: {file_path}")
    
    file_extension = os.path.splitext(file_path)[1].lower()
    core_logger.debug(f"Extensión del archivo: {file_extension}")
    
    if file_extension == '.pdf':
        core_logger.info(f"Cargando documento PDF con PDFPlumberLoader: {file_path}")
        loader = PDFPlumberLoader(file_path)
    elif file_extension == '.docx':
        core_logger.info(f"Cargando documento DOCX con Docx2txtLoader: {file_path}")
        loader = Docx2txtLoader(file_path)
    else:
        core_logger.error(f"Formato de archivo no soportado: {file_extension}")
        raise ValueError(f"Formato de archivo no soportado: {file_extension}. Solo se admiten .pdf y .docx")
    
    try:    
        core_logger.debug(f"Ejecutando loader.load() para {file_path}")
        documents = loader.load()
        core_logger.info(f"Documento cargado con éxito: {len(documents)} páginas/secciones")
        
        # Añadir metadatos adicionales a los documentos
        file_hash = get_file_hash(file_path)
        core_logger.debug(f"Hash calculado para el archivo: {file_hash[:8]}...")
        
        for doc in documents:
            doc.metadata["file_hash"] = file_hash
            doc.metadata["file_path"] = file_path
            doc.metadata["file_extension"] = file_extension
        
        process_time = time.time() - start_time
        core_logger.info(f"Documento procesado en {process_time:.2f}s: {file_path}")
        return documents
    except Exception as e:
        core_logger.error(f"Error al cargar documento {file_path}: {str(e)}")
        raise

# Mantener compatibilidad con código existente
def load_pdf(file):
    core_logger.debug(f"Llamada a función legacy load_pdf: {file}")
    return load_document(file)

def index_docs(documents, materia):
    start_time = time.time()
    core_logger.info(f"Indexando {len(documents)} documentos para materia: {materia}")
    vectorstore = get_vector_stores(materia)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 100,
    )
    core_logger.debug(f"Dividiendo documentos con chunk_size=1000, chunk_overlap=100")
    chunked_docs = text_splitter.split_documents(documents)
    core_logger.info(f"Documentos divididos en {len(chunked_docs)} fragmentos")
    
    core_logger.debug(f"Añadiendo documentos al vector store para materia: {materia}")
    vectorstore.add_documents(chunked_docs)
    core_logger.debug(f"Persistiendo vector store para materia: {materia}")
    vectorstore.persist()
    
    process_time = time.time() - start_time
    core_logger.info(f"Indexación completada en {process_time:.2f}s para materia: {materia}")


def get_file_hash(file_path):
    core_logger.debug(f"Calculando hash para archivo: {file_path}")
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            buf = f.read()
            hasher.update(buf)
        hash_value = hasher.hexdigest()
        core_logger.debug(f"Hash calculado: {hash_value[:8]}...")
        return hash_value
    except Exception as e:
        core_logger.error(f"Error al calcular hash para {file_path}: {str(e)}")
        raise

def is_document_already_indexed(file_path: str, materia: str) -> bool:
    """Verifica si un documento ya está indexado en la base de vectores.
    
    Args:
        file_path: Ruta al archivo a verificar
        materia: Materia o colección donde buscar
        
    Returns:
        True si el documento ya está indexado, False en caso contrario
    """
    start_time = time.time()
    core_logger.info(f"Verificando si el documento ya está indexado: {file_path} en materia: {materia}")
    
    try:
        vectorstore = get_vector_stores(materia)
        core_logger.debug(f"Realizando búsqueda de similitud para verificar indexación")
        result = vectorstore.similarity_search(file_path, k=1)
        
        if result:
            file_hash = get_file_hash(file_path)
            for doc in result:
                doc_hash = doc.metadata.get("file_hash")
                core_logger.debug(f"Comparando hashes - Actual: {file_hash[:8]}... vs Encontrado: {doc_hash[:8] if doc_hash else 'None'}...")
                
                if doc_hash == file_hash:
                    process_time = time.time() - start_time
                    core_logger.info(f"Documento ya indexado (verificado en {process_time:.2f}s): {file_path}")
                    return True
        
        process_time = time.time() - start_time
        core_logger.info(f"Documento no indexado previamente (verificado en {process_time:.2f}s): {file_path}")
        return False
    except Exception as e:
        core_logger.error(f"Error al verificar indexación: {str(e)}")
        raise

# Mantener compatibilidad con código existente
def is_pdf_already_indexed(file_path, materia):
    core_logger.debug(f"Llamada a función legacy is_pdf_already_indexed: {file_path}")
    return is_document_already_indexed(file_path, materia)


def retrieve_docs(query, coleccion):
    start_time = time.time()
    core_logger.info(f"Recuperando documentos para consulta en colección: {coleccion}")
    core_logger.debug(f"Query: '{query[:50]}...' (truncada)")
    
    try:
        vectorstore = get_vector_stores(coleccion)
        docs = vectorstore.similarity_search(query, k=5)
        
        process_time = time.time() - start_time
        if docs:
            core_logger.info(f"Recuperados {len(docs)} documentos en {process_time:.2f}s")
            return docs
        else:
            core_logger.warning(f"No se encontraron documentos relevantes para la consulta en {process_time:.2f}s")
            return []
    except Exception as e:
        core_logger.error(f"Error al recuperar documentos: {str(e)}")
        raise


def retrieve_questions(query, materia, unidad_tematica):
    start_time = time.time()
    core_logger.info(f"Verificando preguntas similares - Materia: {materia}, Unidad: {unidad_tematica}")
    core_logger.debug(f"Query: '{query[:50]}...' (truncada)")
    
    try:
        vectorstore = get_vector_store_cuestions(materia, unidad_tematica)
        docs = vectorstore.similarity_search_with_score(query, k=10)
        
        process_time = time.time() - start_time
        if docs and docs[0][1] < 500:
            scores = docs[0][1]
            core_logger.info(f"Encontradas {len(docs)} preguntas similares en {process_time:.2f}s. Scores: {scores}")
            return docs, scores
        else:
            core_logger.info(f"No se encontraron preguntas similares en {process_time:.2f}s")
            return [], 0  
    except Exception as e:
        core_logger.error(f"Error al recuperar preguntas: {str(e)}")
        return [], 0    


def index_questions(documents, materia, unidad_tematica):
    start_time = time.time()
    core_logger.info(f"Indexando nueva pregunta - Materia: {materia}, Unidad: {unidad_tematica}")
    core_logger.debug(f"Contenido: '{documents[:50]}...' (truncado)")
    
    try:
        vectorstore = get_vector_store_cuestions(materia, unidad_tematica)
        vectorstore.add_documents([Document(page_content=documents)])
        vectorstore.persist()
        
        process_time = time.time() - start_time
        core_logger.info(f"Pregunta indexada correctamente en {process_time:.2f}s")
    except Exception as e:
        core_logger.error(f"Error al indexar pregunta: {str(e)}")
        raise