from ast import List
from pydantic import BaseModel


class Question(BaseModel):
    materia: str
    unidad_competencia: str
    pregunta: str

class Questions(BaseModel):
    questions: list[Question]