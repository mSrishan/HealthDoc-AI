import fitz  # PyMuPDF
from fastapi import UploadFile
import os
import uuid

UPLOAD_DIR = "uploads"

# uploads folder එක නැත්නම් හදනවා
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_pdf(file: UploadFile) -> str:
    """PDF file එක save කරලා path එක return කරනවා"""
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return file_path


def extract_text_from_pdf(file_path: str) -> str:
    """PDF එකෙන් text එක extract කරනවා"""
    text = ""
    doc = fitz.open(file_path)

    for page in doc:
        text += page.get_text()

    doc.close()
    return text.strip()