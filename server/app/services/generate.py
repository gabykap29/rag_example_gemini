from app.core.documents import index_questions, retrieve_docs, retrieve_questions
from app.core.models import generate_response_stream
from app.utils.filters import filtrar_consigna
from app.utils.logging import service_logger
import time

def generate_response(carrera: str, anio:str, materia:str, unidad_competencia:str, elemento_competencia:str, evidencia:str, nivel:str):
    """
    Genera una respuesta completa consumiendo el generador de respuestas.
    Si la pregunta ya existe en la base, vuelve a generar hasta obtener una nueva.
    """
    start_time = time.time()
    service_logger.info(
        f"Iniciando generación de respuesta - "
        f"Materia: {materia}, "
        f"Unidad: {unidad_competencia}, "
        f"Evidencia: {evidencia}, "
        f"Nivel: {nivel}"
    )
    
    service_logger.info(f"Recuperando documentos relevantes para unidad: {unidad_competencia} en materia: {materia}")
    context = retrieve_docs(unidad_competencia, materia)
    service_logger.info(f"Recuperados {len(context)} documentos relevantes")

    tries = 0
    questions_list = "PREGUNTAS YA GENERADAS: \n"

    while True:
        iteration_start = time.time()
        tries += 1
        service_logger.info(f"Intento #{tries} de generación de respuesta")
        possibly_repeated = False
        
        # Generar respuesta
        service_logger.info("Iniciando stream de generación de respuesta")
        chunks = []
        for chunk in generate_response_stream(
            carrera, anio, materia, unidad_competencia, elemento_competencia, evidencia, nivel, context, questions_list
        ):
            chunks.append(chunk)
        
        full_response = "".join(chunks)
        response_filter = filtrar_consigna(full_response)
        service_logger.debug(f"Respuesta generada con {len(full_response)} caracteres")
        
        service_logger.info("Verificando si la respuesta ya existe en la base de datos")
        questions = retrieve_questions(response_filter, materia, unidad_competencia)

        if len(questions) == 0:  
            service_logger.info("Respuesta única encontrada, indexando en la base de datos")
            index_questions(response_filter, materia, unidad_competencia)
            
            total_time = time.time() - start_time
            service_logger.info(f"Generación completada en {total_time:.2f}s después de {tries} intentos")
            return full_response, possibly_repeated
        else:
            iteration_time = time.time() - iteration_start
            service_logger.warning(
                f"Respuesta duplicada encontrada en intento #{tries}. "
                f"Tiempo de iteración: {iteration_time:.2f}s. "
                f"Intentando nuevamente..."
            )
            questions_list = questions_list + response_filter

            if tries >= 2:
                possibly_repeated = True
                service_logger.warning(
                    f"Alcanzado límite máximo de intentos (3). "
                    f"Retornando respuesta a pesar de posible duplicación."
                )
                total_time = time.time() - start_time
                service_logger.info(f"Generación completada en {total_time:.2f}s después de {tries} intentos")

                return full_response, possibly_repeated

