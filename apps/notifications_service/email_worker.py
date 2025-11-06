# apps/notifications_service/worker.py
import asyncio
import json
import smtplib
from email.mime.text import MIMEText
from nats.aio.client import Client as NATS
from nats.errors import NoServersError
from apps.notifications_service.config import MailConfig

async def handle_email_notification(msg):
    subject = msg.subject
    try:
        data = json.loads(msg.data.decode())
        print(f"Получено сообщение на тему '{subject}': {data}")

        # Получаем настройки из конфига
        params = MailConfig.get_connection_parametres()
        host = params["mail_host"]
        port = int(params["mail_port"])

        # Формируем email
        message = MIMEText(data["message"])
        message["Subject"] = "Уведомление от сервиса"
        message["From"] = params["mail_address"]
        message["To"] = data["email"]

        with smtplib.SMTP(host, port) as server:
            server.send_message(message)

        print(f"Письмо отправлено на {data['email']}")

    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")

async def run_worker():
    """Основной цикл воркера."""
    nc = NATS()
    try:
        # Подключаемся к NATS
        await nc.connect(servers=["nats://localhost:4222"])
        print("Воркер подключился к NATS")

        # Подписываемся на тему
        await nc.subscribe("notifications.send.email", cb=handle_email_notification)
        print("Воркер слушает тему 'notifications.send.email'")

        # Ждём бесконечно
        await asyncio.Future()  # блокирует выполнение до Ctrl+C

    except NoServersError:
        print("Не удалось подключиться к NATS. Убедитесь, что сервер запущен.")
    except KeyboardInterrupt:
        print("\nВоркер остановлен вручную")
    finally:
        await nc.close()
        print("Воркер отключился от NATS")

if __name__ == "__main__":
    asyncio.run(run_worker())