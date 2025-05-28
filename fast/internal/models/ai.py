from pydantic import BaseModel

class RequestModel(BaseModel):
    userid: int
    context: str