
try:
    from logai.initiators import LogAIInitiator
    from logai.utils.dataset import LogDataset
except Exception:
    LogAIInitiator = None
class LogAIAdapter:
    def __init__(self, config: dict): self.cfg=config
    def fit_predict(self, df):
        if not LogAIInitiator: raise RuntimeError("logai not installed")
        app = LogAIInitiator(self.cfg); dataset = LogDataset(df); return app.run(dataset)
