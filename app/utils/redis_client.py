import redis.asyncio as redis

_redis = None

def get_redis_client():
    global _redis
    if _redis is None:
        _redis = redis.from_url("redis://localhost:6379", decode_responses=True)
    return _redis