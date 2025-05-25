from pydantic import BaseModel, constr, EmailStr
from datetime import datetime

class AddUser(BaseModel):
    userid: int
    username: str | None = None
    full_name: str

class UpdateUser(BaseModel):
    username: str | None = None
    full_name: str

class InfoUser(BaseModel):
    userid: int
    full_name: str
    username: str | None = None
    added_time: datetime
    agreement_status: bool
