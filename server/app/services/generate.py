from app.core.documents import retrieve_docs
from app.core.gemini_model import generate_response_stream

def generate_response(context, materia, unidad_tematica, evidencia, nivel):

    docs = retrieve_docs(context, materia)
    context = docs
    return generate_response_stream(context, materia, unidad_tematica, evidencia, nivel)

