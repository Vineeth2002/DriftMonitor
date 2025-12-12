from datetime import datetime
from pathlib import Path
import json

from driftmonitor.collectors.google_trends.collector import collect_google_trends
from driftmonitor.collectors.hackernews.collector import collect_hackernews

TODAY = datetime.utcnow().strftime("%Y-%m-%d")
RAW_DIR = Path(f"data/live/raw/{TODAY}")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def main():
    google_data = collect_google_trends()
    hn_data = collect_hackernews()

    with open(RAW_DIR / "google_trends.json", "w") as f:
        json.dump(google_data, f, indent=2)

    with open(RAW_DIR / "hackernews.json", "w") as f:
        json.dump(hn_data, f, indent=2)

    print(f"[OK] Raw data collected for {TODAY}")

if __name__ == "__main__":
    main()
