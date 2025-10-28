from fastapi import FastAPI, HTTPException, Request
from app import app
from repositories.account import AccountRepository
from fastapi import Query
from services.account import AccountService
import json
from schemas.account_schemas import *
from typing import Optional
from pydantic import EmailStr
from decorators.phone import *
from exceptions import *


# !!!не защищаемая информация!!!(напрямую в БД)
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/v1/accounts/search")
def search_account(
    email: Optional[EmailStr] = Query(None),
    phone: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None)
):
    count = 0
    for x in [email, phone, user_id]:
        if x is not None:
            count += 1

    if count == 0:
        raise ZaprosError("Укажите email, phone или user_id")
    if count > 1:
        raise ZaprosError("Укажите только один параметр: email, phone или user_id")

    # Валидация телефона (если передан)
    if phone is not None and not is_valid_phone(phone):
        raise ValueError("Нет от формат телефона")

    # Валидация user_id (если передан)
    if user_id is not None and not user_id.isdigit():
        raise ValueError("user_id должно быть числом")

    user = AccountService.search_user(
        email=email,
        phone=phone,
        user_id=user_id
    )

    if user is None:
        raise UserNotFoundError("User not found")

    return user


#Что такое регистрация пользователя? Это
# 1. Валидация данных запросы
# 2. Проверка, не существует ли такой.
# 3. Создание account.
# 4. Создание профиля.
# 5. Выдача токенов.
# В это время на фронте крутится лоадер, поэтому только синхронный флоу тут,
# без брокера. В этом флоу все делает account, кроме выдачи токенов.
# Я бы сделал так - обращаемся в auth, передаём в account - account сохраняет и
# отдает назад данные для формирования токена - auth создаёт токен


@app.post("/v1/accounts", response_model=AccountCreatedResponse)
def create_account(request: CreateAccountRequest):
    # Проверка на существование email
    if AccountRepository.get_user_by_email(request.email) is not None:
        raise HTTPException(status_code=409, detail="Аккаунт с указанным email уже создан!")

    # Проверка на существование телефона
    if AccountRepository.get_user_by_phone(request.phone) is not None:
        raise HTTPException(status_code=409, detail="Аккаунт с указанным телефоном уже создан!")

    user_id = AccountRepository.create_account(
        email=request.email,
        phone=request.phone,
        first_name=request.first_name,
        middle_name=request.middle_name,
        last_name=request.last_name
    )

    return AccountCreatedResponse(
        user_id=user_id,
        email=request.email,
        phone=request.phone,
        first_name=request.first_name,
        middle_name=request.middle_name,
        last_name=request.last_name
    )