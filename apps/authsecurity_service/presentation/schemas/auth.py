from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    phone: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SessionStatusUpdate(BaseModel):
    token: str = Field(..., min_length=1)
    status: bool

class TokenRequest(BaseModel):
    token: str = Field(..., min_length=1)

class SessionOperationResponse(BaseModel):
    success: bool
    message: Optional[str] = None