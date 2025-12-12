import json
import os
from datetime import datetime, timezone

from driftmonitor.collectors.google_trends.collector import collect_google_trends
from driftmonitor.collectors.hackernews.collector import collect_hackernews

BASE_DIR = "data/live/raw"

def today_dir():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    date = today_dir()
    out_dir = os.path.join(BASE_DIR, date)
    ensure_dir(out_dir)

    print(f"[COLLECT] Saving raw data to {out_dir}")

    google_data = collect_google_trends()
    hn_data = collect_hackernews()

    save_json(f"{out_dir}/google_trends.json", google_data)
    save_json(f"{out_dir}/hackernews.json", hn_data)

    print("[COLLECT] Done")

if __name__ == "__main__":
    main()
