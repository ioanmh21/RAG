from PyPDF2 import PdfReader
import os
import re
import chromadb
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction
from app.config import settings

os.environ["CHROMA_SERVER_NO_ANALYTICS"] = settings.CHROMADB_NO_ANALYTICS

embedding_function = GoogleGenerativeAiEmbeddingFunction(api_key = settings.GEMINI_API_KEY)

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


# def chunk_text(text, max_words = settings.CHUNK_MAX_WORDS, overlap_words = settings.CHUNK_OVERLAP_WORDS):
#     words = text.split()
#     chunks = []
#     for i in range(0, len(words), max_words - overlap_words):
#         chunk_words = words[i : i + max_words]
#         chunk_text = " ".join(chunk_words)
#         chunks.append(chunk_text)
#     return chunks


def chunk_text(text, max_words=None, overlap_words=None):
    if max_words is None:
        max_words = settings.CHUNK_MAX_WORDS
    if overlap_words is None:
        overlap_words = settings.CHUNK_OVERLAP_WORDS

    lines = text.split('\n')
    chunks = []
    current_chunk_lines = []
    current_chunk_word_count = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        line_words = line.split()
        line_word_count = len(line_words)

        if current_chunk_word_count + line_word_count > max_words and current_chunk_lines:
            chunks.append("\n".join(current_chunk_lines))

            overlap_content = []
            overlap_count = 0
            for ol_line in reversed(current_chunk_lines):
                ol_line_words = ol_line.split()
                if overlap_count + len(ol_line_words) <= overlap_words:
                    overlap_content.insert(0, ol_line)
                    overlap_count += len(ol_line_words)
                else:
                    break
            
            current_chunk_lines = overlap_content
            current_chunk_word_count = overlap_count
        
        current_chunk_lines.append(line)
        current_chunk_word_count += line_word_count

    if current_chunk_lines:
        chunks.append("\n".join(current_chunk_lines))
    
    return [chunk for chunk in chunks if chunk.strip()]

def solve_for_vdb(data_path : str):
    client = chromadb.PersistentClient(path = settings.CHROMADB_PERSIST_PATH)
    collection_name = settings.CHROMADB_COLLECTION_NAME
    
    collection = client.get_or_create_collection(
        name = collection_name,
        embedding_function = embedding_function
    )
    
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