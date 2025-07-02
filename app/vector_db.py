from PyPDF2 import PdfReader
import os
import re
import chromadb
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

embedding_function = GoogleGenerativeAiEmbeddingFunction(api_key = os.environ["GEMINI_API_KEY"])

def extract_text(data_path):
    data = []
    for file in os.listdir(data_path):
        file_path = os.path.join(data_path, file)
        
        if file.endswith('.pdf'):
            print(f"Procesare PDF: {file_path}\n")
            try:
                reader = PdfReader(file_path)
                page_index = 0
                for page in reader.pages:
                    text = page.extract_text() or ""
                    # normalizare
                    cleaned_text = re.sub(r'\s+', ' ', text).strip()
                    if cleaned_text:
                        page_index += 1
                        data.append({
                            "filename": file,
                            "page": page_index,
                            "text": cleaned_text
                        })
            except Exception as e:
                print(f"Eroare la procesare PDF {file_path}: {e}\n")
                continue

        elif file.endswith('.txt'):
            print(f"Procesare TXT: {file_path}\n")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    #normalizare
                    cleaned_text = re.sub(r'\s+', ' ', text).strip()
                    
                    if cleaned_text:
                        data.append({
                            "filename": file,
                            "page": 1,
                            "text": cleaned_text
                        })
            except Exception as e:
                print(f"Eroare la procesare TXT {file_path}: {e}\n")
                continue
        else:
            print(f"Fișier ignorat (tip necunoscut): {file_path}\n")
            continue
    return data

def chunk_text(text, max_words = 200, overlap_words = 40):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words - overlap_words):
        chunk_words = words[i : i + max_words]
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)
    return chunks

def solve_for_vdb(data_path : str):
    client = chromadb.PersistentClient(path = "./chroma_db")
    collection_name = "my_document_collection"
    
    collection = client.get_or_create_collection(
        name = collection_name,
        embedding_function = embedding_function
    )

    documents_to_add = []
    metadatas_to_add = []
    ids_to_add = []

    global_chunk_id_counter = collection.count()

    extracted_data = extract_text(data_path)
    for doc_info in extracted_data:
        page_chunks = chunk_text(doc_info['text'])

        for i, chunk in enumerate(page_chunks):
            unique_chunk_id = f"chunk_{global_chunk_id_counter}"

            documents_to_add.append(chunk)
            metadatas_to_add.append({
                "filename": doc_info['filename'],
                "page": doc_info['page'],
                "chunk_index": i,
            })
            ids_to_add.append(unique_chunk_id)
            global_chunk_id_counter += 1

    if documents_to_add:
        collection.add(
            documents = documents_to_add,
            metadatas = metadatas_to_add,
            ids = ids_to_add
        )
        print("Documente adaugate cu succes.\n")
    else:
        print("Nu exista documente noi de adaugat.\n")

    return collection