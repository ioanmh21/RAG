from PyPDF2 import PdfReader
import os
import re

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
                data.append({"filename" : file, "page" : page_index, "text" : text})
    return data

def clean_data(data):  #normalizare date
    new_data = []
    for dict in data:
        raw_text = dict['text']
        raw_text = raw_text.lower()
        raw_text = re.sub(r'\s+', ' ', raw_text) #scoatem spatii duble
        raw_text = re.sub(r'[^\w\s.,;:!?-]', '', raw_text) #scoatem punctuatie inutila

        new_data.append({"filename" : dict["filename"], "page" : dict["page"], "text" : raw_text.strip()})
    return new_data

def split_in_chunks(data, chunk_size = 300, overlap = 50):
    chunks = []
    metadatas = []

    for dict in data:
        words = dict["text"].split()
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i : i + chunk_size])
            chunks.append(chunk)
            metadatas.append({
                "filename" : dict["filename"],
                "page" : dict["page"],
                "chunk_id" : i // (chunk_size - overlap)
            })

    return chunks, metadatas
