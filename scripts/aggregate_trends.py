import pandas as pd
import glob
import os

# Load evaluated files
files = glob.glob("data/evaluated/*.csv")
if not files:
    print("No evaluated data found.")
    exit(0)

df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
df["date"] = pd.to_datetime(df["date"])

# Assume each row ≈ one text unit
df["total_words"] = 1
df["risk_words"] = df["risk_score"]

def add_severity(df):
    df["risk_percentage"] = (df["risk_words"] / df["total_words"]) * 100

    def severity(p):
        if p < 1:
            return "LOW"
        elif p <= 5:
            return "MEDIUM"
        else:
            return "HIGH"

    df["severity"] = df["risk_percentage"].apply(severity)
    return df

def aggregate(freq, out_dir, filename):
    agg = (
        df.groupby([pd.Grouper(key="date", freq=freq), "category"])
        .agg(
            total_words=("total_words", "sum"),
            risk_words=("risk_words", "sum")
        )
        .reset_index()
    )

    agg = add_severity(agg)
    os.makedirs(out_dir, exist_ok=True)
    agg.to_csv(f"{out_dir}/{filename}", index=False)

# DAILY
aggregate("D", "data/history/daily", "daily_summary.csv")

# WEEKLY
aggregate("W", "data/history/weekly", "weekly_summary.csv")

# MONTHLY
aggregate("M", "data/history/monthly", "monthly_summary.csv")

# QUARTERLY
aggregate("Q", "data/history/quarterly", "quarterly_summary.csv")

print("Aggregation completed successfully")
