
from .celery_app import celery
from ..services.pubsub import get_redis, json_dumps
from ..services.streams import xadd
@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries':5})
def task_dummy(self, payload: dict):
    publish_progress(self.request.id, "start", 1)
    publish_progress(self.request.id, "half", 50)
    publish_progress(self.request.id, "done", 100)
    return {"ok": True}
def publish_progress(task_id: str, stage: str, progress: int, **extra):
    payload = {"task_id": task_id, "stage": stage, "progress": progress, **extra}
    r = get_redis(); ch = f"jobs:{task_id}"
    import asyncio; loop = asyncio.get_event_loop()
    loop.create_task(r.publish(ch, json_dumps(payload)))
    loop.create_task(r.publish("jobs:all", json_dumps(payload)))
    loop.create_task(xadd(ch, payload)); loop.create_task(xadd("jobs:all", payload))
