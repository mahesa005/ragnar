import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CHROMA_DB_PATH = "./chroma_db"
CHROMA_COLLECTION_NAME = "ragnar"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

UPLOAD_DIR = Path("data/pdf_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 50 * 1_024 * 1_024

CHROMA_MAX_QUERY_RESULT = 5

LLM_TEMPERATURE = 0.1
LLM_TOP_P = 0.95
LLM_MAX_TOKENS = 1024

IMAGE_DESCRIPTION_TEMPERATURE = 0.2
IMAGE_DESCRIPTION_MAX_TOKENS = 2000
IMAGE_BATCH_SIZE = 2 # Model has low token limit
