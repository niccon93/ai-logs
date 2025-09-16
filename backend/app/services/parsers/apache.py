
import re
# Simple Apache combined log format regex
APACHE_RE = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+"(?P<method>\S+)\s(?P<path>\S+)\s(?P<proto>[^"]+)"\s+(?P<status>\d+)\s+(?P<size>\S+)\s+"(?P<ref>[^"]*)"\s+"(?P<ua>[^"]*)"'
)
def parse_line(line: str):
    m = APACHE_RE.search(line)
    if not m: return None
    d = m.groupdict()
    size = 0 if d["size"] == '-' else int(d["size"])
    return {
        "ip": d["ip"], "time": d["time"], "method": d["method"], "path": d["path"],
        "proto": d["proto"], "status": int(d["status"]), "size": size,
        "ref": d["ref"], "ua": d["ua"], "raw": line.strip()
    }
