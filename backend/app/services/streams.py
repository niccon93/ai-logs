
from .pubsub import get_redis, json_dumps
async def xadd(channel: str, message: dict, maxlen: int = 2000):
    r = get_redis(); await r.xadd(channel, {"data": json_dumps(message)}, maxlen=maxlen, approximate=True)
