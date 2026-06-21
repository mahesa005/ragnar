from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from pydantic import BaseModel
from ..models.schemas import QueryRequest, QueryResponse, IngestResponse
from ..services.ingest import validate_file, save_file
from ..services.extract import extract_pdf

router = APIRouter()

@router.get("/ping")
def ping():
    return("pong")

@router.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)):
    await validate_file(file)
    file_path = await save_file(file)
    pdf_content = extract_pdf(file_path)
    return IngestResponse(status="success", message="File validated successfully", elements=[pdf_content])

@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):   
    pass

@router.get("/")
def root():
    return {"message": "ragnar is running"}