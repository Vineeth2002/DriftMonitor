import pandas as pd
import glob
import os

files = glob.glob("data/evaluated/*.csv")

if not files:
    print("No evaluated files found. Skipping aggregation.")
    exit(0)

dfs = []

for f in files:
    try:
        df = pd.read_csv(f)
        if not df.empty:
            dfs.append(df)
    except Exception:
        continue

if not dfs:
    print("No valid data to aggregate.")
    exit(0)

df = pd.concat(dfs, ignore_index=True)

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(0)

def aggregate(freq, out_dir, out_file):
    out = (
        df.groupby([pd.Grouper(key="date", freq=freq), "category"])
        .risk_score.sum()
        .reset_index()
    )
    if out.empty:
        return
    os.makedirs(out_dir, exist_ok=True)
    out.to_csv(os.path.join(out_dir, out_file), index=False)

aggregate("W", "data/history/weekly", "weekly_trends.csv")
aggregate("M", "data/history/monthly", "monthly_trends.csv")
aggregate("Q", "data/history/quarterly", "quarterly_trends.csv")
