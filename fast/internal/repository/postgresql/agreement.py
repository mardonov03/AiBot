from fast.internal.core.logging import logger
from fast.internal.models import agreement as model

class AgreementRepository:
    def __init__(self, pool):
        self.pool = pool

    async def get_agreement_mesid(self, userid: int) -> int | None:
        try:
            async with self.pool.acquire() as conn:
                mesid = await conn.fetchval("SELECT mesid FROM user_agreement WHERE userid = $1", userid)
                if mesid:
                    return mesid
        except Exception as e:
            logger.error(f'[get_agreement_mesid repo error]: {e}')


    async def update_agreement_mesid(self, form: model.UpdateAgreementMesid):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("UPDATE user_agreement SET mesid = $1 WHERE userid = $2", form.mesid, form.userid)
        except Exception as e:
            logger.error(f'[add_user repo error]: {e}')
