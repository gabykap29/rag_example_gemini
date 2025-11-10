from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from typing import Literal, List, Dict, Union
import os
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

load_dotenv()

api_key = os.getenv("API_KEY")

# Directorios
pdf_directory = "./documents"
db_directory = "./app/db"
log_directory = "./logs"

model_gemini = os.getenv("GEMINI_MODEL")

model_embedding_gemini = GoogleGenerativeAIEmbeddings(
    google_api_key=api_key,
    model="models/text-embedding-004"
)
model_embedding_ollama = OllamaEmbeddings(
    model="nomic-embed-text"
)

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

if os.getenv("MODEL_EMBEDDINGS") == "GEMINI_EMBEDDINGS": 
    embeddings_model = model_embedding_gemini
else: 
    embeddings_model = model_embedding_ollama

OLLAMA_CONFIG_STUDENT = ollama_model.with_structured_output(OutputParserAssistantStudent)
GEMINI_CONFIG_STUDENT = gemini_model.with_structured_output(OutputParserAssistantStudent)

GEMINI_CONFIG_INSTRUCTOR = gemini_model.with_structured_output(OutpuParser)
OLLAMA_CONFIG_INSTRUCTOR = ollama_model.with_structured_output(OutpuParser)