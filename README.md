Proiect de Învățare: Sistem RAG cu FastAPI pentru Începători

## 🎯 Ce vei învăța din acest proiect

### Backend Basics
- Cum funcționează un API REST
- Ce înseamnă endpoint-uri și cum le creezi
- Cum primești și trimiți date în format JSON
- Cum documentezi automat API-ul tău cu Swagger

### AI/RAG Basics
- Ce sunt embeddings și cum ajută la căutare semantică
- Cum funcționează un sistem RAG simplu
- Cum folosești un API de AI (Gemini) în aplicația ta
- Cum stochezi și cauți în documente text

## 📁 Structura Simplă a Proiectului

```
rag_project/
├── app/
│ ├── main.py # Punctul de pornire al aplicației
│ ├── api.py # Endpoint-urile tale
│ ├── rag_service.py # Logica pentru RAG
│ ├── vector_db.py # Lucrul cu baza de date vectorială
│ └── config.py # Configurări (API keys, etc.)
│
├── data/
│ └── documents/ # Folder cu documente text simple
│ ├── doc1.txt
│ ├── doc2.txt
│ └── doc3.txt
│
├── requirements.txt # Lista de librării Python necesare
├── .env # Variabile de mediu (API keys)
├── .env.example # Template pentru .env
├── Dockerfile # Pentru a rula în Docker
└── README.md # Documentația proiectului
```

## 🛠️ Tehnologii de Bază

### Pentru Backend
- **FastAPI**: Framework simplu pentru a crea API-uri
- **Uvicorn**: Server pentru a rula aplicația FastAPI
- **Pydantic**: Pentru validarea datelor (vine cu FastAPI)

### Pentru AI/RAG
- **Google Generative AI**: Pentru a folosi Gemini API
- **ChromaDB**: Bază de date simplă pentru vectori
- **Sentence Transformers**: Pentru a crea embeddings local (opțional)

### Pentru Development
- **Python 3.10+**: Limbajul de programare
- **Docker**: Pentru a împacheta aplicația (opțional la început)
- **python-dotenv**: Pentru a citi variabile din .env

## 🚀 Ce va face aplicația ta

### 1. Încărcare Documente (la pornire)
- Citește fișiere .txt din folderul `data/documents/`
- Creează embeddings (reprezentări numerice) pentru fiecare document
- Le salvează în ChromaDB pentru căutare rapidă

### 2. Endpoint Principal: POST /ask
- Primește o întrebare de la utilizator
- Caută în baza de date cele mai relevante documente
- Trimite întrebarea + context către Gemini
- Returnează răspunsul generat

### 3. Endpoint Secundar: GET /documents
- Arată ce documente sunt în sistem
- Util pentru debugging

### 4. Documentație Automată
- FastAPI generează automat documentație la `/docs`
- Poți testa API-ul direct din browser

## 📝 Pași de Implementare

### 1: Setup și Hello World
1. Instalează Python și creează virtual environment
2. Instalează FastAPI și Uvicorn
3. Creează primul endpoint simplu care returnează "Hello World"
4. Învață să rulezi serverul și să accesezi `/docs`

### 2: Lucrul cu Date
1. Învață să primești date prin POST
2. Creează modele Pydantic pentru request și response
3. Adaugă validare pentru input
4. Practică cu endpoint-uri CRUD simple

### 3: Integrare ChromaDB
1. Instalează și configurează ChromaDB
2. Învață să adaugi documente în baza de date
3. Implementează căutarea simplă
4. Testează cu câteva documente mock

### 4: Conectare la Gemini
1. Obține API key pentru Gemini
2. Învață să faci request-uri către API
3. Creează funcții simple de generare text
4. Gestionează erorile și rate limits

### 5: Implementare RAG
1. Combină căutarea cu generarea
2. Construiește prompt-uri eficiente
3. Testează cu diferite întrebări
4. Optimizează rezultatele

### 6: Polish și Docker
1. Adaugă logging pentru debugging
2. Îmbunătățește gestionarea erorilor
3. Creează Dockerfile simplu
4. Documentează cum se folosește aplicația

## 💡 Concepte Importante de Înțeles

### API REST Basics
- **GET**: Pentru a citi date
- **POST**: Pentru a trimite date
- **Endpoint**: O adresă URL care face ceva specific
- **Request/Response**: Cerere și răspuns în format JSON

### RAG Concepts
- **Embedding**: Transformarea textului în numere pentru comparație
- **Similarity Search**: Găsirea documentelor similare semantic
- **Context**: Informația relevantă pe care o dai AI-ului
- **Prompt**: Instrucțiunea completă pe care o trimiți către AI

### Python Async Basics
- **async/await**: Pentru operații care durează mult (API calls)
- **Concurrency**: Cum să gestionezi mai multe request-uri simultan

## 🎓 Resurse de Învățare Recomandate

### Pentru FastAPI
1. Tutorial oficial FastAPI (foarte bun pentru începători)
2. Video-uri YouTube despre REST APIs
3. Documentația pentru HTTP status codes

### Pentru AI/RAG
1. Concepte de base despre embeddings
2. Tutoriale simple ChromaDB
3. Documentația Gemini API

### Pentru Python
1. Async programming basics
2. Environment variables și configurare
3. Error handling în Python

## ⚠️ Greșeli Comune de Evitat

1. **Nu hardcoda API keys** - folosește întotdeauna .env
2. **Nu uita error handling** - API-urile externe pot pica
3. **Începe simplu** - nu adăuga features până nu merge baza
4. **Testează manual des** - folosește Swagger UI
5. **Nu ignora documentația** - scrie README pe măsură ce lucrezi

## 🎯 Obiective Minime pentru Proiect Funcțional

1. **3-5 endpoint-uri funcționale**
- POST /ask - întrebare principală
- GET /health - verificare că merge
- GET /documents - listare documente

2. **Cel puțin 5 documente text** în sistem

3. **Răspunsuri coerente** la întrebări despre conținutul documentelor

4. **Documentație Swagger** funcțională și ușor de înțeles

5. **README clar** cu instrucțiuni de instalare și utilizare

## 🚦 Cum Știi că Ai Reușit

- [ ] Aplicația pornește fără erori
- [ ] Poți accesa `/docs` și vezi endpoint-urile tale
- [ ] Poți face o întrebare și primești un răspuns relevant
- [ ] Codul e organizat și ușor de citit
- [ ] Ai învățat conceptele de bază ale backend-ului
- [ ] Înțelegi cum funcționează un sistem RAG simplu

## 💪 Următorii Pași (După ce Termini Basics)

1. Adaugă mai multe tipuri de documente (PDF, etc.)
2. Implementează un sistem simplu de utilizatori
3. Adaugă caching pentru performanță
4. Experimentează cu alți provideri de AI
5. Deploy pe un serviciu gratuit (Render, Railway)

Ține minte: scopul este să înveți, nu să faci sistemul perfect din prima! Începe simplu și adaugă complexitate gradual.