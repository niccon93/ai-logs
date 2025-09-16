from celery import Celery
import os

broker = os.getenv("REDIS_URL", "redis://redis:6379/0")
backend = broker

celery_app = Celery("ai_logs", broker=broker, backend=backend)
celery_app.conf.task_default_queue = "default"

@celery_app.task(name="enqueue_parse")
def enqueue_parse(lines):
    # Placeholder task; real parse is done inline in API preview or here for batch
    from ..services.parse_drain import parse_lines
    return parse_lines(lines)
