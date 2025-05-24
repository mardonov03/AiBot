from fastapi import APIRouter
from fast.internal.models import user as model


router = APIRouter()

@router.post("add-to-db")
async def add_user(user: model.AddUser):
    pass