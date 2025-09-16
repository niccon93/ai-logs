
import hashlib, json
from ..services.pubsub import get_redis
def _key(task_name: str, args, kwargs):
    h = hashlib.sha256(json.dumps([task_name, args, kwargs], default=str).encode()).hexdigest()
    return f"tasks:dedupe:{task_name}:{h}"
async def acquire_dedupe(task_name: str, args, kwargs, ttl: int = 3600) -> bool:
    r = get_redis(); ok = await r.setnx(_key(task_name,args,kwargs), "1")
    if ok: await r.expire(_key(task_name,args,kwargs), ttl)
    return ok
async def release_dedupe(task_name: str, args, kwargs):
    r = get_redis(); await r.delete(_key(task_name,args,kwargs))
