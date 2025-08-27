from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config.config import api_key
from app.config.template import custom_template
from ollama import Client, ChatResponse, chat
from app.utils.filters import filter_markdown
from app.config.config import model, ollama_url

def generate_response_stream(context, carrera, año, materia, unidad_competencia, elemento_competencia, evidencia, nivel):
    if model == "OLLAMA": 
        client = Client(
            host=ollama_url,
        )
        response: ChatResponse = chat(
            model= "medicina", messages=[
                {
                    "role": "user",
                    "content": f"Carrera: {carrera}, Año: {año}, Materia: {materia}, Unidad_Competencia: {unidad_competencia}, Elemento_Competencia: {elemento_competencia}, Evidencia: {evidencia}, Nivel: {nivel}, Contexto: {context}"
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
            temperature=0.4,
            max_tokens=2000,
            top_p=0.9,
            google_api_key=api_key,
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", custom_template),
            ("user", "Carrera: {carrera}, Año: {año}, Materia: {materia}, Unidad_Competencia: {unidad_competencia}, Elemento_Competencia: {elemento_competencia}, Evidencia: {evidencia}, Nivel: {nivel}, Contexto: {context}"),
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
            "context": context
        }
        print("Input dictionary:", input_dict)
        
        for chunk in chain.stream(input_dict):
            chunk = filter_markdown(chunk)
            yield chunk


