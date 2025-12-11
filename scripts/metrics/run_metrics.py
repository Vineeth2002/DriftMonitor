#!/usr/bin/env python3
"""
Metrics runner for DriftMonitor

- Loads two processed evaluation JSON files (either specified or picks the two latest)
- Computes distributional drift (JSD) between them using metrics.utils
- Computes toxicity summaries for each evaluation
- Writes a drift summary JSON to the processed output directory:
    data/live/processed/drift_summary_<timestamp>.json

CLI:
    python -m driftmonitor.scripts.metrics.run_metrics
    python -m driftmonitor.scripts.metrics.run_metrics --eval-a path/to/a.json --eval-b path/to/b.json
    python -m driftmonitor.scripts.metrics.run_metrics --processed-dir data/live/processed --output-dir data/live/processed
"""

from __future__ import annotations
import argparse
import glob
import json
import logging
import os
from datetime import datetime
from typing import Optional

from driftmonitor.metrics.utils import compute_drift_between, toxicity_summary_of

logger = logging.getLogger("driftmonitor.scripts.metrics.run_metrics")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def _pick_latest_two(processed_dir: str):
    files = sorted(glob.glob(os.path.join(processed_dir, "eval_*.json")))
    if len(files) >= 2:
        return files[-2], files[-1]
    elif len(files) == 1:
        return files[0], files[0]
    else:
        return None, None


def compute_drift_and_write(
    processed_dir: str = "data/live/processed",
    output_dir: Optional[str] = None,
    eval_a_path: Optional[str] = None,
    eval_b_path: Optional[str] = None,
) -> str:
    """
    Compute drift summary and write JSON. Returns the path to the written summary file.

    If eval_a_path / eval_b_path are provided, uses them. Otherwise it picks the two latest
    eval_*.json files from processed_dir (if only one is present, compares it to itself).
    """
    processed_dir = os.path.abspath(processed_dir)
    output_dir = os.path.abspath(output_dir or processed_dir)
    os.makedirs(output_dir, exist_ok=True)

    if eval_a_path and eval_b_path:
        a_path = os.path.abspath(eval_a_path)
        b_path = os.path.abspath(eval_b_path)
    else:
        a_path, b_path = _pick_latest_two(processed_dir)

    if not a_path or not b_path:
        raise RuntimeError(f"No processed evaluation files found in {processed_dir}")

    logger.info("Using evaluation files:\n A: %s\n B: %s", a_path, b_path)

    with open(a_path, "r", encoding="utf-8") as fa:
        eval_a = json.load(fa)
    with open(b_path, "r", encoding="utf-8") as fb:
        eval_b = json.load(fb)

    # Compute drift (JSD) and toxicity summaries
    drift = compute_drift_between(eval_a, eval_b)
    tox_a = toxicity_summary_of(eval_a)
    tox_b = toxicity_summary_of(eval_b)

    summary = {
        "computed_at": datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
        "eval_a": os.path.basename(a_path),
        "eval_b": os.path.basename(b_path),
        "drift": drift,
        "toxicity_a": tox_a,
        "toxicity_b": tox_b,
    }

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_file = os.path.join(output_dir, f"drift_summary_{ts}.json")
    with open(out_file, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)

    logger.info("Wrote drift summary to %s", out_file)
    return out_file


def main():
    parser = argparse.ArgumentParser(description="DriftMonitor metrics runner: compute drift & toxicity summary.")
    parser.add_argument("--processed-dir", default="data/live/processed", help="Directory containing eval_*.json files.")
    parser.add_argument("--output-dir", default=None, help="Where to write drift summary (defaults to processed-dir).")
    parser.add_argument("--eval-a", default=None, help="Path to eval A JSON (optional).")
    parser.add_argument("--eval-b", default=None, help="Path to eval B JSON (optional).")
    args = parser.parse_args()

    path = compute_drift_and_write(
        processed_dir=args.processed_dir,
        output_dir=args.output_dir,
        eval_a_path=args.eval_a,
        eval_b_path=args.eval_b,
    )
    print(f"Drift summary written: {path}")


if __name__ == "__main__":
    main()
