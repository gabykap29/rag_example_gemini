from app.core.documents import index_questions, retrieve_docs, retrieve_questions
from app.core.models import generate_response as llm
from app.utils.logging import service_logger
from app.utils.probability import score_to_probability
from app.core.models import generate_response_student
import time

def generate_response(carrera: str, anio: str, materia: str, unidad_competencia: str, 
                     elemento_competencia: str, evidencia: str, nivel: str):
    """
    Genera una respuesta completa, verificando duplicados y re-intentando si es necesario.
    Envía al modelo las preguntas ya generadas para evitar repeticiones.
    
    Returns:
        tuple: (respuesta_completa, posible_repeticion, probabilidad_similitud)
    """
    start_time = time.time()
    service_logger.info(
        f"Iniciando generación - Materia: {materia}, Unidad: {unidad_competencia}, "
        f"Evidencia: {evidencia}, Nivel: {nivel}"
    )
    
    service_logger.info(f"Recuperando documentos para unidad: {unidad_competencia}")
    context = retrieve_docs(unidad_competencia, materia)
    service_logger.info(f"Recuperados {len(context)} documentos relevantes")

    tries = 0
    max_tries = 3
    questions_list = "PREGUNTAS YA GENERADAS:\n"

    while tries < max_tries:
        iteration_start = time.time()
        tries += 1
        service_logger.info(f"Intento #{tries} de generación de respuesta")
        
        response = llm(
            carrera, anio, materia, unidad_competencia, elemento_competencia, 
            evidencia, nivel, context, questions_list
        )
        
        service_logger.info("Verificando duplicados en base de datos")
        questions, score = retrieve_questions(response.Consigna, materia, unidad_competencia)

        probability = score_to_probability(score=score)


        if probability < 70:  
            service_logger.info("Respuesta única encontrada, indexando")
            index_questions(response.Consigna, materia, unidad_competencia)
            
            total_time = time.time() - start_time
            service_logger.info(f"Generación completada en {total_time:.2f}s tras {tries} intentos")
            return response, False, probability
        
        else:
            # Agregar pregunta duplicada a la lista para el próximo intento
            questions_list += f"{questions}\n\n"
            iteration_time = time.time() - iteration_start
            service_logger.warning(
            f"Duplicado encontrado (similaridad: {probability:.1f}%) en intento #{tries}. "
            f"Tiempo: {iteration_time:.2f}s. Reintentando..."
            )
            # Se alcanzó el límite máximo de intentos
            service_logger.warning(f"Límite de {max_tries} intentos alcanzado. Retornando última respuesta")
            total_time = time.time() - start_time
            service_logger.info(f"Generación completada en {total_time:.2f}s tras {tries} intentos")
            
            return response, True, probability

def generate_response_assistant(contexto: str, question: str): 
    start_time = time.time()
    service_logger.info(
        f"Iniciando generación de respuesta de asistente - Contexto: {len(contexto)} chars, Pregunta: {question}"
    )
    try:

        service_logger.info("Iniciando streaming desde generate_response_student")
        response = generate_response_student(contexto=contexto, question=question)
        
        total_time = time.time() - start_time
        service_logger.info(f"Generación de respuesta de asistente completada en {total_time:.2f}s")

        return response
        
    except Exception as e:
        service_logger.error(f"Error en generate_response_assistant: {str(e)}")
        total_time = time.time() - start_time
        service_logger.error(f"Falló la generación tras {total_time:.2f}s")
        raise