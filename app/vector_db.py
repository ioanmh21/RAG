from PyPDF2 import PdfReader
import os
import re
from sentence_transformers import SentenceTransformer
import chromadb

def extract_data(data_path):
    data = []

    for file in os.listdir(data_path):
        if file.endswith('.pdf'):
            reader = PdfReader(os.path.join(data_path, file))
            text = ""

            page_index = 0
            for page in reader.pages:
                text = page.extract_text() or ""
                page_index += 1
                data.append({
                    "filename" : file, 
                    "page" : page_index, 
                    "text" : text})
    return data

def clean_data(data):  #normalizare date
    new_data = []
    for dict in data:
        raw_text = dict['text']
        raw_text = raw_text.lower()
        raw_text = re.sub(r'\s+', ' ', raw_text) #scoatem spatii duble
        raw_text = re.sub(r'[^\w\s.,;:!?-]', '', raw_text) #scoatem punctuatie inutila

        new_data.append({
            "filename" : dict["filename"], 
            "page" : dict["page"], 
            "text" : raw_text.strip()})
    return new_data

def split_in_chunks(data, chunk_size = 300, overlap = 50):
    chunks = []

    j = 0
    for dict in data:
        words = dict["text"].split()
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i : i + chunk_size])

            chunks.append({
                "filename" : dict["filename"],
                "page" : dict["page"],
                "text" : chunk,
                "chunk_id" : j
            })
            j += 1
    return chunks

def get_data_base_data(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    ids = []
    embeddings = []
    metadatas = []
    documents = []

    for chunk in chunks:
        embedding = model.encode(chunk["text"]).tolist()
        embeddings.append(embedding)

        ids.append(str(chunk["chunk_id"]))
        metadatas.append({
            "filename": chunk["filename"],
            "page": chunk["page"]
        })
        documents.append(chunk["text"])

    return ids, embeddings, metadatas, documents

def create_data_base(ids, embeddings, metadatas, documents, name = "my_rag_collection"):
    client = chromadb.Client()
    collection = client.create_collection(name)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents
    )
    return collection

def solve_for_rag(data_path):
    data = extract_data(data_path)
    data = clean_data(data)
    chunks = split_in_chunks(data)
    ids, embeddings, metadatas, documents = get_data_base_data(chunks)

    return create_data_base(ids, embeddings, metadatas, documents)