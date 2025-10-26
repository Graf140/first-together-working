from dotenv import load_dotenv
# from presentation.routes import register_routes
# from presentation.error_handlers import register_error_handlers
import os
from fastapi import FastAPI

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

app = FastAPI()
app.secret_key = secret_key

register_routes(app)
register_error_handlers(app)

if __name__ == "__main__":
    app.