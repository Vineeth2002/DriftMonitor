import pandas as pd
import plotly.express as px
import os

OUTPUT_DIR = "docs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "index.html")
WEEKLY_FILE = "data/history/weekly/weekly_trends.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# If weekly data does not exist yet
if not os.path.exists(WEEKLY_FILE):
    html = """
    <html>
      <head><title>Drift Monitor</title></head>
      <body>
        <h1>Drift Monitor</h1>
        <p><b>Status:</b> No trend data available yet.</p>
        <p>Automation is running correctly. Data will appear over time.</p>
      </body>
    </html>
    """
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)
    exit(0)

df = pd.read_csv(WEEKLY_FILE)

# If file exists but has no rows
if df.empty:
    html = """
    <html>
      <head><title>Drift Monitor</title></head>
      <body>
        <h1>Drift Monitor</h1>
        <p><b>Status:</b> Weekly trend file exists but contains no data yet.</p>
      </body>
    </html>
    """
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)
    exit(0)

# Normal dashboard
fig = px.line(
    df,
    x="date",
    y="risk_score",
    color="category",
    title="AI Safety Risk Trends (Weekly)"
)

fig.write_html(OUTPUT_FILE)
