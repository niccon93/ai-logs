
try:
    from loglizer.models import PCA
except Exception:
    PCA = None
class LoglizerAdapter:
    def __init__(self): self.model=None
    def fit(self, x):
        if not PCA: raise RuntimeError("loglizer not installed")
        self.model = PCA(); self.model.fit(x)
    def predict(self, x): return self.model.predict(x)
