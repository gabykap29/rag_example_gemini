import asyncio
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

async def process_questions(question):

    try:

        _, score = retrieve_questions(question.pregunta, question.materia, question.unidad_competencia)
        if score > 400:
            index_questions(question.pregunta, question.materia, question.unidad_competencia)
            service_logger.info(f"Pregunta guardada en bd vectorial {question}")
            return {"pregunta": question.pregunta, "status": "guardada"}
        else:
            service_logger.info(f"La pregunta ya se encuentra en la base de datos... omitida")
            return {"pregunta": question.pregunta, "status": "omitida"}
    except Exception as e:
        service_logger.error(f"Error procesando {question.pregunta}: {e}")
        return {"pregunta": question.pregunta, "status": "error"}

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
        
        result = await asyncio.gather(
            *[process_questions(q) for q in request.questions],
            return_exceptions=True
        )
        guardadas = sum(1 for r in result if r.get("status") == "guardada")
        omitidas = sum(1 for r in result if r.get("status") == "omitida")
        errores  = sum(1 for r in result if r.get("status") == "error")

        return JSONResponse(
            content={
                "guardadas": guardadas,
                "omitidas": omitidas,
                "errores": errores,
                "total": len(result)
            },
            status_code=201
        )
    except Exception as e:
        return JSONResponse(
            content=f"Error al procesar las preguntas, {e}",
            status_code=500
        )
    finally:
        total_time = time.time() - start_time
        service_logger.info(f"Generación completada en {total_time:.2f}")
        