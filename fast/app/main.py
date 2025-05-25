from fastapi import FastAPI
from fast.internal.repository.postgresql import db
from fast.internal.core.logging import logger
from fast.internal.api import user, ai
from fast.internal.repository.redis import db as redis_db

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(ai.router, prefix="/ai", tags=["Ai Model"])

@app.on_event('startup')
async def eventstart():
    try:
        app.state.pool = await db.create_pool()
        await db.init_db(app.state.pool)
        app.state.redis_pool = await redis_db.create_redis()
    except Exception as e:
        logger.error(f'[eventstart error]: {e}')

@app.on_event('shutdown')
async def shutdownevent():
    try:
        await app.state.pool.close()
    except Exception as e:
        logger.error(f'[shutdownevent error]: {e}')