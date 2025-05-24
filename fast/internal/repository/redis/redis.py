from fast.internal.repository.redis.user import RedisUserRepository
from fast.internal.repository.redis.menu import RedisMenuRepository

class RedisRepo:
    def __init__(self, redis):
        self.redis = redis
        self.user = RedisUserRepository(redis)
