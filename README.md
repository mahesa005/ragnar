# ragnar

Multimodal RAG (Retrieval-Augmented Generation) pipeline for PDF documents. Extracts text, tables, and images, stores them in a vector database, and answers questions via REST API.

## Features

- **Multimodal PDF Processing**: Extracts text, tables, and images from PDF documents
- **Image Understanding**: Generates descriptions for images in PDFs using vision models
- **Vector Storage**: Stores embeddings in ChromaDB for efficient retrieval
- **RAG-based QA**: Retrieves relevant context and uses LLM to answer questions
- **REST API**: Easy-to-use endpoints for document ingestion and querying
- **Batch Processing**: Handles batch image processing with configurable batch sizes

## Architecture

The system follows a pipeline architecture with two main flows:

### Ingestion Pipeline
1. **Extract** - PDF parsing to extract text, tables, and images
2. **Process Images** - Generate descriptions for images using vision models
3. **Group by Page** - Organize content by page number
4. **Chunk** - Split text into overlapping chunks for better retrieval
5. **Embed & Store** - Generate embeddings and store in ChromaDB

### Retrieval Pipeline
1. **Query Retrieval** - Find relevant chunks from ChromaDB based on the query
2. **LLM Generation** - Use retrieved context to generate an answer via LLM

## Tech Stack

- **Framework**: FastAPI
- **PDF Processing**: Unstructured, PyMuPDF
- **Embeddings**: Hugging Face Sentence Transformers
- **Vector DB**: ChromaDB
- **LLM**: Groq
- **Vision Model**: For image descriptions
- **Text Splitting**: LangChain

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ragnar
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Required environment variables:
- `HF_TOKEN` - Hugging Face API token for embeddings
- `GROQ_API_KEY` - Groq API key for LLM

## Configuration

Key configuration options in `app/core/config.py`:

```python
CHUNK_SIZE = 1000              # Characters per chunk
CHUNK_OVERLAP = 200            # Overlap between chunks
CHROMA_MAX_QUERY_RESULT = 5    # Number of retrieved documents
MAX_FILE_SIZE = 50 * 1_024 * 1_024  # Maximum PDF size (50MB)
IMAGE_BATCH_SIZE = 2           # Batch size for image processing
LLM_TEMPERATURE = 0.1          # LLM generation temperature
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

Server will be available at `http://localhost:8000`

API documentation at `http://localhost:8000/docs` (Swagger UI)

## API Endpoints

### Health Check
```
GET /
```
Returns status message

### Ingest PDF
```
POST /ingest
```
Upload a PDF file for processing

**Request**: Multipart form data with `file` field
**Response**:
```json
{
  "status": "success",
  "message": "Processed 42 chunks from document.pdf",
  "elements": []
}
```

### Query
```
POST /query
```
Ask a question about ingested documents

**Request**:
```json
{
  "query": "What is the main topic?"
}
```

**Response**:
```json
{
  "response": "The main topic is..."
}
```

### Ping
```
GET /ping
```
Simple health check endpoint

## Project Structure

```
ragnar/
├── app/
│   ├── api/              # API routes
│   │   └── routes.py     # Endpoint definitions
│   ├── services/         # Business logic
│   │   ├── extract.py    # PDF extraction
│   │   ├── image_handler.py  # Image processing
│   │   ├── embed.py      # Embedding & storage
│   │   ├── query.py      # LLM querying
│   │   ├── retrieval.py  # Vector DB retrieval
│   │   ├── ingest.py     # File handling
│   │   └── pipeline.py   # Orchestration
│   ├── models/           # Data schemas
│   │   └── schemas.py    # Pydantic models
│   ├── core/             # Configuration
│   │   └── config.py     # App settings
│   └── main.py           # FastAPI app
├── chroma_db/            # Vector database storage
├── data/                 # Upload directory
└── requirements.txt      # Dependencies
```

## How It Works

### Document Ingestion
1. User uploads a PDF via `/ingest` endpoint
2. PDF is parsed to extract text, tables, and images
3. Images are batch-processed to generate descriptions
4. Content is grouped by page
5. Text is split into overlapping chunks
6. Embeddings are generated for each chunk
7. Data is stored in ChromaDB with metadata

### Question Answering
1. User submits query via `/query` endpoint
2. Query is embedded and searched in ChromaDB
3. Top-k relevant chunks are retrieved
4. Retrieved context is passed to LLM
5. LLM generates answer based on context
6. Response is returned to user

## Development

Run tests (if available):
```bash
pytest
```

## Notes

- PDFs are temporarily stored in `data/pdf_uploads` during processing
- ChromaDB data persists in `chroma_db/` directory
- Image processing uses batch processing to manage API limits
- Low LLM temperature (0.1) ensures factual, consistent responses
