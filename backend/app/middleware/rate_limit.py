
import os
from slowapi import Limiter
from slowapi.util import get_remote_address
DEFAULT_LIMIT = os.getenv("RATE_LIMIT_DEFAULT", "60/minute")
limiter = Limiter(key_func=get_remote_address, default_limits=[DEFAULT_LIMIT])
