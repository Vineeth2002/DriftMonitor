import pandas as pd
import glob
from datetime import datetime
import os

DASHBOARD_PATH = "docs/index.html"

def load_latest(path_pattern):
    files = sorted(glob.glob(path_pattern))
    if not files:
        return None
    return pd.read_csv(files[-1])

def add_severity(df):
    def severity(row):
        if row["risk_percentage"] < 1:
            return "🟢 LOW"
        elif row["risk_percentage"] < 5:
            return "🟡 MEDIUM"
        else:
            return "🔴 HIGH"

    df["severity"] = df.apply(severity, axis=1)
    return df

def table_html(df):
    return df.to_html(index=False, classes="risk-table", border=0)

daily = load_latest("data/history/daily/*.csv")
weekly = load_latest("data/history/weekly/*.csv")
monthly = load_latest("data/history/monthly/*.csv")
quarterly = load_latest("data/history/quarterly/*.csv")

sections = []

for title, data in [
    ("Daily AI Risk Summary", daily),
    ("Weekly AI Risk Summary", weekly),
    ("Monthly AI Risk Summary", monthly),
    ("Quarterly AI Risk Summary", quarterly),
]:
    if data is not None and not data.empty:
        data = add_severity(data)
        sections.append(f"<h2>{title}</h2>{table_html(data)}")
    else:
        sections.append(f"<h2>{title}</h2><p>No data available yet.</p>")

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AI Drift Monitor</title>
<style>
body {{
  font-family: Arial, sans-serif;
  margin: 40px;
  background: #ffffff;
  color: #222;
}}

h1 {{ margin-bottom: 5px; }}
h2 {{ margin-top: 40px; }}

.status {{
  font-weight: bold;
  margin-bottom: 20px;
}}

.legend {{
  position: fixed;
  right: 30px;
  top: 100px;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #ddd;
  width: 260px;
}}

.legend h3 {{
  margin-top: 0;
}}

.risk-table {{
  border-collapse: collapse;
  width: 100%;
  margin-top: 10px;
}}

.risk-table th {{
  background: #343a40;
  color: white;
  padding: 10px;
}}

.risk-table td {{
  padding: 8px;
  border-bottom: 1px solid #ddd;
}}

footer {{
  margin-top: 50px;
  font-size: 0.9em;
  color: #555;
}}
</style>
</head>

<body>

<h1>AI Drift Monitor</h1>
<div class="status">Status: Automated monitoring active</div>

<div class="legend">
  <h3>Severity Guide</h3>
  <p>🟢 <b>LOW</b><br>&lt; 1% risk words<br>Minimal AI risk</p>
  <p>🟡 <b>MEDIUM</b><br>1–5% risk words<br>Moderate AI risk</p>
  <p>🔴 <b>HIGH</b><br>&gt; 5% risk words<br>Elevated AI risk</p>
</div>

{''.join(sections)}

<footer>
<p>Last updated (UTC): {datetime.utcnow().isoformat()}</p>
<p>Sources: Google Trends, Hacker News</p>
<p>Pipeline: GitHub Actions (Fully Automated)</p>
</footer>

</body>
</html>
"""

os.makedirs("docs", exist_ok=True)
with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard built successfully")
