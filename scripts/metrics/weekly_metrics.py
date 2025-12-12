import os
import json
from datetime import datetime, timedelta
from collections import Counter

RAW_DIR = "data/live/raw"
OUT_DIR = "data/live/processed/weekly"

def load_last_7_days():
    today = datetime.utcnow().date()
    days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    all_items = []

    for d in days:
        day_dir = os.path.join(RAW_DIR, d)
        if not os.path.isdir(day_dir):
            continue

        for fname in os.listdir(day_dir):
            if fname.endswith(".json"):
                with open(os.path.join(day_dir, fname), encoding="utf-8") as f:
                    data = json.load(f)
                    all_items.extend(data.get("items", []))

    return all_items

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    items = load_last_7_days()

    source_count = Counter()
    keywords = Counter()

    for item in items:
        if "title" in item:
            keywords.update(item["title"].lower().split())
        source_count[item.get("source", "unknown")] += 1

    summary = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "window": "last_7_days",
        "total_items": len(items),
        "source_distribution": dict(source_count),
        "top_keywords": keywords.most_common(20)
    }

    out_file = f"{OUT_DIR}/weekly_{datetime.utcnow().strftime('%Y-%m-%d')}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("Weekly summary written:", out_file)

if __name__ == "__main__":
    main()
