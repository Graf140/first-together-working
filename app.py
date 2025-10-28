from fastapi import FastAPI
from error_handlers import reg_error_handler

app = FastAPI()
reg_error_handler(app)

# uvicorn app:app --host 0.0.0.0 --port 8000