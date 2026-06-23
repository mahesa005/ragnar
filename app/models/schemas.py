from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class Sources(BaseModel):
    page: int
    content_type: str

class QueryResponse(BaseModel):
    response: str

class IngestResponse(BaseModel):
    status: str
    message: str
    elements: list = []
