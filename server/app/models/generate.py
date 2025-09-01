from pydantic import BaseModel, Field

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
                "context": "Contenido del documento o contexto para generar la actividad",
                "carrera": "Medicina",
                "año": "1er Año",
                "materia": "Anatomía",
                "unidad_competencia": "Sistema Musculoesquelético",
                "elemento_competencia": "Arquitectura Ósea",
                "evidencia": "Conocimiento",
                "nivel": "Media"
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
