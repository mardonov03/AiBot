from fastapi import APIRouter
from fast.internal.models import ai as model
from fastapi import Depends
from fast.internal.service.ai import AiService
from fast.internal import dependencies

router = APIRouter()

@router.post("/")
async def message_handler(form: model.RequestModel, service: AiService = Depends(dependencies.get_ai_service)):
    return await service.message_handler(form)