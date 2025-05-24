import redis.asyncio as aioredis
from fast.internal.core import config
from fast.internal.core.logging import logger

async def create_redis():
    try:
        redis = aioredis.from_url(f"redis://{config.settings.REDIS_HOST}:{config.settings.REDIS_PORT}",decode_responses=True)
        return redis
    except Exception as e:
        logger.error(f"create_redis error: {e}")
