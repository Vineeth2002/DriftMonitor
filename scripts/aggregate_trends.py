import pandas as pd
import glob
import os

# -------------------------------
# Load all evaluated daily files
# -------------------------------
evaluated_files = sorted(glob.glob("data/evaluated/*.csv"))

if not evaluated_files:
    raise RuntimeError("No evaluated files found in data/evaluated/")

df = pd.concat(
    (pd.read_csv(f) for f in evaluated_files),
    ignore_index=True
)

# -------------------------------
# Date handling (CRITICAL)
# -------------------------------
df["date"] = pd.to_datetime(df["date"])

# Ensure numeric safety
df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(0)

# -------------------------------
# Aggregation function
# -------------------------------
def aggregate_and_save(freq, out_dir, out_file):
    aggregated = (
        df.groupby([pd.Grouper(key="date", freq=freq), "category"])
          .risk_score
          .sum()
          .reset_index()
          .sort_values("date")
    )

    os.makedirs(out_dir, exist_ok=True)
    aggregated.to_csv(os.path.join(out_dir, out_file), index=False)

    print(f"[OK] {freq} trends saved → {out_dir}/{out_file}")

# -------------------------------
# Weekly, Monthly, Quarterly
# -------------------------------
aggregate_and_save(
    freq="W",
    out_dir="data/history/weekly",
    out_file="weekly_trends.csv"
)

aggregate_and_save(
    freq="M",
    out_dir="data/history/monthly",
    out_file="monthly_trends.csv"
)

aggregate_and_save(
    freq="Q",
    out_dir="data/history/quarterly",
    out_file="quarterly_trends.csv"
)

print("[SUCCESS] All aggregations completed")
