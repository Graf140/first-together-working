from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRegisterIn(BaseModel):
    mail: EmailStr
    phone: str
    password_hash: str


class UserIdentifyIn(BaseModel):
    """Используется для delete_user и take_pass — нужны mail + phone"""
    mail: EmailStr
    phone: str

class UserOut(BaseModel):
    user_id: int
    mail: str
    phone: str
    date_created: datetime
    password_hash: str

class PasswordHash(BaseModel):
    password_hash: str