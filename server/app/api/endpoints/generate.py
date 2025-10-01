from app.services.generate import generate_response, generate_response_assistant
from fastapi import APIRouter, Body
from app.models.generate import GenerateRequest, GenerateResponse, RequestStudent
from app.utils.logging import api_logger
import time
import uuid

router = APIRouter(tags=["Generate"], prefix="/generate")

@router.post("", response_model=GenerateResponse, status_code=200,
            summary="Generar actividad educativa",
            description="Genera una actividad educativa basada en el contexto y parámetros proporcionados")
async def generate(request: GenerateRequest = Body(...)):
    """
    Genera una actividad educativa basada en el contexto y parámetros proporcionados.

    - **materia**: Materia o asignatura
    - **unidad_competencia**: Unidad temática o tema específico
    - **evidencia**: Tipo de evidencia o actividad a generar
    - **nivel**: Nivel de dificultad
    
    Returns:
        Un objeto JSON con la actividad generada en formato estructurado
    """
    # Generar ID único para la solicitud
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Logging de la solicitud
    api_logger.info(
        f"Solicitud de generación recibida [ID: {request_id}] - "
        f"Materia: {request.materia}, "
        f"Unidad: {request.unidad_competencia}, "
        f"Evidencia: {request.evidencia}, "
        f"Nivel: {request.nivel}"
    )
    
    try:
        # Procesar la solicitud
        result = generate_response(
            request.carrera,
            request.anio,
            request.materia, 
            request.unidad_competencia, 
            request.elemento_competencia,
            request.evidencia, 
            request.nivel
        )
        if result is None:
            response, possibly_repeated, probability = None, None, None
        else:
            response, possibly_repeated, probability = result
        
        # Calcular tiempo de procesamiento
        process_time = time.time() - start_time
        
        # Logging de la respuesta exitosa
        api_logger.info(
            f"Respuesta generada con éxito [ID: {request_id}] - "
            f"Tiempo: {process_time:.2f}s"
        )
        
        return GenerateResponse(response=response, possibly_repeated = possibly_repeated, probability=probability)
    
    except Exception as e:
        # Logging de error
        api_logger.error(
            f"Error al generar respuesta [ID: {request_id}] - "
            f"Error: {str(e)}"
        )
        # Re-lanzar la excepción para que FastAPI la maneje
        raise

@router.post("/student", status_code=200)
def response_user(request: RequestStudent = Body(...)): 
    # Generar ID único para la solicitud
    request_id = str(uuid.uuid4())
    start_time = time.time()
    try:         

        api_logger.info(
            f"Solicitud de generación recibida [ID: {request_id}] - "
            f"contexto: {request.contexto}, "
            f"question: {request.question}"
        )
        
        response = generate_response_assistant(contexto=request.contexto, question=request.question)
        process_time = time.time() - start_time

        api_logger.info(
                f"Respuesta generada con éxito [ID: {request_id}] - "
                f"Tiempo: {process_time:.2f}s"
            )
        return response
    except Exception as e: 
        api_logger.error(
            f"Error al generar respuesta [ID: {request_id}] - "
            f"Error: {str(e)}"
        )
        raise