from pydantic import BaseModel
from typing import List, Optional

class GenerateRequest(BaseModel):
    context: str = "" 
    materia: str
    unidad_tematica: str
    evidencia: str
    nivel: str
    
    class Config:
        schema_extra = {
            "example": {
                "context": "Contenido del documento o contexto para generar la actividad",
                "materia": "Matemáticas",
                "unidad_tematica": "Álgebra",
                "evidencia": "Examen",
                "nivel": "Medio"
            }
        }

class GenerateResponse(BaseModel):
    response: str
    
    class Config:
        schema_extra = {
            "example": {
                "response": "{\"Titulo\": \"Resolución de ecuaciones cuadráticas\", \"Consigna\": \"Resuelve las siguientes ecuaciones cuadráticas utilizando la fórmula general.\", ...}"
            }
        }