import fastapi
import os
from pydantic import BaseModel
from app import rag_service
from fastapi.middleware.cors import CORSMiddleware

class Question(BaseModel):
    text : str

app = fastapi.FastAPI()
router = fastapi.APIRouter()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    f"http://localhost:{8001}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
async def root():
    return {"message" : "Hello from root!"}

@router.get("/documents")
async def get_documents():
    return [file for file in os.listdir("documents")]

@router.post("/ask")
async def answer_question(question : Question):
    try:
        answer = await rag_service.answer_question(question.text)
        return {"answer" : answer}
    except Exception as e:
        raise fastapi.HTTPException(
            status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail = str(e))

app.include_router(router)
