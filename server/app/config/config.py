from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Dict, Literal
import os


TipoDificultad = Literal["Baja", "Media", "Alta", "Muy Alta"]

# De igual forma, la respuesta correcta debe ser una de las claves
OpcionKey = Literal["A", "B", "C", "D"]

# --- Clase Principal con BaseModel ---

class OutpuParser(BaseModel):
    """
    Representa una pregunta (ítem) para una evaluación, 
    validando su estructura con Pydantic.
    """
    Consigna: str
    Contexto: str
    DificultadItem: TipoDificultad
    TiempoEstimado: str 
    Opciones: str
    VectorNivel: str
    RespuestaCorrecta: OpcionKey

load_dotenv()

api_key = os.getenv("API_KEY")

# Directorios
pdf_directory = "./documents"
db_directory = "./app/db"
log_directory = "./logs"

model_gemini = os.getenv("GEMINI_MODEL")

if os.getenv("GEMINI_MODEL") is None: 
    model_gemini = "gemini-2.0-flash"
else: 
    model_gemini = os.getenv("GEMINI_MODEL")


class OutputParserAssistantStudent(BaseModel):
    contexto: str
    pregunta: str
    pista:str

# Configuración de modelos
model = os.getenv("MODEL")
model_name = os.getenv("MODEL_NAME")

if os.getenv("OLLAMA_URL"): 
    ollama_url = os.getenv("OLLAMA_URL") 
else: 
    ollama_url = "http://localhost:11434"
# Configuración de logging
log_level = os.getenv("LOG_LEVEL", "INFO")
log_to_file = os.getenv("LOG_TO_FILE", "True").lower() == "true"

if os.getenv("MODEL_USER_OLLAMA") is None:
    model_student = "medicina_usuario"
else:
    model_student = os.getenv("MODEL_USER_OLLAMA")

gemini_model = ChatGoogleGenerativeAI(
            model=model_gemini,
            temperature=0.3,
            max_tokens=2000,
            google_api_key=api_key,
        )

ollama_model = ChatOllama(
            base_url= ollama_url,
            model= "gpt-oss:20b-cloud",
            temperature=0.5
)

OLLAMA_CONFIG_STUDENT = ollama_model.with_structured_output(OutputParserAssistantStudent)
GEMINI_CONFIG_STUDENT = gemini_model.with_structured_output(OutputParserAssistantStudent)

GEMINI_CONFIG_INSTRUCTOR = gemini_model.with_structured_output(OutpuParser)
OLLAMA_CONFIG_INSTRUCTOR = ollama_model.with_structured_output(OutpuParser)