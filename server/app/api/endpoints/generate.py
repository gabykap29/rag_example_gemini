from app.services.generate import generate_response
from fastapi import APIRouter, Request, Body
from app.models.generate import GenerateRequest, GenerateResponse
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Generate"], prefix="/generate")

@router.post("", response_model=GenerateResponse, status_code=200,
            summary="Generar actividad educativa",
            description="Genera una actividad educativa basada en el contexto y parámetros proporcionados")
async def generate(request: GenerateRequest = Body(...)):
    """
    Genera una actividad educativa basada en el contexto y parámetros proporcionados.

    - **materia**: Materia o asignatura
    - **unidad_tematica**: Unidad temática o tema específico
    - **evidencia**: Tipo de evidencia o actividad a generar
    - **nivel**: Nivel de dificultad
    
    Returns:
        Un objeto JSON con la actividad generada en formato estructurado
    """
    response = generate_response(
        request.carrera,
        request.anio,
        request.materia, 
        request.unidad_competencia, 
        request.elemento_competencia,
        request.evidencia, 
        request.nivel,
    )
    return GenerateResponse(response=response)

