from pydantic import BaseModel

class GenerateRequest(BaseModel):
    context: str = "" 
    carrera: str  
    anio: str = Field(..., alias="año")
    materia: str
    unidad_competencia: str
    elemento_competencia: str
    evidencia: str
    nivel: str
    
    class Config:
        populate_by_name = True
        schema_extra = {
            "example": {
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
                "response": "{\"Titulo\": \"Resolución de ecuaciones cuadráticas\", \"Consigna\": \"Resuelve las siguientes ecuaciones cuadráticas utilizando la fórmula general.\"}"
            }
        }
