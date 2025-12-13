#!/usr/bin/env python3
"""
Run all collectors and store raw data.

IMPORTANT:
- Must be executed as a module:
  python -m scripts.collect.run_collectors
"""

import json
from pathlib import Path
from datetime import datetime, timezone

from driftmonitor.collectors.google_trends import collect_google_trends
from driftmonitor.collectors.hackernews import collect_hackernews

RAW_BASE = Path("data/live/raw")


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = RAW_BASE / today
    out_dir.mkdir(parents=True, exist_ok=True)

    google = collect_google_trends()
    hn = collect_hackernews()

    (out_dir / "google_trends.json").write_text(
        json.dumps(google, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    (out_dir / "hackernews.json").write_text(
        json.dumps(hn, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"[OK] Collected data for {today}")


if __name__ == "__main__":
    main()
