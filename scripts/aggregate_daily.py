import pandas as pd
import glob
import os

# Read evaluated files
files = glob.glob("data/evaluated/*.csv")
if not files:
    print("No evaluated files found")
    exit(0)

df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

# Ensure date is datetime
df["date"] = pd.to_datetime(df["date"]).dt.date

# Calculate total words per source per day
df["total_words"] = df["source"].map(
    df.groupby("source")["risk_score"].transform("count")
)

# Aggregate daily
daily = (
    df.groupby(["date", "category"])
    .agg(
        total_words=("total_words", "sum"),
        risk_words=("risk_score", "sum")
    )
    .reset_index()
)

# Risk percentage
daily["risk_percentage"] = (
    daily["risk_words"] / daily["total_words"] * 100
).round(2)

# Severity logic
def severity(p):
    if p < 1:
        return "🟢 LOW"
    elif p <= 5:
        return "🟡 MEDIUM"
    else:
        return "🔴 HIGH"

daily["severity"] = daily["risk_percentage"].apply(severity)

# Save
os.makedirs("data/history/daily", exist_ok=True)
daily.to_csv("data/history/daily/daily_trends.csv", index=False)

print("Daily aggregation complete")
