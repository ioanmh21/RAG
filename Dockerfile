FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r /app/requirements.txt

COPY app /app/app
COPY documents /app/documents
COPY .env /app/.env
COPY frontend.py /app/frontend.py
COPY interface.html /app/interface.html
COPY interface.css /app/interface.css
COPY interface.js /app/interface.js

# 8000 pentru backend-ul FastAPI
# 8001 pentru serverul de frontend Python
EXPOSE 8000
EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
