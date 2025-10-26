from pydantic import BaseModel

class LoginRequest(BaseModel):
    mail: str
    phone: str
    password: str