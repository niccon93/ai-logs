
import paramiko, io
def try_connect(host: str, port: int, username: str, password: str | None = None, private_key: str | None = None):
    try:
        client = paramiko.SSHClient(); client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if private_key:
            pkey = paramiko.RSAKey.from_private_key(io.StringIO(private_key))
            client.connect(host, port=port, username=username, pkey=pkey, timeout=5)
        else:
            client.connect(host, port=port, username=username, password=password, timeout=5)
        fp = client.get_transport().get_remote_server_key().get_fingerprint(); client.close()
        return True, ':'.join('{:02x}'.format(b) for b in fp)
    except Exception: return False, None
