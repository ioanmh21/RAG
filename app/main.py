import vector_db as vdb

data_path = 'data\\documents'

data = vdb.extract_data(data_path)
data = vdb.clean_data(data)
chunks, metadatas = vdb.split_in_chunks(data)

# from fastapi import FastAPI

# from pydantic import BaseModel



# app=FastAPI()

# @app.get('/')
# def read_root():
#     return {"message": "Hello World"}
