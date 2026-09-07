from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.services.gemini_service import ask_gemini
from pydantic import BaseModel

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