import google.generativeai as genai
import os
import app.vector_db as vdb

data_path = 'documents'
collection = vdb.solve_for_vdb(data_path)

def answer_question(text : str):
    try: #configurare api ai
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    except KeyError:
        print("Eroare: Variabila de mediu 'GEMINI_API_KEY' nu este setată.")
        exit()

    MODEL_NAME = 'gemini-2.5-flash'
    ai_model = genai.GenerativeModel(MODEL_NAME)

    #facem embedding la intrebare
    question_embedding = vdb.model.encode([text]).tolist()
    #cautam chunk-urile relevante
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=3
    )
    #context
    context = "\n".join(results['documents'][0])
    #prompt
    prompt = f"Context:\n{context}\n\nÎntrebare: {text}\nRăspuns:"

    try:
        response = ai_model.generate_content(prompt)
        print(response.text)
    except Exception as e:
        print(f"Eroare la generare: {e}")
        if "RESOURCE_EXHAUSTED" in str(e):
            print("\nAi atins limita de utilizare.")
        exit()

    return response.text