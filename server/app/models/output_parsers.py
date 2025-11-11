from pydantic import BaseModel, Field, field_validator
from typing import Literal, List, Dict, Union
import json


# --- Definiciones de tipos ---
TipoDificultad = Literal["Baja", "Media", "Alta", "Muy Alta"]
OpcionKey = Literal["A", "B", "C", "D"]

# --- Clase Pydantic para el Parser ---

class OutpuParser(BaseModel):
    """
    Representa una pregunta (ítem) para una evaluación, 
    validando su estructura con Pydantic.
    """
    
    Consigna: str = Field(..., description="El texto de la pregunta.")
    Contexto: str = Field(..., description="Un texto breve que da contexto a la pregunta.")
    DificultadItem: TipoDificultad = Field(..., description="La dificultad general del ítem.")
    
    informacionNivel: List[TipoDificultad] = Field(..., description="Niveles de información asociados al ítem.")
    
    TiempoEstimado: str = Field(..., description="Tiempo estimado para resolver (ej. '01:30'). SOLO MINUTOS Y SEGUNDOS.")
    
    Opciones: Dict[OpcionKey, str] = Field(..., description="Diccionario de opciones con sus textos.")
    
    VectorNivel: Dict[OpcionKey, List[TipoDificultad]] = Field(..., 
        description="Mapeo de los niveles de dificultad asociados a cada vector/opción.")
    
    RespuestaCorrecta: OpcionKey = Field(..., description="La clave de la opción correcta (A, B, C o D).")
    
    @field_validator('Opciones', mode='before')
    @classmethod
    def parse_opciones(cls, v: Union[str, Dict]) -> Dict:
        """Convierte strings a diccionarios si es necesario."""
        if isinstance(v, str):
            try:
                # Intentar parsear como JSON
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                # Si falla, intentar eval como última opción
                try:
                    return eval(v)
                except Exception:
                    raise ValueError(f"No se puede parsear Opciones: {v}")
        return v
    
    @field_validator('VectorNivel', mode='before')
    @classmethod
    def parse_vector_nivel(cls, v: Union[str, Dict]) -> Dict:
        """Convierte strings a diccionarios si es necesario."""
        if isinstance(v, str):
            try:
                # Intentar parsear como JSON
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                # Si falla, intentar eval como última opción
                try:
                    return eval(v)
                except Exception:
                    raise ValueError(f"No se puede parsear VectorNivel: {v}")
        return v


class OutputParserAssistantStudent(BaseModel):
    contexto: str
    pregunta: str
    pista: str