from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel

from app.services.gemini_service import ask_gemini
from app.services.document_processor import save_pdf, extract_text_from_pdf

load_dotenv()

app = FastAPI(
    title="HealthDoc AI",
    description="AI Medical Document Intelligence Platform",
    version="1.0.0"
)

# Frontend එකෙන් request එනකොට allow කරන්න
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "HealthDoc AI Backend is running!",
        "status": "ok"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        answer = ask_gemini(request.question)
        return {
            "question": request.question,
            "answer": answer
        }
    except Exception as e:
        return {
            "error": str(e)
        }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # PDF file එකද කියලා බලනවා
        if not file.filename.lower().endswith(".pdf"):
            return {"error": "Only PDF files are allowed"}

        # File එක save කරනවා
        file_path = await save_pdf(file)

        # Text extract කරනවා
        extracted_text = extract_text_from_pdf(file_path)

        return {
            "message": "PDF uploaded and processed successfully",
            "filename": file.filename,
            "file_path": file_path,
            "extracted_text": extracted_text[:2000]
        }

    except Exception as e:
        return {"error": str(e)}