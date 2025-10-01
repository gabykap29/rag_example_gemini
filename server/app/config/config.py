from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

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