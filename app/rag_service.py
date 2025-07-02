import google.generativeai as genai
import os

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Eroare: Variabila de mediu 'GEMINI_API_KEY' nu este setată.")
    print("Asigură-te că ai urmat pașii pentru a o seta și că ai reîncărcat shell-ul/terminalul.")
    exit() # Oprește scriptul dacă cheia nu e disponibilă
