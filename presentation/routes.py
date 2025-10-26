from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service.Authorization import AuthService

router = APIRouter()

class LoginRequest(BaseModel):
    mail: str
    phone: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    try:
        token = AuthService.authorize_user(
            mail=data.mail,
            phone=data.phone,
            password=data.password
        )
        if token is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"access_token": token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")