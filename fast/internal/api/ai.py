from fastapi import APIRouter
from fast.internal.models import ai as model


router = APIRouter()

@router.post("/{sessionid}")
async def message_handler(form: model.RequestModel):
    pass