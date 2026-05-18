import os
from dotenv import load_dotenv

load_dotenv

HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CHROMA_DB_PATH = "./chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200