
import os, json
from redis.asyncio import Redis
_redis=None
def get_redis():
    global _redis
    if _redis is None:
        url = os.getenv("REDIS_URL","redis://redis:6379/0"); _redis = Redis.from_url(url, encoding="utf-8", decode_responses=True)
    return _redis
def json_dumps(o): return json.dumps(o, default=str, ensure_ascii=False)
