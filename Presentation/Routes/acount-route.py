from urllib import request

from fastapi import FastAPI, HTTPException, Request
from app import app
from repositories.acount import AcountRepository
from decorators.phone import validate_phone
from decorators.email import validate_email
from services.acount import AcountService
import json
from schemas.schemas import CreateUserSchema



# !!!не защищаемая информация!!!(напрямую в БД)
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/acount/{email}")
@validate_email
def read_acount_information_email(email: str):
    user = AcountRepository.get_user_by_email(email=email)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

@app.get("/api/acount/{phone}")
@validate_phone
def read_acount_information_phone(phone: str):
    user = AcountRepository.get_user_by_phone(phone=phone)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user


@app.put("/api/acount")
async def create_user(request: Request):
    try:
        # 1. Читаем тело запроса как JSON
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # 2. Валидируем через Marshmallow
    schema = CreateUserSchema()
    try:
        data = schema.load(body)  # ← возвращает dict с валидными данными
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Validation error: {err.messages}")

    # 3. Передаём в сервис
    try:
        result = AcountService.create_or_update_user(
            email=data["email"],
            phone=data["phone"],
            full_name=data["full_name"]
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")