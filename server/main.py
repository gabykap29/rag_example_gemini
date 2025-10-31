from fastapi import FastAPI
from app.api.endpoints import generate, documents, questions
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="RAG API",
    description="API para generar actividades educativas utilizando RAG (Retrieval Augmented Generation)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router)
app.include_router(documents.router)
app.include_router(questions.router)



