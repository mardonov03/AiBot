from fast.internal.repository.postgresql.user import UserRepository
from fast.internal.repository.redis.user import RedisUserRepository
from fast.internal.models import user as model
from fast.internal.core.logging import logger


class UserService:
    def __init__(self, pool, redis_pool):
        self.psql_repo = UserRepository(pool)
        self.redis_repo = RedisUserRepository(redis_pool)

    async def add_user(self, user: model.AddUser):
        try:
            return await self.psql_repo.add_user(user)
        except Exception as e:
            logger.error(f'[add_user error]: {e}')