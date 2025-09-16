
from .nginx import parse_line as parse_nginx
from .apache import parse_line as parse_apache
def detect(filename: str):
    f = filename.lower()
    if "nginx" in f: return "nginx"
    if "apache" in f or "httpd" in f: return "apache"
    return "drain"
def parse_line(filename: str, line: str):
    typ = detect(filename)
    if typ == "nginx":
        return {"type":"nginx", "data": parse_nginx(line)}
    if typ == "apache":
        return {"type":"apache", "data": parse_apache(line)}
    return {"type":"drain", "data": {"raw": line.strip()}}
