#мне написал квенчик, каюсь
# cd D:\My-data\Desktop\Projects\first-together-working
# .\start_services.ps1

# start_services.ps1
# Запускает все микросервисы из корня проекта с использованием `python -m`
# Корень проекта — папка, содержащая папку `apps`

$projectRoot = "D:\My-data\Desktop\Projects\first-together-working"

Write-Host "📁 Корень проекта: $projectRoot" -ForegroundColor Cyan

# Account Service
Start-Process powershell -ArgumentList "-NoExit", "-Command", "
    cd '$projectRoot';
    & 'apps\account_service\.venv\Scripts\Activate.ps1';
    python -m apps.account_service.main
"

# AuthSecurity Service
Start-Process powershell -ArgumentList "-NoExit", "-Command", "
    cd '$projectRoot';
    & 'apps\authsecurity_service\.venv\Scripts\Activate.ps1';
    python -m apps.authsecurity_service.main
"

$projectRoot = "D:\My-data\Desktop\Projects\first-together-working"
# Notifications Service (порт 8030)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "
    cd '$projectRoot';
    & 'apps\notifications_service\.venv\Scripts\Activate.ps1';
    uvicorn apps.notifications_service.main:app --host 0.0.0.0 --port 8030 --reload
"

# Notifications Worker (слушает NATS и отправляет email)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "
    cd '$projectRoot';
    & 'apps\notifications_service\.venv\Scripts\Activate.ps1';
    python -m apps.notifications_service.email_worker
"

Write-Host "✅ Все сервисы запущены как модули из корня проекта!" -ForegroundColor Green