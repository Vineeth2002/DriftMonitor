from datetime import date
from pathlib import Path
import json

TODAY = date.today().isoformat()

RAW_DIR = Path("data/live/raw") / TODAY
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Example save
with open(RAW_DIR / "google_trends.json", "w") as f:
    json.dump(google_results, f, indent=2)

with open(RAW_DIR / "hackernews.json", "w") as f:
    json.dump(hn_results, f, indent=2)
