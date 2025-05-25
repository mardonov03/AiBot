from fast.internal.repository.postgresql.agreement import AgreementRepository
from fast.internal.models import agreement as model
from fast.internal.core.logging import logger


class AgreementService:
    def __init__(self, pool):
        self.psql_repo = AgreementRepository(pool)

    async def get_agreement_mesid(self, userid: int):
        try:
            return await self.psql_repo.get_agreement_mesid(userid)
        except Exception as e:
            logger.error(f'[get_agreement_mesid service error]: {e}')

    async def update_agreement_mesid(self, form: model.UpdateAgreementMesid):
        try:
            return await self.psql_repo.update_agreement_mesid(form)
        except Exception as e:
            logger.error(f'[update_agreement_mesid service error]: {e}')

    async def update_agreement(self, form: model.UpdateAgreement):
        try:
            await self.psql_repo.update_agreement(form)
            return {'status': 'ok'}
        except Exception as e:
            logger.error(f'[update_agreement service error]: {e}')
