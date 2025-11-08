from langchain_core.prompts import ChatPromptTemplate
from app.config.template import custom_template, user_template
from app.config.config import GEMINI_CONFIG_STUDENT, OLLAMA_CONFIG_STUDENT, model, OLLAMA_CONFIG_INSTRUCTOR
from app.config.config import GEMINI_CONFIG_INSTRUCTOR





def generate_response(carrera, anio, materia, unidad_competencia, elemento_competencia, evidencia, nivel, context, questions_list):
    prompt = ChatPromptTemplate.from_messages([
            ("system", custom_template),
            ("user", "Carrera: {carrera}, Año: {anio}, Materia: {materia}, Unidad_Competencia: {unidad_competencia}, Elemento_Competencia: {elemento_competencia}, Evidencia: {evidencia}, Nivel: {nivel}, Contexto: {context},  Preguntas Previas: {questions_list}"),
        ])

    input_dict = {
            "carrera": carrera,
            "anio": anio,
            "materia": materia,
            "unidad_competencia": unidad_competencia,
            "elemento_competencia":elemento_competencia,
            "evidencia": evidencia,
            "nivel": nivel,
            "context": context,
            "questions_list": questions_list
        }
        
    if model == "OLLAMA": 

        chain = prompt | OLLAMA_CONFIG_INSTRUCTOR
        response = chain.invoke()
        return response
    else: 

        prompt = ChatPromptTemplate.from_messages([
            ("system", custom_template),
            ("user", "Carrera: {carrera}, Año: {anio}, Materia: {materia}, Unidad_Competencia: {unidad_competencia}, Elemento_Competencia: {elemento_competencia}, Evidencia: {evidencia}, Nivel: {nivel}, Contexto: {context},  Preguntas Previas: {questions_list}"),
        ])

        chain = prompt | GEMINI_CONFIG_INSTRUCTOR
        
        input_dict = {
            "carrera": carrera,
            "anio": anio,
            "materia": materia,
            "unidad_competencia": unidad_competencia,
            "elemento_competencia":elemento_competencia,
            "evidencia": evidencia,
            "nivel": nivel,
            "context": context,
            "questions_list": questions_list
        }
        
        response = chain.invoke(input_dict)
        return response
        


def generate_response_student(contexto: str, question: str): 

    prompt = ChatPromptTemplate.from_messages([
        ("system", user_template),
        ("user", "Contexto: {contexto}\nPregunta: {pregunta}"),
    ])
            
    input_dict = {
        "contexto": contexto,
        "pregunta": question
    }
    try: 
        if model == "OLLAMA":
            chain = prompt | OLLAMA_CONFIG_STUDENT
            response = chain.invoke()
            return response    
        else:            

            chain = prompt | GEMINI_CONFIG_STUDENT
            response = chain.invoke(input_dict)

            return response
            
    except Exception as e: 
        raise Exception(f"Error al obtener la respuesta del modelo: {e}");