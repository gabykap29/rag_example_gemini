# Servidor RAG para Generación de Actividades Educativas

Este servidor implementa una API basada en FastAPI que utiliza la técnica de Retrieval Augmented Generation (RAG) para generar actividades educativas de alta calidad. El sistema permite subir documentos (PDF y DOCX) que serán indexados y utilizados como contexto para la generación de actividades personalizadas.

## Características

- **Generación de actividades**: Crea actividades educativas de opción múltiple adaptativas y pedagógicamente sólidas.
- **Procesamiento de documentos**: Soporta la carga e indexación de archivos PDF y DOCX.
- **Búsqueda semántica**: Utiliza embeddings para recuperar información relevante de los documentos.
- **API RESTful**: Interfaz clara y documentada para integración con aplicaciones frontend.
- **Documentación interactiva**: Swagger UI para probar y entender los endpoints.

## Requisitos previos

- Python 3.12 
- [Ollama](https://ollama.ai/) instalado y configurado
- Espacio en disco para almacenar documentos y embeddings

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/gabykap29/rag_example_gemini.git
cd rag/server
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno (opcional):

```bash
cp Example.env .env
# Edita el archivo .env según tus necesidades
```

## Configuración de Ollama

### Instalación de Ollama

1. Descarga e instala Ollama desde [ollama.ai](https://ollama.ai/)
2. Verifica que Ollama esté funcionando correctamente:

```bash
ollama --version
```

### Creación de un modelo personalizado con Ollama

El servidor utiliza un modelo personalizado basado en Gemma para la generación de actividades educativas. Para crear este modelo:

1. Asegúrate de que Ollama esté en ejecución
2. Ejecuta el siguiente comando desde la carpeta del servidor:

```bash
ollama create medicina -f prompt_system.txt
```

Este comando creará un modelo personalizado llamado `medicina` utilizando las instrucciones del archivo `prompt_system.txt`. El modelo está configurado para:

- Actuar como un asistente educativo especializado en diseño de actividades de evaluación formativa
- Generar actividades de opción múltiple adaptativas según parámetros específicos
- Producir respuestas en formato JSON estructurado
- Adaptar la dificultad según el nivel del estudiante

## Ejecución del servidor

```bash
uvicorn main:app --reload
```

El servidor estará disponible en `http://localhost:8000`.

## Documentación de la API

Accede a la documentación interactiva de la API en:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints principales

### Generación de actividades

```
POST /generate
```

Genera una actividad educativa basada en los parámetros proporcionados:

- **materia**: Campo de conocimiento específico (ej: Anatomía)
- **unidad_tematica**: Tema específico dentro de la materia (ej: Sistema Nervioso)
- **evidencia**: Tipo de competencia a evaluar (Conocimiento, Procedimiento, Producto)
- **nivel**: Nivel del estudiante (1: Básico, 2: Satisfactorio, 3: Avanzado)

### Carga de documentos

```
POST /documents/upload
```

Permite subir documentos PDF o DOCX para ser indexados y utilizados como contexto:

- **file**: Archivo PDF o DOCX (máximo 10MB)
- **subject**: Materia o asignatura relacionada con el documento

## Estructura del proyecto

```
server/
├── app/
│   ├── api/            # Definición de endpoints
│   ├── config/         # Configuración de la aplicación
│   ├── core/           # Lógica central (vectorstore, modelos LLM)
│   ├── models/         # Modelos Pydantic
│   ├── services/       # Servicios de negocio
│   └── utils/          # Utilidades
├── main.py            # Punto de entrada de la aplicación
├── prompt_system.txt  # Instrucciones para el modelo personalizado
└── requirements.txt   # Dependencias del proyecto
```

