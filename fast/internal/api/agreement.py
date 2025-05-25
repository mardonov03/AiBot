from fastapi import APIRouter, Depends
from fast.internal.models import agreement as model
from fast.internal.service.agreement import AgreementService
from fast.internal import dependencies

router = APIRouter()

@router.post("/update-mesid")
async def update_agreement_mesid(form: model.UpdateAgreementMesid, service: AgreementService = Depends(dependencies.get_agreement_service)):
    return await service.update_agreement_mesid(form)

@router.post("/update")
async def update_agreement(form: model.UpdateAgreement, service: AgreementService = Depends(dependencies.get_agreement_service)):
    return await service.update_agreement(form)

@router.get("/get-mesid")
async def get_agreement_mesid(userid: int, service: AgreementService = Depends(dependencies.get_agreement_service)):
    return await service.get_agreement_mesid(userid)
