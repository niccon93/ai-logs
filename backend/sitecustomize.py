# Auto-loaded by Python on startup if present in sys.path.
# Provides KeysView/ValuesView/ItemsView under collections for legacy libs (e.g., drain3 on Python 3.10+).
import collections as _c, collections.abc as _abc
for _name in ("KeysView","ValuesView","ItemsView"):
    if not hasattr(_c, _name) and hasattr(_abc, _name):
        setattr(_c, _name, getattr(_abc, _name))
