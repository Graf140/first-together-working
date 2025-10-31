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

@router.post("/auth")
def login(data: LoginRequest):
    try:
        EmailStr._validate(data.email)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid credentials {e}")
    try:
        token = AuthService.authorize_user(LoginRequest(
                email=data.email, phone=data.phone, password=data.password
            )
        )
        if token is None:
            raise HTTPException(status_code=401, detail="Invalid credentials1")
        return {"access_token": token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials2")

@router.post("/registration")
async def registration(data: Registration):
    try:
        EmailStr._validate(data.email)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid credentials {e}")
    try:
        status = RegistrationMethods.registrate_user(
            mail=data.email,
            phone=data.phone,
            password=data.password
        )
        if not status:
            raise HTTPException(status_code=401, detail="Something went wrong")
        await post_data_to_accounts(
            PostAccount(
                user_id = status,
                first_name = data.first_name,
                middle_name = data.middle_name,
                last_name = data.last_name,
                mail = data.email,
                phone = data.phone,
                date_created = datetime.datetime.now()
            )
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")
