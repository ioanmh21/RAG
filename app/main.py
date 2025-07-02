from app import vector_db as vdb
from app.api import router
from fastapi import FastAPI
from app.rag_service import collection

app = FastAPI()
app.include_router(router)
@app.get("/")
async def root():
    return {"message": "Hello from root!"}