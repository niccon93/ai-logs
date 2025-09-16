
import os
from cryptography.fernet import Fernet, MultiFernet
def _get_fernet():
    keys = [k for k in os.getenv("FERNET_KEYS","").split(";") if k]
    if not keys: keys = [Fernet.generate_key().decode()]
    return MultiFernet([Fernet(k.encode()) for k in keys])
fernet = _get_fernet()
def encrypt_bytes(data: bytes) -> bytes: return fernet.encrypt(data)
def decrypt_bytes(token: bytes) -> bytes: return fernet.decrypt(token)
