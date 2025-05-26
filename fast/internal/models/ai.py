from pydantic import BaseModel

class RequestModel(BaseModel):
    userid: int
    sessionid: int
    message: str