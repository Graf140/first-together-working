from dotenv import load_dotenv

from presentation.routes import router as auth_router
import os
from fastapi import FastAPI
import uvicorn

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

app = FastAPI(title="SecAuth-service")
app.secret_key = secret_key

app.include_router(auth_router, prefix="/api/v1", tags=["auth","registration"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8200)