import pandas as pd
import glob
import os

files = glob.glob("data/evaluated/*.csv")

# -------------------------
# No evaluated files
# -------------------------
if not files:
    print("No evaluated files found. Skipping aggregation.")
    exit(0)

frames = []

for f in files:
    df = pd.read_csv(f)

    # Skip empty CSVs
    if df.empty:
        continue

    frames.append(df)

# -------------------------
# All files empty
# -------------------------
if not frames:
    print("Evaluated files exist but contain no data.")
    exit(0)

df = pd.concat(frames, ignore_index=True)

# Ensure datetime
df["date"] = pd.to_datetime(df["date"])

# -------------------------
# Create output folders
# -------------------------
os.makedirs("data/history/weekly", exist_ok=True)
os.makedirs("data/history/monthly", exist_ok=True)
os.makedirs("data/history/quarterly", exist_ok=True)

# -------------------------
# Weekly aggregation
# -------------------------
weekly = (
    df.groupby([pd.Grouper(key="date", freq="W"), "category"])
      .risk_score.sum()
      .reset_index()
)

weekly.to_csv(
    "data/history/weekly/weekly_trends.csv",
    index=False
)

# -------------------------
# Monthly aggregation
# -------------------------
monthly = (
    df.groupby([pd.Grouper(key="date", freq="M"), "category"])
      .risk_score.sum()
      .reset_index()
)

monthly.to_csv(
    "data/history/monthly/monthly_trends.csv",
    index=False
)

# -------------------------
# Quarterly aggregation
# -------------------------
quarterly = (
    df.groupby([pd.Grouper(key="date", freq="Q"), "category"])
      .risk_score.sum()
      .reset_index()
)

quarterly.to_csv(
    "data/history/quarterly/quarterly_trends.csv",
    index=False
)

print("Weekly, monthly, and quarterly aggregation completed successfully")
