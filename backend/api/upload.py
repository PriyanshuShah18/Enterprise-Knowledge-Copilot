# Document uploading endpoint

import os
from typing import List
from fastapi import APIRouter, UploadFile, File

from backend.config import UPLOAD_DIR
from backend.rag.loader import load_document
from backend.rag.splitter import split_documents
from backend.rag.vectorstore import add_documents

router = APIRouter()

@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    all_chunks = []
    uploaded_files = []

    for file in files:
        path = os.path.join(UPLOAD_DIR, file.filename)

        with open(path, "wb") as f:
            f.write(await file.read())

        documents = load_document(path)
        chunks = split_documents(documents)

        all_chunks.extend(chunks)
        uploaded_files.append(file.filename)

    add_documents(all_chunks)

    return {
        "status": "success",
        "files_uploaded": uploaded_files,
        "total_chunks_added": len(all_chunks),
    }
