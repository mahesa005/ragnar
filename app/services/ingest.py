import os
from fastapi import UploadFile, File, HTTPException
from ..core.config import UPLOAD_DIR, MAX_FILE_SIZE

async def validate_file(file: UploadFile):
    """
    Validates upload file extentsion, type, error handling
    """
    # 1. Check file type
    # Retrieve file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be PDF")
    header = await file.read(5)
    if header != b'%PDF-':
        raise HTTPException(status_code=400, detail="File must be PDF")
    await file.seek(0)
    
    # 2. Check file size
    await file.seek(0, 2)
    size = await file.tell()
    await file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE // (1024 * 1024)}MB")
    return True