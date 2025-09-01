from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config.config import api_key
from app.config.template import custom_template
from ollama import Client, ChatResponse, chat
from app.utils.filters import filter_markdown
from app.config.config import model, ollama_url

def generate_response_stream(context, materia, unidad_tematica, evidencia, nivel, questions_list):
    if model == "OLLAMA": 
        client = Client(
            host=ollama_url,
        )
        response: ChatResponse = chat(
            model= "medicina", messages=[
                {
                    "role": "user",
                    "content": f"Materia: {materia}, Unidad_Tematica: {unidad_tematica}, Evidencia: {evidencia}, Nivel: {nivel}, Contexto: {context}, Preguntas: {questions_list}"
                }
            ], 
            stream=True,
            format="json"
        )
        for chunk in response:
            chunk = filter_markdown(chunk['message']['content'] )
            yield chunk
    else: 
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.6,
            max_tokens=2000,
            google_api_key=api_key,
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", custom_template),
            ("user", "Materia: {materia}, Unidad_Tematica: {unidad_tematica}, Evidencia: {evidencia}, Nivel: {nivel}, Contexto: {context},  Preguntas Previas: {questions_list}"),
        ])

        chain = prompt | llm | StrOutputParser()
        
        input_dict = {
            "carrera": carrera,
            "año": año,
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


