from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.utils.logging import api_logger
from app.models.questions import Questions
from app.utils.logging import service_logger
from app.core.documents import retrieve_questions, index_questions
import os
import time
import uuid

router = APIRouter(tags=["Questions"], prefix="/questions")

@router.post("", status_code=200, summary="Embedding de preguntas cargadas manualmente",
             description="Aqui se recibe las preguntas cargadas manualmente")
async def questions(request: Questions = Body(...)):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    api_logger.info(
        f"Solicitud de generación recibida [ID: {request_id}] - "
        f"Preguntas recibidas: {len(request.questions)}, "
    )
    
    try:
        skipped_questions = 0
        total = len(request.questions)
        if total < 1: 
            return JSONResponse(
                content="Debe enviar por lo menos 1 pregunta",
                status_code=422
            )
        for question in request.questions:
            _, score = retrieve_questions(question.pregunta, question.materia, question.unidad_competencia)
            if score > 400:
                index_questions(question.pregunta, question.materia, question.unidad_competencia)
                service_logger.info(f"Pregunta guardada en bd vectorial {question}")
            else:
                skipped_questions += 1
                service_logger.info(f"La pregunta ya se encuentra en la base de datos... omitidas: {skipped_questions}")
        return JSONResponse(
            content= f"Se completo la verificacion, total de preguntas guardadas: { total - skipped_questions} de {total}",
            status_code=201
        )
    except Exception as e:
        service_logger.error(f"Error encontrado {e}")
        return JSONResponse(
            content= f"Error al procesar las preguntas, {e}",
            status_code=500
        )
    finally:
        total_time = time.time() - start_time
        service_logger.info(f"Generación completada en {total_time:.2f}")