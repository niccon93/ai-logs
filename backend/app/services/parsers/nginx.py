
import re
# Very simple NGINX access log regex (common/combined)
# Example: 127.0.0.1 - - [12/Mar/2024:19:21:01 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.68.0"
NGINX_RE = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+"(?P<method>\S+)\s(?P<path>\S+)\s(?P<proto>[^"]+)"\s+(?P<status>\d+)\s+(?P<size>\d+)\s+"(?P<ref>[^"]*)"\s+"(?P<ua>[^"]*)"'
)
def parse_line(line: str):
    m = NGINX_RE.search(line)
    if not m: return None
    d = m.groupdict()
    return {
        "ip": d["ip"], "time": d["time"], "method": d["method"], "path": d["path"],
        "proto": d["proto"], "status": int(d["status"]), "size": int(d["size"]),
        "ref": d["ref"], "ua": d["ua"], "raw": line.strip()
    }
