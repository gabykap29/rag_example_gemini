from app.config.config import pdf_directory
from app.core.documents import is_document_already_indexed, load_document, index_docs, retrieve_docs
import os
from typing import Dict, Any, Optional


def upload_document(file, subject) -> Dict[str, Any]:
    """Sube un documento (PDF o DOCX) y lo indexa para su uso en RAG.
    
    Args:
        file: Archivo subido (UploadFile de FastAPI)
        subject: Materia o asignatura relacionada con el documento
        
    Returns:
        Diccionario con información sobre el resultado de la operación
    """
    # Asegurar que el directorio existe
    os.makedirs(pdf_directory, exist_ok=True)
    
    # Guardar el archivo
    file_path = os.path.join(pdf_directory, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    # Obtener extensión del archivo
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension not in [".pdf", ".docx"]:
        os.remove(file_path)  # Eliminar archivo no válido
        raise ValueError(f"Formato de archivo no soportado: {file_extension}. Solo se admiten .pdf y .docx")
    
    # Verificar si ya está indexado
    if is_document_already_indexed(file_path, subject):
        return {
            "message": "Documento ya indexado previamente",
            "file_name": file.filename,
            "file_type": file_extension[1:],  # Eliminar el punto inicial
            "subject": subject
        }
    
    # Cargar e indexar el documento
    try:
        documents = load_document(file_path)
        index_docs(documents, subject)
        return {
            "message": "Documento indexado correctamente",
            "file_name": file.filename,
            "file_type": file_extension[1:],  # Eliminar el punto inicial
            "subject": subject
        }
    except Exception as e:
        # Si hay un error, eliminar el archivo y propagar la excepción
        os.remove(file_path)
        raise e

# Mantener compatibilidad con código existente
def upload_pdf(file, subject):
    return upload_document(file, subject)

#Funcion para obtener los documentos
def retrieve(query, subject): 
    documents = retrieve_docs(query, subject)
    return documents

