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
ollama_url = os.getenv("OLLAMA_URL")

# Configuración de logging
log_level = os.getenv("LOG_LEVEL", "INFO")
log_to_file = os.getenv("LOG_TO_FILE", "True").lower() == "true"
