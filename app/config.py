import os

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    LLM_MODEL_NAME: str = 'gemini-2.0-flash-lite'

    DOCUMENTS_PATH: str = 'documents'
    CHROMADB_PERSIST_PATH: str = './chroma_db'
    CHROMADB_COLLECTION_NAME: str = 'my_collection'

    CHROMADB_NO_ANALYTICS: str = "1" # Setează "1" pentru a dezactiva telemetria ChromaDB

    CHUNK_MAX_WORDS: int = 150
    CHUNK_OVERLAP_WORDS: int = 30

    CHUNKS_RETRIEVED: int = 5

    HOST: str = os.getenv("APP_HOST", "127.0.0.1") # Poate fi "0.0.0.0" pentru acces extern
    PORT: int = int(os.getenv("APP_PORT", 8000)) # Portul pe care rulează serverul


settings = Settings()