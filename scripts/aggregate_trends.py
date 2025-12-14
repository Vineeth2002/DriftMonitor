import pandas as pd
import glob
import os

# Collect all evaluated CSV files
files = sorted(glob.glob("data/evaluated/*.csv"))

if not files:
    print("[INFO] No evaluated files found. Skipping aggregation.")
    exit(0)

dfs = []

for f in files:
    try:
        df = pd.read_csv(f)
        if df.empty:
            print(f"[INFO] Skipping empty file: {f}")
            continue
        dfs.append(df)
    except pd.errors.EmptyDataError:
        print(f"[INFO] EmptyDataError, skipping: {f}")
        continue

if not dfs:
    print("[INFO] No valid evaluated data available yet. Skipping aggregation.")
    exit(0)

df = pd.concat(dfs, ignore_index=True)

# Ensure correct types
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(0)

def aggregate(freq, out_dir, out_file):
    out = (
        df.groupby([pd.Grouper(key="date", freq=freq), "category"])
          .risk_score.sum()
          .reset_index()
          .sort_values("date")
    )

    if out.empty:
        print(f"[INFO] No data for {freq} aggregation.")
        return

    os.makedirs(out_dir, exist_ok=True)
    out.to_csv(os.path.join(out_dir, out_file), index=False)
    print(f"[OK] Saved {out_file}")

# Weekly / Monthly / Quarterly
aggregate("W", "data/history/weekly", "weekly_trends.csv")
aggregate("M", "data/history/monthly", "monthly_trends.csv")
aggregate("Q", "data/history/quarterly", "quarterly_trends.csv")

print("[SUCCESS] Aggregation step completed safely")
