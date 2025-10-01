from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config.config import api_key
from app.config.template import custom_template, user_template
from ollama import Client, ChatResponse, chat
from app.utils.filters import filter_markdown
from app.config.config import model, ollama_url
from app.config.config import model_student

def generate_response_stream(carrera, anio, materia, unidad_competencia, elemento_competencia, evidencia, nivel, context, questions_list):
    if model == "OLLAMA": 
        Client(
            host=ollama_url,
        )
        response: ChatResponse = chat(
            model= "medicina", messages=[
                {
                    "role": "user",
                    "content": f"Carrera: {carrera}, Año: {anio}, Materia: {materia}, Unidad_Competencia: {unidad_competencia}, Elemento_Competencia: {elemento_competencia}, Evidencia: {evidencia}, Nivel: {nivel}, Contexto: {context}, Preguntas: {questions_list}"
                }
            ], 
            format="json"
        )
        for chunk in response:
            chunk = filter_markdown(chunk['message']['content'] )
            yield chunk
    else: 
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3,
            max_tokens=2000,
            google_api_key=api_key,
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", custom_template),
            ("user", "Carrera: {carrera}, Año: {anio}, Materia: {materia}, Unidad_Competencia: {unidad_competencia}, Elemento_Competencia: {elemento_competencia}, Evidencia: {evidencia}, Nivel: {nivel}, Contexto: {context},  Preguntas Previas: {questions_list}"),
        ])

        chain = prompt | llm | StrOutputParser()
        
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
        
        for chunk in chain.stream(input_dict):
            chunk = filter_markdown(chunk)
            yield chunk


def generate_response_student(contexto: str, question: str): 
    try: 
        if model == "OLLAMA":
            Client(host=ollama_url)
            response = chat(
                model=model_student or "medicina_usuario",
                messages=[
                    {
                        "role": "user",
                        "content": f"question: {question}, context: {contexto}"
                    }
                ],
                stream=True
            )
            for chunk in response:
                yield chunk["message"]["content"]
            
        else:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.3,
                max_tokens=2000,
                google_api_key=api_key,
            )
            

            prompt = ChatPromptTemplate.from_messages([
                ("system", user_template),
                ("user", "Contexto: {contexto}\nPregunta: {pregunta}"),
            ])

            chain = prompt | llm | StrOutputParser()
            
            input_dict = {
                "contexto": contexto,
                "pregunta": question
            }
            
            for chunk in chain.stream(input_dict):
                chunk = filter_markdown(chunk)
                yield chunk
    except Exception as e: 
        # Para generadores, necesitamos usar yield en lugar de return
        yield f"Error al obtener la respuesta del modelo: {e}"