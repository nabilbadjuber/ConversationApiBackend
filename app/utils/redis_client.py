import redis.asyncio as redis
import os

_redis = None

def get_redis_client():
    global _redis
    if _redis is None:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        _redis = redis.from_url(redis_url, decode_responses=True)
    return _redis