# start_services.ps1
# cd D:\My-data\Desktop\Projects\first-together-working
# .\start_services.ps1

# Путь к корню проекта
$projectRoot = "D:\My-data\Desktop\Projects\first-together-working\apps"

# Запуск AccountService
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\account_service'; .\.venv\Scripts\Activate.ps1; python main.py"

# Запуск AuthService
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\authsecurity_service'; .\.venv\Scripts\Activate.ps1; python main.py"

Write-Host "✅ Оба сервиса запущены в отдельных окнах!" -ForegroundColor Green