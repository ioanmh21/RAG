import google.generativeai as genai
import os
import app.vector_db as vdb
import asyncio

os.environ["CHROMA_SERVER_NO_ANALYTICS"] = "1"

data_path = 'documents'

collection = None
try:
    collection = vdb.solve_for_vdb(data_path)
    print("ChromaDB collection initializata cu succes.\n")
except Exception as e:
    print(f"Eroare la inițializarea bazei de date ChromaDB:{e}\n")

try: #configurare api ai
    genai.configure(api_key = os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Eroare: Variabila de mediu 'GEMINI_API_KEY' nu este setată.\n")
    exit()

ai_model = None
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    MODEL_NAME = 'gemini-2.5-flash'
    ai_model = genai.GenerativeModel(MODEL_NAME)
    print(f"Gemini model '{MODEL_NAME}' initializat cu succes.\n")
except KeyError:
    print("Eroare: Variabila de mediu 'GEMINI_API_KEY' nu este setată.\n")
    print("WARNING: Gemini API calls will likely fail.\n")
except Exception as e:
    print(f"Eroare la inițializarea modelului Gemini: {e}\n")

async def answer_question(text : str):
    if collection is None or ai_model is None:
        raise Exception("Serviciul RAG nu este inițializat corect.\n")

    # !!!   folosim threaduri deoarece pentru metodele care sunt synchronous !!!

    results = await asyncio.to_thread(
        collection.query,
        query_texts=[text],
        n_results=5,
    )
    #context
    if results and results.get('documents') and results['documents'][0]:
        context = "\n".join(results['documents'][0])
        print(f"Retrieved Context:\n{context[:500]}...\n")
    else:
        print("Nu sunt documente relevante in baza de date.\n")
        return "Nu am găsit informații relevante în documente.\n"

    #prompt
    prompt = f"""Ești un asistent AI care răspunde la întrebări pe baza contextului furnizat.
    Dacă răspunsul nu poate fi găsit în context, spune clar că nu ai informații suficiente.

    Context: {context}
    Întrebare: {text}
    Răspuns: """

    try:
        #facem un thread separat pentru apelul la gemeni api
        gemini_response = await asyncio.to_thread(ai_model.generate_content, prompt)

        if gemini_response and hasattr(gemini_response, 'text') and gemini_response.text:
            return gemini_response.text
        else:
            # Handle cases where Gemini might not return text (e.g., safety block, empty response)
            # You can inspect gemini_response.prompt_feedback or gemini_response.candidates
            # for more details if needed.
            print(f"Atenție: Răspunsul Gemini nu conține text. Detalii: {gemini_response}\n")
            return "Nu am putut genera un răspuns.\n"

    except Exception as e:
        print(f"Eroare la generare cu modelul AI: {e}\n")
        if "RESOURCE_EXHAUSTED" in str(e):
            return "Ne pare rău, am atins limita de utilizare a modelului AI. Vă rugăm să încercați mai târziu.\n"
        return f"A apărut o eroare la comunicarea cu modelul AI: {str(e)}\n"