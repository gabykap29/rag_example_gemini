from fastapi import APIRouter, Request, File, Form, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from app.services.documents import upload_document
from app.models.documents import UploadResponse
from app.utils.logging import api_logger
import os
import time
import uuid

router = APIRouter(tags=["Documents"], prefix="/documents")

@router.post("/upload", response_model=UploadResponse, status_code=200,
            summary="Subir documento (PDF o DOCX)",
            description="Sube un documento PDF o DOCX para ser indexado y utilizado en la generación de actividades")
async def upload_file(
    file: UploadFile = File(..., description="Archivo PDF o DOCX a subir"),
    subject: str = Form(..., description="Materia o asignatura relacionada con el documento")
):
    """
    Sube un documento PDF o DOCX para ser indexado y utilizado en la generación de actividades.
    
    El documento será procesado, indexado y almacenado para su posterior uso en la generación
    de actividades educativas. El sistema extraerá el texto del documento y creará embeddings
    para su recuperación mediante búsqueda semántica.
    
    Parameters:
    - **file**: Archivo PDF o DOCX a subir (máximo 10MB)
    - **subject**: Materia o asignatura relacionada con el documento
    
    Returns:
        UploadResponse: Información sobre el resultado de la operación
        
    Raises:
        HTTPException: Si el formato del archivo no es soportado o si ocurre un error durante el procesamiento
    """
    # Generar ID único para la solicitud
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Logging de la solicitud
    api_logger.info(
        f"Solicitud de subida de documento recibida [ID: {request_id}] - "
        f"Archivo: {file.filename}, "
        f"Tamaño: {file.size / 1024:.2f} KB, "
        f"Materia: {subject}"
    )
    
    # Verificar el tamaño del archivo (máximo 10MB)
    max_size = 10 * 1024 * 1024  # 10MB en bytes
    if file.size > max_size:
        api_logger.warning(
            f"Archivo rechazado por tamaño [ID: {request_id}] - "
            f"Tamaño: {file.size / 1024:.2f} KB (máximo: 10240 KB)"
        )
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="El archivo es demasiado grande. El tamaño máximo permitido es 10MB."
        )
    
    # Verificar la extensión del archivo
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in [".pdf", ".docx"]:
        api_logger.warning(
            f"Archivo rechazado por formato [ID: {request_id}] - "
            f"Formato: {file_extension}"
        )
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Formato de archivo no soportado. Solo se admiten archivos PDF y DOCX."
        )
    
    try:
        # Procesar el documento
        result = upload_document(file, subject)
        
        # Calcular tiempo de procesamiento
        process_time = time.time() - start_time
        
        # Logging de la respuesta exitosa
        api_logger.info(
            f"Documento procesado con éxito [ID: {request_id}] - "
            f"Archivo: {file.filename}, "
            f"Mensaje: {result['message']}, "
            f"Tiempo: {process_time:.2f}s"
        )
        
        # Devolver respuesta
        return UploadResponse(
            message=result["message"],
            file_name=result["file_name"],
            file_type=result["file_type"],
            subject=result["subject"]
        )
    except ValueError as e:
        api_logger.error(
            f"Error de validación al procesar documento [ID: {request_id}] - "
            f"Error: {str(e)}"
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        api_logger.error(
            f"Error interno al procesar documento [ID: {request_id}] - "
            f"Error: {str(e)}"
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al procesar el documento: {str(e)}")
