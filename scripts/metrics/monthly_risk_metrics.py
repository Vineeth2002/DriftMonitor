import os
import json
from datetime import datetime
from collections import Counter

BASE = "data/live/processed"

def main():
    month = datetime.utcnow().strftime("%Y-%m")
    agg = Counter()
    total = 0

    for d in os.listdir(BASE):
        if d.startswith(month):
            p = os.path.join(BASE, d, "safety_summary.json")
            if os.path.isfile(p):
                with open(p) as f:
                    data = json.load(f)
                    for k, v in data["risk_breakdown"].items():
                        agg[k] += v
                    total += data["total_items"]

    out = {
        "month": month,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_items": total,
        "risk_breakdown": dict(agg)
    }

    out_dir = os.path.join(BASE, "monthly")
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, f"monthly_{month}.json"), "w") as f:
        json.dump(out, f, indent=2)

if __name__ == "__main__":
    main()
