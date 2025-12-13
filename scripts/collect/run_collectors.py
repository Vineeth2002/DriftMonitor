import json
from pathlib import Path
from datetime import datetime, timezone

from driftmonitor.collectors.google_trends.collector import collect_google_trends
from driftmonitor.collectors.hackernews.collector import collect_hackernews

BASE = Path("data/live/raw")

def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = BASE / today
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
