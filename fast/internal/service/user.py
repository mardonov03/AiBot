from fast.internal.repository.postgresql.user import UserRepository
from fast.internal.repository.redis.user import RedisUserRepository
from fast.internal.models import user as model
from fast.internal.core.logging import logger


class UserService:
    def __init__(self, pool, redis_pool):
        self.psql_repo = UserRepository(pool)
        self.redis_repo = RedisUserRepository(redis_pool)

    async def init_or_deny(self, user: model.AddUser):
        try:
            existing = await self.psql_repo.get_user_data(user.userid)

            if not existing:
                await self.psql_repo.add_user(user)
                return {"agreement_status": "need_agreement"}

            if not existing.agreement_status:
                return {"agreement_status": "need_agreement"}

            return {"agreement_status": "ok"}

        except Exception as e:
            logger.error(f'[init_or_deny error]: {e}')
            return {"agreement_status": "error"}

    async def get_user_data(self, userid: int):
        try:
            return await self.psql_repo.get_user_data(userid)
        except Exception as e:
            logger.error(f'[get_user_data error]: {e}')

