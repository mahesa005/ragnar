import os
import shutil
from fastapi import UploadFile, File, HTTPException
from ..core.config import UPLOAD_DIR, MAX_FILE_SIZE
from pathlib import Path

async def validate_file(file: UploadFile):
    # 1. Check file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be PDF")
    
    header = await file.read(5)
    if header != b'%PDF-':
        raise HTTPException(status_code=400, detail="File must be PDF")
    await file.seek(0)
    
    # 2. Check file size
    contents = await file.read()
    size = len(contents)
    await file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE // (1024 * 1024)}MB")

async def save_file(file: UploadFile) -> str:
    """
    save uploaded file to local disk
    input: UploadFile object
    output: path string ke file yang disimpan
    """
    file_path = UPLOAD_DIR / file.filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return str(file_path)