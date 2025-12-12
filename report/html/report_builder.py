from pathlib import Path
import json

PROCESSED_DIR = Path("data/live/processed")

def get_latest_date():
    dates = sorted(d.name for d in PROCESSED_DIR.iterdir() if d.is_dir())
    return dates[-1]

def load_latest_results():
    latest = get_latest_date()
    with open(PROCESSED_DIR / latest / "safety_results.json") as f:
        return json.load(f), latest
