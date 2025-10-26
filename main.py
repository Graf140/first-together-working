from dotenv import load_dotenv
from presentation.routes import router as auth_router
import os
from fastapi import FastAPI

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

app = FastAPI(title="SecAuth-service")
app.secret_key = secret_key

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])