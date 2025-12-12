#!/usr/bin/env python3
# driftmonitor/scripts/metrics/run_metrics.py
import json
import os
from glob import glob
from statistics import mean
from datetime import datetime

PROCESSED = os.path.abspath("data/live/processed")
OUT = os.path.abspath("data/live/processed/drift_summary.json")

def load_latest_eval_files(n=2):
    files = sorted(glob(os.path.join(PROCESSED, "eval_*.json")), reverse=True)
    return files[:n]

def compute_simple_kl(p, q, eps=1e-9):
    # tiny approximate metric using binary bins: safe vs risky
    import math
    p = max(eps, min(1-eps, p))
    q = max(eps, min(1-eps, q))
    return p * math.log(p/q) + (1-p) * math.log((1-p)/(1-q))

def run():
    files = load_latest_eval_files(2)
    if len(files) < 2:
        print("Not enough eval files for drift computation")
        return {}
    stats = {}
    def score_from_file(f):
        try:
            data = json.load(open(f, "r", encoding="utf-8"))
            scores = [x.get("safety_score", 1.0) for x in data if isinstance(x, dict)]
            return mean(scores) if scores else 1.0
        except Exception:
            return 1.0
    s0 = score_from_file(files[0])
    s1 = score_from_file(files[1])
    kl = compute_simple_kl(s0, s1)
    stats = {"ts": datetime.utcnow().isoformat(), "files": files, "mean_scores": [s0, s1], "kl_approx": kl}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print("Drift summary written to", OUT)
    return stats

if __name__ == "__main__":
    run()
