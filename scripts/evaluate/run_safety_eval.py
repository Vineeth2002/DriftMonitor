import json
import os
from datetime import datetime, timezone

from driftmonitor.benchmark.classifiers.safety_classifier import SafetyClassifier

RAW_BASE = "data/live/raw"
PROC_BASE = "data/live/processed"

def today_dir():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    date = today_dir()
    raw_dir = f"{RAW_BASE}/{date}"
    out_dir = f"{PROC_BASE}/{date}"

    os.makedirs(out_dir, exist_ok=True)

    classifier = SafetyClassifier()

    evaluated = []

    for fname in ["google_trends.json", "hackernews.json"]:
        path = f"{raw_dir}/{fname}"
        if not os.path.exists(path):
            continue

        data = load_json(path)
        texts = [r["text"] for r in data["results"]]

        scores = classifier.score_texts(texts)

        for r, s in zip(data["results"], scores):
            evaluated.append({
                **r,
                **s,
                "evaluated_at": datetime.now(timezone.utc).isoformat()
            })

    save_json(f"{out_dir}/evaluated.json", evaluated)
    print(f"[EVALUATE] Saved {len(evaluated)} items")

if __name__ == "__main__":
    main()
