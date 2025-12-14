import pandas as pd
import os

INPUT = "data/history/daily/daily_trends.csv"
BASE_DIR = "data/history"

df = pd.read_csv(INPUT)
df["date"] = pd.to_datetime(df["date"])

def aggregate(freq, folder):
    out_dir = f"{BASE_DIR}/{folder}"
    os.makedirs(out_dir, exist_ok=True)

    agg = (
        df.groupby([pd.Grouper(key="date", freq=freq), "category"])
          .agg(
              total_words=("total_words", "sum"),
              risk_words=("risk_words", "sum")
          )
          .reset_index()
    )

    agg["risk_percentage"] = (
        agg["risk_words"] / agg["total_words"] * 100
    ).round(2)

    agg = agg.sort_values(["category", "date"])
    agg["delta"] = agg.groupby("category")["risk_percentage"].diff().round(2)

    def trend_symbol(x):
        if pd.isna(x) or x == 0:
            return "➖ 0.0%"
        elif x > 0:
            return f"🔺 +{x}%"
        else:
            return f"🔻 {x}%"

    agg["trend"] = agg["delta"].apply(trend_symbol)

    def severity(p):
        if p < 1:
            return "🟢 LOW"
        elif p <= 5:
            return "🟡 MEDIUM"
        else:
            return "🔴 HIGH"

    agg["severity"] = agg["risk_percentage"].apply(severity)

    agg.to_csv(f"{out_dir}/{folder}_trends.csv", index=False)
    print(f"{folder.capitalize()} trends saved")

aggregate("W", "weekly")
aggregate("M", "monthly")
aggregate("Q", "quarterly")
