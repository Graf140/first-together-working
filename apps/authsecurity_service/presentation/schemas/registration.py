from pydantic import BaseModel

class Registration(BaseModel):
    email: str
    password: str
    phone: str
    first_name: str
    middle_name: str
    last_name: str