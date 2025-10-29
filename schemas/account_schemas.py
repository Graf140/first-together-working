# auth_service/schemas/account_schemas.py
from typing import Optional

from pydantic import BaseModel, EmailStr, AnyHttpUrl


class CreateAccountRequest(BaseModel):
    email: EmailStr
    phone: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    user_id: int

class AccountCreatedResponse(BaseModel):
    user_id: int
    email: EmailStr
    phone: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str