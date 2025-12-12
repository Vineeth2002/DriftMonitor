# driftmonitor/report/html/report_builder.py
import os
import json
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROCESSED = os.path.join(ROOT, "data", "live", "processed") if False else os.path.abspath("data/live/processed")
OUTDIR = os.path.abspath("report/html")
os.makedirs(OUTDIR, exist_ok=True)

TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>DriftMonitor Report</title>
  <style>body{font-family:Arial,Helvetica,sans-serif;padding:20px} .card{border:1px solid #ddd;padding:12px;margin:12px 0}</style>
</head>
<body>
  <h1>DriftMonitor Report</h1>
  <p>Generated at: {{ ts }}</p>
  <h2>Summary</h2>
  <pre>{{ summary | tojson(indent=2) }}</pre>
  {% if risky %}
  <h2>Top Risky Examples</h2>
  <ul>
    {% for r in risky %}
    <li class="card"><strong>score:</strong> {{ r.safety_score }} - {{ r.text }}</li>
    {% endfor %}
  </ul>
  {% endif %}
</body>
</html>
"""

def find_latest_summary():
    files = sorted([f for f in os.listdir("data/live/processed") if f.startswith("eval_summary_")], reverse=True)
    if not files:
        return None
    return os.path.join("data/live/processed", files[0])

def build_report():
    path = find_latest_summary()
    summary = {}
    risky = []
    ts = ""
    if path and os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            summary = json.load(f)
        ts = summary.get("evaluated_at", "")
        risky = summary.get("risky_examples", [])
    html = TEMPLATE.replace("{{ ts }}", ts)
    # use naive render
    from json import dumps
    html = TEMPLATE
    html = html.replace("{{ ts }}", ts)
    html = html.replace("{{ summary | tojson(indent=2) }}", dumps(summary, indent=2))
    # risky insertion
    risky_html = ""
    for r in risky:
        risky_html += f"<li class='card'><strong>score:</strong> {r.get('safety_score')} - {r.get('text')[:300]}</li>\n"
    html = html.replace("{% if risky %}\n  <h2>Top Risky Examples</h2>\n  <ul>\n    {% for r in risky %}\n    <li class=\"card\"><strong>score:</strong> {{ r.safety_score }} - {{ r.text }}</li>\n    {% endfor %}\n  </ul>\n  {% endif %}", risky_html)
    outfile = os.path.join(OUTDIR, "report.html")
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(html)
    print("Report built ->", outfile)
    return outfile

if __name__ == "__main__":
    build_report()
