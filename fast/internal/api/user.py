from fastapi import APIRouter, Depends
from fast.internal.models import user as model
from fast.internal.service.user import UserService
from fast.internal import dependencies
router = APIRouter()

@router.post("/init-or-deny-access")
async def init_or_deny(user: model.AddUser, service: UserService = Depends(dependencies.get_user_service)):
    return await service.init_or_deny(user)

@router.get("/get-user-data")
async def get_user_data(userid: int, service: UserService = Depends(dependencies.get_user_service)):
    return await service.get_user_data(userid)
