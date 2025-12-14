import pandas as pd
from pathlib import Path
from datetime import datetime

DOCS = Path("docs")
DOCS.mkdir(exist_ok=True)

def load_csv(path):
    return pd.read_csv(path) if path.exists() else pd.DataFrame()

def severity_label(p):
    if p < 1:
        return "🟢 LOW"
    elif p <= 5:
        return "🟡 MEDIUM"
    else:
        return "🔴 HIGH"

def render_table(df):
    if df.empty:
        return "<p><em>No data available.</em></p>"

    df["severity"] = df["risk_percentage"].apply(severity_label)
    return df.to_html(index=False, classes="risk-table")

# ---- LOAD DATA ----
daily = load_csv(Path("data/history/daily/daily_summary.csv"))
weekly = load_csv(Path("data/history/weekly/weekly_summary.csv"))
monthly = load_csv(Path("data/history/monthly/monthly_summary.csv"))
quarterly = load_csv(Path("data/history/quarterly/quarterly_summary.csv"))

# ---- HTML ----
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AI Drift Monitor</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background: #f6f7f9;
    padding: 30px;
}}
h1 {{ margin-bottom: 5px; }}
.status {{ font-weight: bold; margin-bottom: 25px; }}

.layout {{
    display: grid;
    grid-template-columns: 3fr 1fr;
    gap: 25px;
}}

.section {{
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 25px;
}}

.risk-table {{
    width: 100%;
    border-collapse: collapse;
}}
.risk-table th {{
    background: #343a40;
    color: #fff;
    padding: 10px;
}}
.risk-table td {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
}}

.severity {{
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    height: fit-content;
}}

.footer {{
    margin-top: 40px;
    color: #555;
    font-size: 0.9em;
}}
</style>
</head>

<body>
<h1>AI Drift Monitor</h1>
<div class="status">Status: Automated monitoring active</div>

<div class="layout">

<div>
<div class="section">
<h2>Daily AI Risk Summary</h2>
{render_table(daily)}
</div>

<div class="section">
<h2>Weekly AI Risk Summary</h2>
{render_table(weekly)}
</div>

<div class="section">
<h2>Monthly AI Risk Summary</h2>
{render_table(monthly)}
</div>

<div class="section">
<h2>Quarterly AI Risk Summary</h2>
{render_table(quarterly)}
</div>
</div>

<div class="severity">
<h3>Severity Guide</h3>
<p>🟢 <b>LOW</b><br>&lt; 1% risk words<br>Minimal AI risk</p>
<p>🟡 <b>MEDIUM</b><br>1–5% risk words<br>Moderate AI risk</p>
<p>🔴 <b>HIGH</b><br>&gt; 5% risk words<br>Elevated AI risk</p>
</div>

</div>

<div class="footer">
Last updated (UTC): {datetime.utcnow().isoformat()}<br>
Sources: Google Trends, Hacker News<br>
Pipeline: GitHub Actions (Automated)
</div>

</body>
</html>
"""

(DOCS / "index.html").write_text(html, encoding="utf-8")
print("Dashboard built successfully")
