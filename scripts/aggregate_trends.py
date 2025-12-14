import pandas as pd
import glob
import os

df = pd.concat(
    (pd.read_csv(f) for f in glob.glob("data/evaluated/*.csv")),
    ignore_index=True
)

df["date"] = pd.to_datetime(df["date"])

def save(freq, folder):
    out = df.groupby(
        [pd.Grouper(key="date", freq=freq), "category"]
    ).risk_score.sum().reset_index()
    os.makedirs(folder, exist_ok=True)
    out.to_csv(f"{folder}/{freq}_trends.csv", index=False)

save("W", "data/history/weekly")
save("M", "data/history/monthly")
save("Q", "data/history/quarterly")

print("Weekly, Monthly, Quarterly trends saved")
