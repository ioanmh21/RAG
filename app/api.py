from fastapi import APIRouter
import os
from pydantic import BaseModel
from app import rag_service

router = APIRouter()
@router.get("/documents")
async def get_documents():
    return [file for file in os.listdir("documents")]

class Question(BaseModel):
    text : str

@router.post("/ask")
async def answer_question(question : Question):
    answer = rag_service.answer_question(question.text)
    return {"answer" : answer}