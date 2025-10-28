from fastapi import APIRouter, HTTPException
from presentation.schemas.auth import LoginRequest
from presentation.schemas.registration import Registration
from service.Authorization import AuthService
from service.Registration import RegistrationMethods
from service.LoadData import post_data_to_accounts
from pydantic import EmailStr
from presentation.Exceptions.AuthExceptions import *
from presentation.schemas.post_account import *
router = APIRouter()

@router.post("/v1/auth")
def login(mail: str, phone:str, password:str):
    validate_mail = None
    try:
        validate_mail = EmailStr._validate(mail)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid credentials {e}")
    try:
        token = AuthService.authorize_user(LoginRequest(
                mail=mail, phone=phone, password=password
            )
        )
        if token is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"access_token": token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/v1/registration")
def registration(first_name:str, middle_name:str, last_name:str, email:str, phone:str, password:str):
    validate_mail = None
    try:
        validate_mail = EmailStr._validate(email)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid credentials {e}")
    try:
        status = RegistrationMethods.registrate_user(
            mail=validate_mail,
            phone=phone,
            password=password
        )
        if not status:
            raise HTTPException(status_code=401, detail="Something went wrong")
        post_data_to_accounts(
            PostAccount(
                user_id = 1, #Доделать
                first_name = first_name,
                middle_name = middle_name,
                last_name = last_name,
                mail = validate_mail,
                phone = phone,
                date_created = datetime.datetime.now()
            )
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")
