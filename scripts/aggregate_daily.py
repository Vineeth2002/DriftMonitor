import pandas as pd
import glob
import os

INPUT_FILES = "data/evaluated/*.csv"
OUTPUT_DIR = "data/history/daily"

os.makedirs(OUTPUT_DIR, exist_ok=True)

files = sorted(glob.glob(INPUT_FILES))

if not files:
    print("No evaluated files found.")
    exit(0)

df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
df["date"] = pd.to_datetime(df["date"])

# ----------------------------
# Aggregate daily
# ----------------------------
daily = (
    df.groupby(["date", "category"])
      .agg(
          total_words=("total_words", "sum"),
          risk_words=("risk_words", "sum")
      )
      .reset_index()
)

daily["risk_percentage"] = (
    daily["risk_words"] / daily["total_words"] * 100
).round(2)

# ----------------------------
# Compute trend deltas
# ----------------------------
daily = daily.sort_values(["category", "date"])
daily["delta"] = daily.groupby("category")["risk_percentage"].diff().round(2)

def trend_symbol(x):
    if pd.isna(x) or x == 0:
        return "➖ 0.0%"
    elif x > 0:
        return f"🔺 +{x}%"
    else:
        return f"🔻 {x}%"

daily["trend"] = daily["delta"].apply(trend_symbol)

# ----------------------------
# Severity
# ----------------------------
def severity(p):
    if p < 1:
        return "🟢 LOW"
    elif p <= 5:
        return "🟡 MEDIUM"
    else:
        return "🔴 HIGH"

daily["severity"] = daily["risk_percentage"].apply(severity)

# ----------------------------
# Save
# ----------------------------
output_file = f"{OUTPUT_DIR}/daily_trends.csv"
daily.to_csv(output_file, index=False)

print("Daily trends with deltas saved:", output_file)
