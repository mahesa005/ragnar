from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="RAGNar",
    description="REST API for PDF interpretation using RAG system",
    version="0.1.0"
)   
app.include_router(router)