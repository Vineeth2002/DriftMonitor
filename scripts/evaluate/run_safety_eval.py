#!/usr/bin/env python3
"""
Run safety evaluation on collected data.

Must be executed as:
python -m scripts.evaluate.run_safety_eval
"""

import json
from pathlib import Path
from datetime import datetime, timezone

from driftmonitor.benchmark.classifiers.safety_classifier import SafetyClassifier

RAW_BASE = Path("data/live/raw")
OUT_BASE = Path("data/live/processed")


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw_dir = RAW_BASE / today
    out_dir = OUT_BASE / today
    out_dir.mkdir(parents=True, exist_ok=True)

    clf = SafetyClassifier()
    evaluated = []

    for fname in ["google_trends.json", "hackernews.json"]:
        path = raw_dir / fname
        if not path.exists():
            continue

        data = json.loads(path.read_text(encoding="utf-8"))
        texts = [r["text"] for r in data.get("results", [])]
        scores = clf.score_texts(texts)

        for r, s in zip(data.get("results", []), scores):
            evaluated.append({**r, **s})

    (out_dir / "evaluated.json").write_text(
        json.dumps(
            {
                "date": today,
                "total": len(evaluated),
                "items": evaluated,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"[OK] Evaluated {len(evaluated)} items")


if __name__ == "__main__":
    main()
