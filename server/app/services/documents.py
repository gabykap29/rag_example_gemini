from app.config.config import pdf_directory
from app.core.documents import is_document_already_indexed, load_document, index_docs, retrieve_docs
import os
from typing import Dict, Any
from app.utils.logging import service_logger


def upload_document(file, subject) -> Dict[str, Any]:
    """Sube un documento (PDF o DOCX) y lo indexa para su uso en RAG.
    
    Args:
        file: Archivo subido (UploadFile de FastAPI)
        subject: Materia o asignatura relacionada con el documento
        
    Returns:
        Diccionario con información sobre el resultado de la operación
    """
    service_logger.info(f"Iniciando procesamiento de documento: {file.filename} para materia: {subject}")
    
    # Asegurar que el directorio existe
    os.makedirs(pdf_directory, exist_ok=True)
    service_logger.debug(f"Directorio de almacenamiento verificado: {pdf_directory}")
    
    # Guardar el archivo
    file_path = os.path.join(pdf_directory, file.filename)
    service_logger.info(f"Guardando archivo en: {file_path}")
    
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
        service_logger.debug(f"Archivo guardado: {file_path} ({len(content)/1024:.2f} KB)")
    
    # Obtener extensión del archivo
    file_extension = os.path.splitext(file_path)[1].lower()
    service_logger.debug(f"Extensión del archivo: {file_extension}")
    
    if file_extension not in [".pdf", ".docx"]:
        service_logger.warning(f"Formato de archivo no soportado: {file_extension}. Eliminando archivo.")
        os.remove(file_path)  # Eliminar archivo no válido
        raise ValueError(f"Formato de archivo no soportado: {file_extension}. Solo se admiten .pdf y .docx")
    
    # Verificar si ya está indexado
    service_logger.info(f"Verificando si el documento ya está indexado: {file_path}")
    if is_document_already_indexed(file_path, subject):
        service_logger.info(f"Documento ya indexado previamente: {file.filename}")
        return {
            "message": "Documento ya indexado previamente",
            "file_name": file.filename,
            "file_type": file_extension[1:],  # Eliminar el punto inicial
            "subject": subject
        }
    
    # Cargar e indexar el documento
    try:
        service_logger.info(f"Cargando documento: {file_path}")
        documents = load_document(file_path)
        service_logger.info(f"Documento cargado con {len(documents)} fragmentos. Indexando...")
        
        index_docs(documents, subject)
        service_logger.info(f"Documento indexado correctamente: {file.filename}")
        
        return {
            "message": "Documento indexado correctamente",
            "file_name": file.filename,
            "file_type": file_extension[1:],  # Eliminar el punto inicial
            "subject": subject
        }
    except Exception as e:
        # Si hay un error, eliminar el archivo y propagar la excepción
        service_logger.error(f"Error al procesar documento: {file_path}. Error: {str(e)}")
        service_logger.info(f"Eliminando archivo debido al error: {file_path}")
        os.remove(file_path)
        raise e

# Mantener compatibilidad con código existente
def upload_pdf(file, subject):
    service_logger.debug(f"Llamada a función legacy upload_pdf para archivo: {file.filename}")
    return upload_document(file, subject)

#Funcion para obtener los documentos
def retrieve(query, subject): 
    service_logger.info(f"Recuperando documentos para consulta: '{query}' en materia: '{subject}'")
    documents = retrieve_docs(query, subject)
    service_logger.info(f"Recuperados {len(documents)} documentos relevantes")
    return documents

