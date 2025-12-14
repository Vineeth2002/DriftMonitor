import pandas as pd
import plotly.express as px
import os

OUTPUT_DIR = "docs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "index.html")
WEEKLY_FILE = "data/history/weekly/weekly_trends.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Case 1: No weekly data yet
# -----------------------------
if not os.path.exists(WEEKLY_FILE):
    html = """
    <html>
      <head>
        <title>Drift Monitor</title>
      </head>
      <body>
        <h1>Drift Monitor</h1>
        <p><b>Status:</b> No trend data available yet.</p>
        <p>The system is running correctly. Data will appear as signals accumulate.</p>
      </body>
    </html>
    """
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)

    print("[INFO] No weekly data found. Placeholder dashboard generated.")
    exit(0)

# -----------------------------
# Case 2: Weekly data exists
# -----------------------------
df = pd.read_csv(WEEKLY_FILE)

if df.empty:
    html = """
    <html>
      <head>
        <title>Drift Monitor</title>
      </head>
      <body>
        <h1>Drift Monitor</h1>
        <p><b>Status:</b> Weekly data file exists but contains no records.</p>
      </body>
    </html>
    """
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)

    print("[INFO] Weekly file empty. Placeholder dashboard generated.")
    exit(0)

# -----------------------------
# Case 3: Normal dashboard
# -----------------------------
fig = px.line(
    df,
    x="date",
    y="risk_score",
    color="category",
    title="AI Safety Risk Trends (Weekly)"
)

fig.write_html(OUTPUT_FILE)
print("[SUCCESS] Dashboard generated with data.")
