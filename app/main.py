from dotenv import load_dotenv
load_dotenv() #incarca variabilele de mediu

from app.api import app
import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"Serverul Uvicorn porneste pe {settings.HOST}:{settings.PORT}")
    uvicorn.run(app, host = settings.HOST, port = settings.PORT)