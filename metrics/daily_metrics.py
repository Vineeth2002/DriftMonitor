import json
from pathlib import Path
from collections import Counter

def compute_daily_metrics(evaluated_file: Path) -> dict:
    data = json.loads(evaluated_file.read_text(encoding="utf-8"))

    items = data.get("items", [])
    total = len(items)

    risk_counts = Counter()
    for i in items:
        risk_counts[i.get("risk_label", "UNKNOWN")] += 1

    return {
        "date": data.get("date"),
        "total": total,
        "risk_breakdown": dict(risk_counts),
    }
