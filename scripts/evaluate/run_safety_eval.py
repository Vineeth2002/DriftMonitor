import os
import json
from datetime import datetime
from driftmonitor.benchmark.classifiers.safety_classifier import classify

RAW_DIR = "data/live/raw"
OUT_BASE = "data/live/processed"

def load_today_items():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    day_dir = os.path.join(RAW_DIR, today)

    items = []
    if not os.path.isdir(day_dir):
        return today, items

    for f in os.listdir(day_dir):
        if f.endswith(".json"):
            with open(os.path.join(day_dir, f), encoding="utf-8") as fh:
                data = json.load(fh)
                items.extend(data.get("items", []))

    return today, items


def main():
    today, items = load_today_items()
    out_dir = os.path.join(OUT_BASE, today)
    os.makedirs(out_dir, exist_ok=True)

    evaluated = []
    counts = {"SAFE": 0, "WARNING": 0, "RISKY": 0}

    for item in items:
        text = (item.get("title", "") + " " + item.get("text", "")).strip()
        result = classify(text)
        counts[result["risk_label"]] += 1

        evaluated.append({
            "source": item.get("source"),
            "title": item.get("title"),
            "risk_score": result["risk_score"],
            "risk_label": result["risk_label"],
            "reason": result["reason"],
        })

    eval_file = os.path.join(out_dir, "safety_eval.json")
    summary_file = os.path.join(out_dir, "safety_summary.json")

    with open(eval_file, "w", encoding="utf-8") as f:
        json.dump(evaluated, f, indent=2)

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump({
            "date": today,
            "total_items": len(items),
            "risk_breakdown": counts,
        }, f, indent=2)

    print("Safety evaluation complete for", today)

if __name__ == "__main__":
    main()
