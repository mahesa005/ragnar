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