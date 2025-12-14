import pandas as pd
import glob
import os

files = glob.glob("data/evaluated/evaluated_*.csv")

if not files:
    print("No evaluated files found")
    exit(0)

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Convert date
df["date"] = pd.to_datetime(df["date"])

daily = (
    df.groupby(df["date"].dt.date)
      .risk_score.sum()
      .reset_index()
)

daily.columns = ["date", "risk_score"]

os.makedirs("data/history/daily", exist_ok=True)
daily.to_csv("data/history/daily/daily_trends.csv", index=False)

print("Daily aggregation completed")
