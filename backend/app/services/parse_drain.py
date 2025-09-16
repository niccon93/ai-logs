from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig

# Build miner with safe defaults; do not require drain3.ini present.
def _build_miner() -> TemplateMiner:
    cfg = TemplateMinerConfig()
    # Defaults tuned light; no file loading to avoid missing 'drain3.ini' error.
    cfg.load_default(None)  # in drain3 0.9.9 available and safe with None
    cfg.profiling_enabled = False
    cfg.drain_sim_th = 0.4
    cfg.drain_depth = 4
    return TemplateMiner(cfg)

miner = _build_miner()

def parse_lines(lines):
    results = []
    for ln in lines:
        r = miner.add_log_message(ln.rstrip())
        if r and "change_type" in r and r["change_type"]:
            results.append({"cluster_id": r.get("cluster_id"), "template_mined": r.get("template_mined")})
    return results
