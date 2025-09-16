
from .celery_app import app

@app.task(name="parse.run")
def parse_run(dataset_id: int, lines: list[str] | None = None):
    # Импортируем drain3 ТОЛЬКО в parse-воркере
    from app.services.parse_drain import parse_lines
    data = parse_lines(lines or ["demo line A", "demo line B"])
    return {"dataset_id": dataset_id, "parsed": len(data)}
