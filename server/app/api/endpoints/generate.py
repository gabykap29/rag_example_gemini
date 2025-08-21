from app.services.generate import generate_response

from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/generate")
async def generate(request: Request):
    data = await request.json()
    context = data["context"]
    materia = data["materia"]
    unidad_tematica = data["unidad_tematica"]
    evidencia = data["evidencia"]
    nivel = data["nivel"]
    response = generate_response(context, materia, unidad_tematica, evidencia, nivel)
    return {"response": response}

