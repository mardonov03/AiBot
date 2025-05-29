from fast.internal.core.logging import logger
from datetime import datetime

class AiRepository:
    def __init__(self, pool):
        self.pool = pool

    async def get_last_session(self, userid: int):
        try:
            async with self.pool.acquire() as conn:
                return await conn.fetchrow("SELECT sessionid, added_time FROM user_sessions WHERE userid = $1 ORDER BY added_time DESC LIMIT 1", userid)
        except Exception as e:
            logger.error(f'[get_last_session error] {e}')
            raise

    async def get_last_user_message_time(self, userid: int, sessionid: int) -> datetime | None:
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("SELECT added_time FROM session_messages WHERE userid = $1 AND sessionid = $2 AND role = 'user' ORDER BY added_time DESC LIMIT 1", userid, sessionid)
                return row["added_time"] if row else None
        except Exception as e:
            logger.error(f'[get_last_user_message_time error] {e}')
            raise

    async def create_new_session(self, userid: int, title: str) -> int:
        try:
            async with self.pool.acquire() as conn:
                sessionid = await conn.fetchval("INSERT INTO user_sessions (userid, title) VALUES ($1, $2) RETURNING sessionid", userid, title)
                return sessionid
        except Exception as e:
            logger.error(f'[create_new_session error] {e}')
            raise

    async def get_chat_messages(self, sessionid: int, userid: int):
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch("SELECT role, message FROM session_messages WHERE sessionid = $1 AND userid = $2 ORDER BY added_time ASC;", sessionid, userid)
                return [{"role": row["role"], "content": row["message"]} for row in rows]
        except Exception as e:
            logger.error(f'[get_chat_messages error] {e}')
            raise

    async def save_message(self, sessionid: int, userid: int, role: str, message: str):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("INSERT INTO session_messages (sessionid, userid, role, message, added_time) VALUES ($1, $2, $3, $4, NOW())", sessionid, userid, role, message)
        except Exception as e:
            logger.error(f'[save_message error] {e}')
            raise
