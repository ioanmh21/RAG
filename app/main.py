import vector_db as vdb

data_path = 'data\\documents'

collection = vdb.solve_for_rag(data_path)


# from fastapi import FastAPI
# from pydantic import BaseModel

# app=FastAPI()

# @app.get('/')
# def read_root():
#     return {"message": "Hello World"}
