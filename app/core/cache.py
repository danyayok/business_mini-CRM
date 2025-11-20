import redis
import json
from app.core.config import settings

redis_client = redis.from_url(settings.redis_url)

def get_cache(key: str):
    val = redis_client.get(key)
    return json.loads(val) if val else None

def set_cache(key: str, value, ttl: int = 300):
    redis_client.setex(key, ttl, json.dumps(value))

def delete_cache(key: str):
    redis_client.delete(key)