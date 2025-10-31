from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRegisterIn(BaseModel):
    mail: str
    phone: str
    password_hash: str


class UserIdentifyIn(BaseModel):
    """Используется для delete_user и take_pass — нужны mail + phone"""
    mail: str
    phone: str

class UserOut(BaseModel):
    user_id: int
    mail: str
    phone: str
    date_created: datetime
    password_hash: str

class PasswordHash(BaseModel):
    password_hash: str