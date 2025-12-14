import pandas as pd
import plotly.express as px
import os

df = pd.read_csv("data/history/weekly/weekly_trends.csv")

fig = px.line(
    df,
    x="date",
    y="risk_score",
    color="category",
    title="AI Safety Risk Trends (Weekly)"
)

os.makedirs("docs", exist_ok=True)
fig.write_html("docs/index.html")

print("[OK] Dashboard built → docs/index.html")
