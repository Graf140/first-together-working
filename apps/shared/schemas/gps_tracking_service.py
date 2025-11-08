from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GpsPoint(BaseModel):
    lat: float
    lng: float
    timestamp: datetime
    altitude: Optional[float] = None
    speed: Optional[float] = None

class StartTrackRequest(BaseModel):
    user_id: str

class AddTrackPointRequest(BaseModel):
    user_id: str
    point: GpsPoint

class FinishTrackRequest(BaseModel):
    user_id: str