import json
import os
from datetime import datetime

BASE = "data/live/processed"
OUT = "docs"

def load_json(path):
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None

def main():
    os.makedirs(OUT, exist_ok=True)

    today = datetime.utcnow().strftime("%Y-%m-%d")

    daily = load_json(f"{BASE}/{today}/safety_summary.json")
    weekly_files = sorted(os.listdir(f"{BASE}/weekly")) if os.path.isdir(f"{BASE}/weekly") else []
    monthly_files = sorted(os.listdir(f"{BASE}/monthly")) if os.path.isdir(f"{BASE}/monthly") else []

    weekly = load_json(f"{BASE}/weekly/{weekly_files[-1]}") if weekly_files else None
    monthly = load_json(f"{BASE}/monthly/{monthly_files[-1]}") if monthly_files else None

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <title>DriftMonitor – AI Safety Dashboard</title>
  <style>
    body {{ font-family: Arial; margin: 40px; }}
    h1 {{ color: #222; }}
    .card {{ border: 1px solid #ccc; padding: 20px; margin-bottom: 20px; }}
    .safe {{ color: green; }}
    .warn {{ color: orange; }}
    .risk {{ color: red; }}
  </style>
</head>
<body>

<h1>DriftMonitor – AI Safety Dashboard</h1>
<p>Last updated: {datetime.utcnow().isoformat()} UTC</p>

<div class="card">
<h2>Daily Summary ({today})</h2>
<pre>{json.dumps(daily, indent=2) if daily else "No daily data yet"}</pre>
</div>

<div class="card">
<h2>Weekly Summary</h2>
<pre>{json.dumps(weekly, indent=2) if weekly else "No weekly data yet"}</pre>
</div>

<div class="card">
<h2>Monthly Summary</h2>
<pre>{json.dumps(monthly, indent=2) if monthly else "No monthly data yet"}</pre>
</div>

</body>
</html>
"""

    with open(f"{OUT}/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Dashboard generated at docs/index.html")

if __name__ == "__main__":
    main()
