import uvicorn
from fastapi import FastAPI
from apps.account_service.error_handlers import reg_error_handler
from apps.account_service.Presentation.Routes.account_route import router as account_router
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()
reg_error_handler(app)
app.include_router(account_router)

if __name__ == "__main__":
    uvicorn.run(
        "apps.account_service.main:app",        # путь к приложению (файл:переменная)
        host="0.0.0.0",
        port=8010,
        reload=True        # авто-перезагрузка при изменении кода (только для разработки!)
    )


# uvicorn main:app --host 0.0.0.0 --port 8000