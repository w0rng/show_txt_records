import asyncio
from functools import wraps
from json import dumps, loads

import redis.asyncio as redis
from config import redis_config
from logger import get_logger

logger = get_logger(__name__)


class RedisConnector:
    def __init__(self):
        if not redis_config.use:
            logger.info("Redis is disabled")
            return
        pool = redis.ConnectionPool.from_url(redis_config.get_url(), max_connections=redis_config.pool_size)
        self.redis = redis.Redis(connection_pool=pool)

    async def get(self, key: str) -> str:
        logger.debug("Getting %s from Redis", key)
        return await self.redis.get(key)

    async def set(self, key: str, value: str) -> None:
        logger.debug("Setting %s in Redis", key)
        await self.redis.set(key, value)


redis_connector = RedisConnector()


def cache_redis(ttl: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if redis_config.use:
                result = await redis_connector.get(args[0])
                if result:
                    return loads(result)
            result = await func(*args, **kwargs)
            if redis_config.use:
                await asyncio.gather(
                    redis_connector.set(args[0], dumps(result)),
                    redis_connector.redis.expire(args[0], ttl),
                )
            return result

        return wrapper

    return decorator


__all__ = ["cache_redis"]
