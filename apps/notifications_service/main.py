# apps/notifications_service/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from apps.notifications_service.nats_client import connect_nats, send_notification
from apps.shared.schemas.notifications_service_request import NotificationRequest

nats_client = None

# Lifespan: управление жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    global nats_client
    nats_client = await connect_nats()
    yield
    if nats_client:
        await nats_client.close()

app = FastAPI(title="Notifications Service", lifespan=lifespan)


# Endpoint для отправки уведомления
@app.post("/v1/notifications/")
async def notify(request: NotificationRequest):
    global nats_client
    try:
        await send_notification(
            nc=nats_client,
            subject="notifications.send.email",
            data={
                "user_id": request.user_id,
                "email": request.email,
                "message": request.message
            }
        )
        return {"status": "success", "detail": "Уведомление отправлено в очередь"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")