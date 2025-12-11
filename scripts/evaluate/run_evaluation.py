#!/usr/bin/env python3
"""
Run Evaluation Pipeline for DriftMonitor.

This script:
- Loads the newest collected raw data from data/live/raw
- Merges Google Trends + HackerNews + Custom Prompts items
- Applies the SafetyClassifier to all text fields
- Saves processed results to data/live/processed/eval_<timestamp>.json
- Lightweight and GitHub Actions friendly
"""

from __future__ import annotations
import os
import json
import glob
import logging
from datetime import datetime
from typing import List, Dict, Any

from driftmonitor.benchmark.classifiers.safety_classifier import SafetyClassifier
from .utils import load_latest_json, extract_text_fields

logger = logging.getLogger("driftmonitor.scripts.evaluate")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

RAW_DIR = os.path.abspath("data/live/raw")
PROCESSED_DIR = os.path.abspath("data/live/processed")


def evaluate() -> str:
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # Load latest raw files
    raw_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.json")))
    if not raw_files:
        raise RuntimeError("No raw data found in data/live/raw")

    logger.info("Found %d raw data files", len(raw_files))

    all_items: List[Dict[str, Any]] = []
    for file in raw_files:
        loaded = load_latest_json(file)
        results = loaded.get("results", [])
        all_items.extend(results)

    logger.info("Total combined items: %d", len(all_items))

    # Extract text fields for classification
    texts = extract_text_fields(all_items)
    logger.info("Extracted %d text fields to classify", len(texts))

    clf = SafetyClassifier()
    safety_results = clf.score_texts(texts)

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    output_file = os.path.join(PROCESSED_DIR, f"eval_{ts}.json")

    final_output = {
        "evaluated_at": ts,
        "n_texts": len(texts),
        "safety_results": safety_results,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    logger.info("Saved evaluation output → %s", output_file)
    return output_file


if __name__ == "__main__":
    path = evaluate()
    print(f"Evaluation complete: {path}")
