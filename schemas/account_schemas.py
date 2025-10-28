# auth_service/schemas/account_schemas.py
from pydantic import BaseModel, EmailStr

class CreateAccountRequest(BaseModel):
    email: EmailStr
    phone: str
    first_name: str
    middle_name: str
    last_name: str

class AccountCreatedResponse(BaseModel):
    user_id: str
    email: EmailStr
    phone: str
    first_name: str
    middle_name: str
    last_name: str