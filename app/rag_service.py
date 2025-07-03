import google.generativeai as genai
import os
import app.vector_db as vdb
import asyncio
from app.config import settings
from functools import lru_cache

os.environ["CHROMA_SERVER_NO_ANALYTICS"] = settings.CHROMADB_NO_ANALYTICS

data_path = settings.DOCUMENTS_PATH

collection = None
ai_model = None

try:
    collection = vdb.solve_for_vdb(data_path)
    print("ChromaDB collection inițializată cu succes.\n")

    if not settings.GEMINI_API_KEY:
        raise KeyError("Variabila de mediu 'GEMINI_API_API_KEY' nu este setată sau este goală.\n")
    
    genai.configure(api_key = settings.GEMINI_API_KEY)
    
    ai_model = genai.GenerativeModel(settings.LLM_MODEL_NAME)
    print(f"Gemini model '{settings.LLM_MODEL_NAME}' inițializat cu succes.\n")

except KeyError as e:
    print(f"Eroare de configurare API Key: {e}\n")
    print("WARNING: Apelurile către Gemini API vor eșua până la setarea cheii.\n")
    ai_model = None
except Exception as e:
    print(f"Eroare la inițializarea serviciilor (ChromaDB sau Gemini): {e}\n")
    print("WARNING: Funcționalitatea RAG poate fi afectată. Verificați logurile.\n")
    collection = None
    ai_model = None

# Caching pentru interogările ChromaDB
@lru_cache(maxsize = 32)
def _cached_chroma_query(query_text_tuple : tuple, n_results : int):
    if collection is None:
        raise Exception("ChromaDB collection nu este inițializată pentru caching.\n")
    return collection.query(
        query_texts  = list(query_text_tuple),
        n_results = n_results,
    )

# Caching pentru răspunsurile modelului AI
@lru_cache(maxsize = 32)
def _cached_gemini_generate(prompt_text: str):
    if ai_model is None:
        raise Exception("Modelul AI nu este inițializat pentru caching.\n")
    return ai_model.generate_content(prompt_text)

async def answer_question(text : str):
    if collection is None or ai_model is None:
        raise Exception("Serviciul RAG nu este inițializat corect.\n")

    # !!!   folosim threaduri pentru metodele care sunt synchronous !!!

    results = await asyncio.to_thread(
        _cached_chroma_query,
        (text,),
        settings.CHUNKS_RETRIEVED,
    )
    #context
    if results and results.get('documents') and results['documents'][0]:
        context = "\n".join(results['documents'][0])
        print(f"Retrieved Context:\n{context[:500]}...\n")
    else:
        print("Nu sunt documente relevante in baza de date.\n")
        return "Nu am găsit informații relevante în documente.\n"

    #prompt
    prompt = f"""Ești un asistent AI util și precis care răspunde la întrebări pe baza contextului furnizat.
    Dacă nu poți găsi un răspuns în context, spune clar că nu ai informații suficiente.
    Pentru întrebările care necesită numărare sau extragere de informații specifice, fii cât mai exact și concis.
    Evită să incluzi informații irelevante sau să speculezi.

    Context:
    {context}
    
    Întrebare: {text}
    Răspuns: """

    print(f"Prompt Complet trimis către Gemini:\n{prompt[:500]}...\n")

    try:
        #facem un thread separat pentru apelul la gemeni api
        gemini_response = await asyncio.to_thread(
            _cached_gemini_generate,
            prompt
        )

        if gemini_response and hasattr(gemini_response, 'text') and gemini_response.text:
            return gemini_response.text
        else:
            print(f"Atenție: Răspunsul Gemini nu conține text. Detalii: {gemini_response}\n")
            return "Nu am putut genera un răspuns.\n"

    except Exception as e:
        print(f"Eroare la generare cu modelul AI: {e}\n")
        if "RESOURCE_EXHAUSTED" in str(e):
            return "Ne pare rău, am atins limita de utilizare a modelului AI. Vă rugăm să încercați mai târziu.\n"
        return f"A apărut o eroare la comunicarea cu modelul AI: {str(e)}\n"