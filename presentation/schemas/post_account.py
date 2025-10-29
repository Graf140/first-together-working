from pydantic import BaseModel
import datetime

class PostAccount(BaseModel):
    user_id: int
    first_name: str
    middle_name: str
    last_name: str
    mail: str
    phone: str
    date_created: datetime.datetime
