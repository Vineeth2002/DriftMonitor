from pytrends.request import TrendReq
from datetime import datetime
import json
import os

def run():
    pytrends = TrendReq(hl="en-US", tz=360)

    keywords = [
        "AI jailbreak",
        "LLM safety",
        "prompt injection",
        "AI misuse",
        "AI alignment"
    ]

    pytrends.build_payload(keywords, timeframe="now 1-d")
    df = pytrends.interest_over_time()

    today = datetime.utcnow().strftime("%Y-%m-%d")
    out_dir = f"data/live/raw/{today}"
    os.makedirs(out_dir, exist_ok=True)

    records = []
    for ts, row in df.iterrows():
        for k in keywords:
            records.append({
                "source": "google_trends",
                "keyword": k,
                "value": int(row[k]),
                "timestamp": ts.isoformat()
            })

    with open(f"{out_dir}/google_trends.json", "w") as f:
        json.dump(records, f, indent=2)

if __name__ == "__main__":
    run()
