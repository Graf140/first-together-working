from dotenv import load_dotenv
from presentation.routes import router as auth_router
import os
from fastapi import FastAPI
import uvicorn

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

app = FastAPI(title="SecAuth-service")
app.secret_key = secret_key

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="10.0.65.107", port=8200)