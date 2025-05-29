from fast.internal.core.logging import logger
from fast.internal.models import user as model

class UserRepository:
    def __init__(self, pool):
        self.pool = pool

    async def add_user(self, user: model.AddUser):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute('INSERT INTO users (userid, full_name, username) VALUES ($1, $2, $3)',user.userid, user.full_name, user.username)
                await conn.execute('INSERT INTO user_agreement (userid) VALUES ($1)',user.userid)
                await conn.execute('INSERT INTO user_states (userid) VALUES ($1)',user.userid)
        except Exception as e:
            logger.error(f'[add_user error]: {e}')

    async def get_user_data(self, userid: int) -> model.InfoUser | None:
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("SELECT u.userid, u.full_name, u.username, u.added_time, a.status FROM users AS u JOIN user_agreement AS a ON u.userid = a.userid WHERE u.userid = $1", userid)
                if row is None:
                    return None
                return model.InfoUser(**dict(row))
        except Exception as e:
            logger.error(f'[get_user_data error]: {e}')
