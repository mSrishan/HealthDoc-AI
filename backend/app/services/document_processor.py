import fitz  # PyMuPDF
from fastapi import UploadFile
import os
import uuid
from app.services.gemini_service import ask_gemini
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



def analyze_medical_document(text: str) -> str:
    """
    Extracted text එක Gemini එකට දීලා 
    structured medical summary එකක් හදනවා
    """

    prompt = f"""
You are a medical document assistant. 
Analyze the following medical document text and provide a clear, structured summary.

Important rules:
- Do NOT diagnose any disease
- Do NOT recommend treatments or medications
- Only extract and organize information from the document
- If a value appears outside the reference range mentioned in the document, highlight it
- Suggest questions the patient can ask their doctor

Document text:
{text}

Please respond in this exact structure:

📄 Document Type:
(what type of document is this)

👤 Patient Information:
(any patient details found)

🔎 Key Findings:
- list important test results

⚠️ Values Outside Reference Range:
- list any abnormal values (based on ranges in the document)

💊 Medications Mentioned:
(if any)

❓ Questions to Discuss With Your Doctor:
- useful questions based on the findings

Keep the language simple and clear.
"""

    response = ask_gemini(prompt)
    return response