import pandas as pd
from pathlib import Path
from datetime import datetime

BASE = Path("data/history")
DOCS = Path("docs")
DOCS.mkdir(exist_ok=True)

FILES = {
    "Daily AI Risk Summary": BASE / "daily" / "daily_trends.csv",
    "Weekly AI Risk Summary": BASE / "weekly" / "weekly_trends.csv",
    "Monthly AI Risk Summary": BASE / "monthly" / "monthly_trends.csv",
    "Quarterly AI Risk Summary": BASE / "quarterly" / "quarterly_trends.csv",
}

def render(df):
    if df.empty:
        return "<p>No data available yet.</p>"
    return df.to_html(index=False, classes="risk-table", border=0)

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AI Drift Monitor</title>
<style>
body {{ font-family: Arial; background:#f4f6f8; padding:25px; }}
.layout {{ display:grid; grid-template-columns:3.5fr 1.2fr; gap:25px; }}
.section {{ background:#fff; padding:18px; border-radius:8px; margin-bottom:25px; }}
.risk-table {{ width:100%; border-collapse:collapse; }}
.risk-table th {{ background:#343a40; color:white; padding:10px; }}
.risk-table td {{ padding:8px; border-bottom:1px solid #ddd; }}
.guide {{ background:#fff; padding:18px; border-radius:8px; height:fit-content; }}
</style>
</head>
<body>

<h1>AI Drift Monitor</h1>
<b>Status:</b> Automated monitoring active

<div class="layout">
<div>
"""

for title, path in FILES.items():
    df = pd.read_csv(path) if path.exists() else pd.DataFrame()
    html += f"<div class='section'><h2>{title}</h2>{render(df)}</div>"

html += f"""
</div>
<div class="guide">
<h2>Severity Guide</h2>
<p>🟢 <b>LOW</b><br>&lt;1% risk</p>
<p>🟡 <b>MEDIUM</b><br>1–5% risk</p>
<p>🔴 <b>HIGH</b><br>&gt;5% risk</p>
<hr>
<p><b>Trend</b><br>🔺 Increase<br>🔻 Decrease<br>➖ Stable / New</p>
</div>
</div>

<p>Last updated (UTC): {datetime.utcnow()}</p>
</body>
</html>
"""

(DOCS / "index.html").write_text(html, encoding="utf-8")
