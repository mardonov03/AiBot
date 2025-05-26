import asyncpg
from fast.internal.core import config
from fast.internal.core.logging import logger

async def create_pool():
    try:
        pool = await asyncpg.create_pool(
            user=config.settings.DB_USER,
            password=config.settings.DB_PASS,
            database=config.settings.DB_NAME,
            host=config.settings.DB_HOST,
            port=config.settings.DB_PORT,
            min_size=1,
            max_size=10
        )
        return pool
    except Exception as e:
        logger.error(f'create_pool error: {e}')


async def init_db(pool):
    try:
        async with pool.acquire() as conn:

            await conn.execute("""DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'session_types') THEN
                        CREATE TYPE session_types AS ENUM ('create_task','answer');
                    END IF;
                END$$;
                """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    userid BIGINT PRIMARY KEY,
                    username TEXT UNIQUE,
                    full_name TEXT,
                    added_time TIMESTAMP DEFAULT now()
                );
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_agreement (
                    userid BIGINT PRIMARY KEY REFERENCES users(userid) ON DELETE CASCADE,
                    agreement_status BOOLEAN NOT NULL DEFAULT FALSE,
                    mesid BIGINT,
                    update_time TIMESTAMP NOT NULL DEFAULT NOW()
                );
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_states (
                    userid BIGINT PRIMARY KEY REFERENCES users(userid) ON DELETE CASCADE
                );
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    userid BIGINT NOT NULL,
                    sessionid INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    context TEXT NOT NULL,
                    type session_types NOT NULL DEFAULT 'answer',
                    added_time TIMESTAMP DEFAULT now(),
                    PRIMARY KEY (userid, sessionid),
                    FOREIGN KEY (userid) REFERENCES users(userid) ON DELETE CASCADE
                );
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS session_messages (
                    userid BIGINT NOT NULL,
                    sessionid INTEGER NOT NULL,
                    role TEXT NOT NULL, -- 'user' или 'assistant'
                    message TEXT NOT NULL,
                    added_time TIMESTAMP DEFAULT now(),
                    FOREIGN KEY (userid, sessionid) REFERENCES user_sessions(userid, sessionid) ON DELETE CASCADE
                );
            """)

    except Exception as e:
        logger.error(f'init_db error: {e}')