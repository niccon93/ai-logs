
import os
from opensearchpy import OpenSearch
OS_ENABLED = os.getenv("ENABLE_OPENSEARCH","").lower() in ("1","true","yes")
def client():
    host = os.getenv("OPENSEARCH_HOST","opensearch")
    port = int(os.getenv("OPENSEARCH_PORT","9200"))
    return OpenSearch([{"host": host, "port": port, "scheme":"http"}], verify_certs=False)
def ensure_index(name="findings"):
    if not OS_ENABLED: return False
    osclient = client()
    if not osclient.indices.exists(name):
        osclient.indices.create(name, body={
            "settings":{"index":{"number_of_shards":1,"number_of_replicas":0}},
            "mappings":{"properties":{
                "ts":{"type":"date"},
                "severity":{"type":"keyword"},
                "host":{"type":"keyword"},
                "app":{"type":"keyword"},
                "message":{"type":"text"},
                "template_id":{"type":"keyword"}
            }}
        })
    return True
def index_finding(doc: dict, index="findings"):
    if not OS_ENABLED: return False
    ensure_index(index)
    client().index(index=index, document=doc)
    return True
