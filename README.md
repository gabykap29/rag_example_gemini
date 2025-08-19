# RAG con Langchain, Gemini, Nomic y ChromaDB

Este proyecto implementa un sistema de Recuperación Aumentada de Generación (RAG) utilizando Langchain, Gemini AI, embeddings de Nomic y ChromaDB como base de datos vectorial. El sistema permite cargar documentos PDF, indexarlos y generar preguntas de opción múltiple adaptativas basadas en el contenido de los documentos.

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instaladas las siguientes dependencias:

```bash
pip install protobuf==4.25.3 grpcio==1.60.0 langchain langchain-community langchain-core langchain-google-genai langchain-ollama google-generativeai streamlit chromadb python-dotenv
```

## Configuración

1. Crea un archivo `.env` en la raíz del proyecto con tu clave API de Google:

```
API_KEY=tu_clave_api_de_google
```

2. Asegúrate de tener instalado Ollama y el modelo `nomic-embed-text` para los embeddings.

## Estructura del Proyecto

El proyecto contiene dos archivos principales:

### 1. main.py

Este archivo contiene la aplicación Streamlit completa para ejecutar el sistema RAG. Permite:

- Subir archivos PDF
- Indexar documentos en ChromaDB
- Generar preguntas de opción múltiple adaptativas basadas en:
  - Materia
  - Unidad Temática
  - Evidencia (Conocimiento, Procedimiento o Producto)
  - Nivel del estudiante (1-4)

### 2. demo.ipynb

Este notebook Jupyter contiene una versión de demostración del sistema con funcionalidad similar a `main.py`, pero en formato de notebook para facilitar la experimentación y el aprendizaje. Incluye:

- Explicaciones detalladas de cada componente
- Código para cargar PDFs y generar embeddings
- Interfaz Streamlit integrada en el notebook

## Ejecución

### Para ejecutar main.py (Aplicación Streamlit)

```bash
streamlit run main.py
```

Esto iniciará la aplicación Streamlit en tu navegador web (generalmente en http://localhost:8501).

### Para ejecutar demo.ipynb

1. Abre el notebook con Jupyter Notebook o Jupyter Lab:

```bash
jupyter notebook
# o
jupyter lab
```

2. Navega hasta `demo.ipynb` y ábrelo.
3. Ejecuta las celdas secuencialmente para ver la demostración.

## Uso

1. **Subir e indexar documentos**:
   - Sube un archivo PDF
   - Proporciona un nombre para la colección/materia
   - El sistema indexará el documento

2. **Generar preguntas**:
   - Ingresa la materia (debe coincidir con la colección indexada)
   - Especifica la unidad temática
   - Define el tipo de evidencia
   - Selecciona el nivel del estudiante
   - Haz clic en "Generar Actividades"

3. **Visualizar resultados**:
   - El sistema generará preguntas de opción múltiple en formato JSON
   - Las preguntas se adaptarán al nivel especificado

## Notas

- El sistema utiliza el modelo Gemini de Google para la generación de preguntas
- Los embeddings se generan con el modelo `nomic-embed-text` de Ollama
- Los documentos se almacenan en ChromaDB para búsqueda por similitud
- La estructura de las preguntas generadas sigue un formato JSON específico

## Tareas Pendientes: 

- [ ] Construir un servidor con FastApi para realizar las peticiones. 
- [ ] Crear una interfaz de usuario para interactuar con el servidor.
- [ ] Configurar un balanceador de carga para distribuir las solicitudes entrantes.
- [ ] Implementar un sistema de monitoreo para rastrear el rendimiento del servidor.
