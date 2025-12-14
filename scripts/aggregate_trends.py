import pandas as pd
import glob
import os

# Load all evaluated CSVs
files = sorted(glob.glob("data/evaluated/*.csv"))
if not files:
    raise RuntimeError("No evaluated files found")

df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

# Ensure proper types
df["date"] = pd.to_datetime(df["date"])
df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(0)

def aggregate(freq, out_dir, out_file):
    out = (
        df.groupby([pd.Grouper(key="date", freq=freq), "category"])
          .risk_score.sum()
          .reset_index()
          .sort_values("date")
    )
    os.makedirs(out_dir, exist_ok=True)
    out.to_csv(os.path.join(out_dir, out_file), index=False)
    print(f"[OK] Saved {out_file}")

# Weekly / Monthly / Quarterly
aggregate("W", "data/history/weekly", "weekly_trends.csv")
aggregate("M", "data/history/monthly", "monthly_trends.csv")
aggregate("Q", "data/history/quarterly", "quarterly_trends.csv")

print("[SUCCESS] Aggregation complete")
