from fastapi import APIRouter, Request, File, Form, UploadFile
from app.services.documents import upload_pdf
from app.models.documents import UploadResponse

router = APIRouter(tags=["Documents"], prefix="/documents")

@router.post("/upload", response_model=UploadResponse, status_code=200,
            summary="Subir documento PDF",
            description="Sube un documento PDF para ser indexado y utilizado en la generación de actividades")
async def upload_file(request: Request):
    """
    Sube un documento PDF para ser indexado y utilizado en la generación de actividades.
    
    - **file**: Archivo PDF a subir
    - **subject**: Materia o asignatura relacionada con el documento
    
    Returns:
        Un mensaje de confirmación de que el archivo se ha subido correctamente
    """
    form = await request.form()
    file = form["file"]
    subject = form["subject"]
    upload_pdf(file, subject)
    return UploadResponse(message="File uploaded successfully")
