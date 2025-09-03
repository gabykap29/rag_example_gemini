import streamlit as st
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import chromadb
import os
import hashlib

load_dotenv()
custom_template = """
Actúa como asistente educativo que genera preguntas de opción múltiple adaptativas.

INPUTS:
- Materia
- Unidad Temática
- Evidencia: Conocimiento | Procedimiento | Producto
- Nivel: 1=Basico-Bajo | 2=Basico | 3=Satisfactorio | 4=Avanzado

OUTPUT:
- SOLO JSON válido con esta estructura:

{{
  "Titulo": "string ≤80",
  "Consigna": "pregunta clara",
  "Contexto": "string ≤200",
  "Dificultad": "Basico-Bajo" | "Basico" | "Medio" | "Alto",
  "TiempoEstimado": "MM:SS (01:00-02:00)",
  "VectorNivelOpciones": {{
    "OpcionA": ["Bajo", "Medio", "Alto", "Alto"],
    "OpcionB": ["Medio", "Medio", "Bajo", "Alto"],
    "OpcionC": ["Alto", "Bajo", "Medio", "Medio"],
    "OpcionD": ["Medio", "Alto", "Bajo", "Bajo"]
  }},
  "Opciones": {{ "A": "str", "B": "str", "C": "str", "D": "str" }},
  "RespuestaCorrecta": "A"|"B"|"C"|"D"
}}

REGLAS:
- Una única respuesta correcta, 3 distractores plausibles.
- Lenguaje acorde al nivel.
- Consigna = pregunta directa alineada con la evidencia.
- Contexto breve y realista.
- Opciones similares en longitud y sin pistas.
"""


pdf_directory = "./data"
db_directory = "./db"

if not os.path.exists(db_directory):
    os.makedirs(db_directory)
if not os.path.exists(pdf_directory):
    os.makedirs(pdf_directory)


def get_vector_stores(materia):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    client = chromadb.PersistentClient(path=db_directory)
    return Chroma(
        client=client,
        collection_name=materia.lower().replace(" ", "_"),
        embedding_function=embeddings,
    )



def retrieve_docs(query, coleccion):
    vectorstore = get_vector_stores(coleccion)
    docs = vectorstore.similarity_search(query, k=5)
    if docs:
        return docs
    else:
        return []

def upload_pdf(file):
    with open(pdf_directory + file.name, "wb") as f:
        f.write(file.getbuffer())
        
def load_pdf(file):
    loader = PDFPlumberLoader(file)
    documents = loader.load()
    return documents

def text_splitter(documents, course_name):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )    
    chunks = text_splitter.split_documents(documents)
    if course_name:
        for _, doc in enumerate(chunks):
            doc.metadata["course_name"] = course_name
    return chunks


def index_docs(documents, materia):
    vectorstore = get_vector_stores(materia)
    vectorstore.add_documents(documents)
    vectorstore.persist()

def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def is_pdf_already_indexed(file_path, materia):
    vectorstore = get_vector_stores(materia)
    result = vectorstore.similarity_search(file_path, k=1)
    if result:
        for doc in result:
            if doc.metadata.get("file_hash") == get_file_hash(file_path):
                return True
    return False



api_key = os.getenv("API_KEY")

if not api_key:
    st.error("API key not found. Please set the API_KEY environment variable.")
    
import os

os.environ["GOOGLE_API_KEY"] = api_key



def generate_response_stream(context, materia, unidad_tematica, evidencia, nivel):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.2,
        max_tokens=2000,
        top_p=0.9,
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
    
    for chunk in chain.stream(input_dict):
        yield chunk 

uploaded_file = st.file_uploader("Sube un archivo PDF", type="pdf")
coleccion = st.text_input("Coleccion")

if uploaded_file and coleccion:
    upload_pdf(uploaded_file)
    documents = load_pdf(pdf_directory + uploaded_file.name)

    file_hash = get_file_hash(pdf_directory + uploaded_file.name)
    if is_pdf_already_indexed(file_hash, coleccion):
        st.warning("Este PDF ya ha sido indexado.")
    else:
        chunked_documents = text_splitter(documents)
        for doc in chunked_documents:
            doc.metadata["file_hash"] = file_hash
            doc.metadata["course_name"] = coleccion.lower().replace(" ", "_")
        index_docs(chunked_documents)
        st.success("PDF subido y procesado correctamente.")



materia = st.text_input("Materia", key="materia_generacion")
unidad_tematica = st.text_input("Unidad Temática", key="unidad")
evidencia = st.text_area("Evidencia", key="evidencia")
nivel = st.number_input("Nivel del Estudiante", min_value=1, max_value=4, step=1, key="nivel")

if st.button("Generar Actividades"):
    if materia and unidad_tematica and evidencia:
        st.info(f"🎯 Generando actividades para {materia}, unidad: {unidad_tematica}, nivel: {nivel}")
    else:
        st.warning("⚠️ Completa todos los campos antes de generar.")
  
    related_documents = retrieve_docs(unidad_tematica, materia)


    contexto = "\n".join(doc.page_content for doc in related_documents) if related_documents else ""

    message_placeholder = st.chat_message("assistant").empty()
    full_response = ""

    for chunk in generate_response_stream(contexto, materia, unidad_tematica, evidencia, nivel):

        full_response += chunk  # cada chunk trae parte del texto
        message_placeholder.markdown(full_response)
