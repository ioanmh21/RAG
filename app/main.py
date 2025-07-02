from app import vector_db as vdb
from app.api import router
from fastapi import FastAPI

data_path = 'documents'
collection = vdb.solve_for_vdb(data_path)

app = FastAPI()
app.include_router(router)
@app.get("/")
async def root():
    return {"message": "Hello from root!"}