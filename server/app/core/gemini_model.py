from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config.config import api_key
from app.config.template import custom_template

def generate_response_stream(context, materia, unidad_tematica, evidencia, nivel):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.4,
        max_tokens=2000,
        top_p=0.9,
        google_api_key=api_key,
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", custom_template),
        ("user", "Materia: {materia}, Unidad_Tematica: {unidad_tematica}, Evidencia: {evidencia}, Nivel: {nivel}, Contexto: {context}"),
    ])

    chain = prompt | llm | StrOutputParser()
    
    input_dict = {
        "materia": materia,
        "unidad_tematica": unidad_tematica,
        "evidencia": evidencia,
        "nivel": nivel,
        "context": context
    }
    print("Input dictionary:", input_dict)
    
    for chunk in chain.stream(input_dict):
        yield chunk
