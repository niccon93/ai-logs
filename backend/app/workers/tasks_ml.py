
from .celery_app import app

@app.task(name="ml.train")
def ml_train(dataset_id: int, backend: str = "logai", params: dict | None = None):
    if backend == "logai":
        from app.services.logai_adapter import train as run
    elif backend == "loglizer":
        from app.services.loglizer_adapter import train as run
    else:
        raise ValueError(f"Unknown backend: {backend}")
    return run(dataset_id, params or {})

@app.task(name="ml.infer")
def ml_infer(dataset_id: int, model_id: int, backend: str = "logai", params: dict | None = None):
    if backend == "logai":
        from app.services.logai_adapter import infer as run
    elif backend == "loglizer":
        from app.services.loglizer_adapter import infer as run
    else:
        raise ValueError(f"Unknown backend: {backend}")
    return run(dataset_id, model_id, params or {})
