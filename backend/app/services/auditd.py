
import re, datetime as dt
AUDIT_RE = re.compile(r"msg=audit\((?P<ts>\d+\.\d+):\d+\): (?P<body>.*)")
KEYVAL = re.compile(r"(\w+)=([^\s]+)")
def parse_audit_line(line: str):
    m = AUDIT_RE.search(line)
    if not m: return None
    ts = dt.datetime.utcfromtimestamp(float(m.group('ts')))
    body = {k:v for k,v in KEYVAL.findall(m.group('body'))}
    return {"ts": ts, **body}
