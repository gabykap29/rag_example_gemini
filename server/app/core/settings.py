from dotenv import load_dotenv
import os

load_dotenv()
# -- configuración de variables de entorno -- #
api_key = os.getenv("API_KEY")
model_gemini = os.getenv("GEMINI_MODEL")

# -- directorios -- #
pdf_directory = "./documents"
db_directory = "./app/db"
log_directory = "./logs"

# -- configuración del modelo de Gemini a utilizar -- #
if os.getenv("GEMINI_MODEL") is None: 
    model_gemini = "gemini-2.0-flash"
else: 
    model_gemini = os.getenv("GEMINI_MODEL")

# -- configuración de Ollama -- #
if os.getenv("OLLAMA_URL"): 
    ollama_url = os.getenv("OLLAMA_URL") 
else: 
    ollama_url = "http://localhost:11434"

# -- configuración de modelos -- #
model = os.getenv("MODEL")
model_name = os.getenv("MODEL_NAME")

# -- configuración de logging -- #
log_level = os.getenv("LOG_LEVEL", "INFO")
log_to_file = os.getenv("LOG_TO_FILE", "True").lower() == "true"

# -- configuración de modelos de embeddings -- #

if os.getenv("MODEL_EMBEDDINGS") == "GEMINI_EMBEDDINGS": 
    embeddings_model = "GEMINI"
else: 
    embeddings_model = "OLLAMA"

# -- configuración del modelo personalizado de ollama (Solo si se esta utilizando ollama) -- #
if os.getenv("MODEL_USER_OLLAMA") is None:
    model_student = "medicina_usuario"
else:
    model_student = os.getenv("MODEL_USER_OLLAMA")

