# apps/notifications_service/nats_client.py
import json
from nats.aio.client import Client as NATS
from nats.errors import NoServersError

async def connect_nats():
    """Подключается к серверу NATS."""
    nc = NATS()
    try:
        await nc.connect(servers=["nats://localhost:4222"])
        print("успешно подключились к NATS")
        return nc
    except NoServersError:
        print("Не удалось подключиться к NATS. Убедитесь, что сервер запущен.")
        raise

async def send_notification(nc, subject: str, data: dict):
    """Отправляет сообщение в NATS."""
    if not nc.is_connected:
        raise RuntimeError("NATS не подключён")
    message = json.dumps(data).encode()
    await nc.publish(subject, message)
    print(f"Отправлено в NATS: {subject} → {data}")