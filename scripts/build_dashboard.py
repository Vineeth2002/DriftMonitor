import pandas as pd
from pathlib import Path
from datetime import datetime

# ---------- Paths ----------
BASE = Path("data/history")
DOCS = Path("docs")
DOCS.mkdir(exist_ok=True)

FILES = {
    "Daily AI Risk Summary": BASE / "daily" / "daily_trends.csv",
    "Weekly AI Risk Summary": BASE / "weekly" / "weekly_trends.csv",
    "Monthly AI Risk Summary": BASE / "monthly" / "monthly_trends.csv",
    "Quarterly AI Risk Summary": BASE / "quarterly" / "quarterly_trends.csv",
}

# ---------- Required table schema ----------
REQUIRED_COLUMNS = [
    "date",
    "category",
    "total_words",
    "risk_words",
    "risk_percentage",
    "severity",
    "trend",
]

# ---------- Helpers ----------
def load_df(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

def render_table(df: pd.DataFrame) -> str:
    if df.empty:
        return """
        <table class="risk-table">
            <tr>
                <td colspan="7" style="text-align:center;color:#777;">
                    No data available yet
                </td>
            </tr>
        </table>
        """

    # Ensure all required columns exist
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    # Enforce column order
    df = df[REQUIRED_COLUMNS]

    # Format percentage nicely
    if "risk_percentage" in df.columns:
        df["risk_percentage"] = df["risk_percentage"].apply(
            lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x
        )

    return df.to_html(
        index=False,
        classes="risk-table",
        border=0,
        justify="left"
    )

# ---------- HTML ----------
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AI Drift Monitor</title>

<style>
body {{
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    margin: 0;
    padding: 25px;
}}

h1 {{
    margin-bottom: 5px;
}}

.status {{
    font-weight: bold;
    margin-bottom: 20px;
}}

.layout {{
    display: grid;
    grid-template-columns: 3.5fr 1.2fr;
    gap: 25px;
}}

.section {{
    background: #ffffff;
    padding: 18px;
    border-radius: 8px;
    margin-bottom: 25px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}}

.risk-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}}

.risk-table th {{
    background: #343a40;
    color: #ffffff;
    padding: 10px;
    font-size: 14px;
    text-align: left;
}}

.risk-table td {{
    padding: 9px;
    border-bottom: 1px solid #ddd;
    font-size: 13px;
}}

.guide {{
    background: #ffffff;
    padding: 18px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    position: sticky;
    top: 20px;
}}

.footer {{
    margin-top: 35px;
    font-size: 13px;
    color: #555;
}}
</style>
</head>

<body>

<h1>AI Drift Monitor</h1>
<div class="status">Status: Automated monitoring active</div>

<div class="layout">

<div>
"""

# ---------- Tables ----------
for title, path in FILES.items():
    df = load_df(path)
    html += f"""
    <div class="section">
        <h2>{title}</h2>
        {render_table(df)}
    </div>
    """

# ---------- Severity Guide ----------
html += """
</div>

<div class="guide">
    <h2>Severity Guide</h2>

    <p>🟢 <b>LOW</b><br>
       Risk &lt; 1%<br>
       Minimal AI risk signals</p>

    <p>🟡 <b>MEDIUM</b><br>
       Risk 1–5%<br>
       Moderate AI risk signals</p>

    <p>🔴 <b>HIGH</b><br>
       Risk &gt; 5%<br>
       Elevated AI risk signals</p>

    <hr>

    <p><b>Trend</b><br>
       🔺 UP – Risk increasing<br>
       🔻 DOWN – Risk decreasing<br>
       ➖ STABLE / NEW</p>
</div>

</div>

<div class="footer">
Last updated (UTC): {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}<br>
Sources: Google Trends, Hacker News, Policy & Regulation News<br>
Pipeline: GitHub Actions (Automated)
</div>

</body>
</html>
"""

(DOCS / "index.html").write_text(html, encoding="utf-8")
print("Dashboard built successfully")
