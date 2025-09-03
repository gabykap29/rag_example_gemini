from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

# Directorios
pdf_directory = "./documents"
db_directory = "./app/db"
log_directory = "./logs"

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
