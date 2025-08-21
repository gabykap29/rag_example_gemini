from app.core.documents import retrieve_docs
from app.core.models import generate_response_stream

def generate_response(materia, unidad_tematica, evidencia, nivel):
    """
    Genera una respuesta completa consumiendo el generador de respuestas.
    """
    docs = retrieve_docs(unidad_tematica, materia)
    context = docs
    
    # Obtener el generador
    generator = generate_response_stream(context, materia, unidad_tematica, evidencia, nivel)
    
    # Consumir el generador y construir la respuesta completa
    full_response = ""
    for chunk in generator:
        full_response += chunk
    
    return full_response

