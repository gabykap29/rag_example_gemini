from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from app.core.settings import api_key, model_gemini, ollama_url
from app.models.output_parsers import OutputParserAssistantStudent, OutpuParser
from app.core.settings import embeddings_model


# configuración de modelos
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

# configuración de modelos de embeddings
if embeddings_model == "GEMINI": 
        MODEL_EMBEDDINGS = GoogleGenerativeAIEmbeddings(
        google_api_key=api_key,
        model="models/text-embedding-004"
)
else:
        MODEL_EMBEDDINGS = OllamaEmbeddings(
        model="nomic-embed-text"
)




# configuración de modelos de salida estructurada para el asistente estudiantil
OLLAMA_CONFIG_STUDENT = ollama_model.with_structured_output(OutputParserAssistantStudent)
GEMINI_CONFIG_STUDENT = gemini_model.with_structured_output(OutputParserAssistantStudent)

# configuración de modelos de salida estructurada para el instructor
GEMINI_CONFIG_INSTRUCTOR = gemini_model.with_structured_output(OutpuParser)
OLLAMA_CONFIG_INSTRUCTOR = ollama_model.with_structured_output(OutpuParser)

