import pandas as pd
import glob
import os

files = glob.glob("data/evaluated/*.csv")
df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

df["date"] = pd.to_datetime(df["date"])

daily = (
    df.groupby(["date", "category"])
      .agg({
          "total_words": "sum",
          "risk_words": "sum",
          "risk_percentage": "mean"
      })
      .reset_index()
)

def severity(p):
    if p < 1:
        return "🟢 LOW"
    elif p <= 5:
        return "🟡 MEDIUM"
    return "🔴 HIGH"

daily["severity"] = daily["risk_percentage"].apply(severity)
daily["trend"] = "NEW"

os.makedirs("data/history/daily", exist_ok=True)
daily.to_csv("data/history/daily/daily_trends.csv", index=False)
