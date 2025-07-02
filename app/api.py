import fastapi
import os
from pydantic import BaseModel
from app import rag_service
import uvicorn

class Question(BaseModel):
    text : str


app = fastapi.FastAPI()
router = fastapi.APIRouter()

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

if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port = 8000) 