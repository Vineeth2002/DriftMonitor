import pandas as pd
import glob
import os

files = glob.glob("data/evaluated/*.csv")
df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(["category", "date"])

df["prev_risk"] = df.groupby("category")["risk_percentage"].shift(1)

def trend(row):
    if pd.isna(row["prev_risk"]):
        return "NEW"
    if row["risk_percentage"] > row["prev_risk"]:
        return "UP"
    if row["risk_percentage"] < row["prev_risk"]:
        return "DOWN"
    return "STABLE"

df["trend"] = df.apply(trend, axis=1)
df.drop(columns=["prev_risk"], inplace=True)

os.makedirs("data/history/daily", exist_ok=True)
df.to_csv("data/history/daily/daily_trends.csv", index=False)

print("Daily aggregation complete")
