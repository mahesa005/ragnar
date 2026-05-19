from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from pydantic import BaseModel
from ..models.schemas import QueryRequest, QueryResponse, IngestResponse

router = APIRouter()

@router.get("/ping")
def ping():
    return("pong")

@router.post("/ingest", response_model=IngestResponse)
def ingest(file: UploadFile = File(...)):
    pass

@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):   
    pass

@router.get("/")
def root():
    return {"message": "ragnar is running"}