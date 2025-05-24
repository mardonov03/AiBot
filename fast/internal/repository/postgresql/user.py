from fast.internal.core.logging import logger
from fast.internal.models import user as model

class UserRepository:
    def __init__(self, pool):
        self.pool = pool

    async def add_user(self, user: model.AddUser):
        try:
            async with self.pool.acquire() as conn:
                return "test"
        except Exception as e:
            logger.error(f'[add_user error]: {e}')