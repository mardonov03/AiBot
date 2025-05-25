from pydantic import BaseModel

class UpdateAgreementMesid(BaseModel):
    userid: int
    mesid: int