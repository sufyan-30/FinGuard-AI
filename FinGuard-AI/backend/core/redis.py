"""Redis configuration and connection pooling"""

import os
import logging
from redis.asyncio import Redis, from_url
from redis.asyncio import ConnectionPool

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class RedisClient:
    """Async Redis client with connection pooling"""

    _instance: Redis = None

    @classmethod
    async def connect(cls) -> Redis:
        """Establish Redis connection"""
        if cls._instance is None:
            cls._instance = await from_url(
                REDIS_URL,
                encoding="utf8",
                decode_responses=True,
                max_connections=20,
            )
        return cls._instance

    @classmethod
    async def disconnect(cls) -> None:
        """Close Redis connection"""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None

    @classmethod
    async def get_client(cls) -> Redis:
        """Get or create Redis client"""
        if cls._instance is None:
            await cls.connect()
        return cls._instance


async def get_redis() -> Redis:
    """Dependency injection for Redis"""
    return await RedisClient.get_client()


async def redis_health_check() -> dict:
    """Check Redis connectivity"""
    try:
        redis = await RedisClient.get_client()
        await redis.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return {"status": "unhealthy", "redis": str(e)}
