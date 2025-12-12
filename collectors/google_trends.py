from pytrends.request import TrendReq
from datetime import datetime
import json
import os

def collect_google_trends(keywords):
    pytrends = TrendReq(hl="en-US", tz=330)
    pytrends.build_payload(keywords, timeframe="now 1-d")

    related = pytrends.related_queries()
    results = []

    for kw, data in related.items():
        if data and data.get("top") is not None:
            for _, row in data["top"].iterrows():
                results.append({
                    "keyword": kw,
                    "query": row["query"],
                    "value": int(row["value"])
                })

    return results


def save_google_trends():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    out_dir = f"data/live/raw/{today}"
    os.makedirs(out_dir, exist_ok=True)

    keywords = ["AI safety", "LLM security", "AI jailbreak"]
    data = collect_google_trends(keywords)

    output = {
        "source": "google_trends",
        "date": today,
        "items": data
    }

    path = f"{out_dir}/google_trends.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return path
