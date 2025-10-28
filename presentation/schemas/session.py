from pydantic import BaseModel, Field
from typing import Optional

class SessionCreate(BaseModel):
    token: str = Field(..., min_length=16, description="JWT or session token")

class SessionVerify(BaseModel):
    token: str = Field(..., min_length=1)

class SessionUpdateStatus(BaseModel):
    token: str = Field(..., min_length=1)
    status: bool

class SessionUpdateToken(BaseModel):
    current_token: str = Field(..., min_length=1)
    new_token: str = Field(..., min_length=16)

class SessionOut(BaseModel):
    token: str
    status: bool
    id: Optional[int] = None