from pydantic import BaseModel

class UpdateAgreementMesid(BaseModel):
    userid: int
    mesid: int

class UpdateAgreement(BaseModel):
    userid: int
    status: bool