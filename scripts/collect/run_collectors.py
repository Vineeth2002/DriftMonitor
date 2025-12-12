import json
import os
import requests
from datetime import datetime
from pytrends.request import TrendReq

BASE_DIR = "data/live/raw"
TODAY = datetime.utcnow().strftime("%Y-%m-%d")
OUT_DIR = os.path.join(BASE_DIR, TODAY)
os.makedirs(OUT_DIR, exist_ok=True)

def collect_google_trends():
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.trending_searches(pn="india")
    trends = pytrends.trending_searches(pn="india").head(10)[0].tolist()

    data = [{
        "source": "google_trends",
        "title": t,
        "collected_at": datetime.utcnow().isoformat()
    } for t in trends]

    with open(f"{OUT_DIR}/google_trends.json", "w") as f:
        json.dump(data, f, indent=2)

def collect_hackernews():
    top_ids = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json"
    ).json()[:10]

    items = []
    for i in top_ids:
        item = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{i}.json"
        ).json()
        if item and "title" in item:
            items.append({
                "source": "hackernews",
                "title": item["title"],
                "collected_at": datetime.utcnow().isoformat(),
                "url": item.get("url")
            })

    with open(f"{OUT_DIR}/hackernews.json", "w") as f:
        json.dump(items, f, indent=2)

if __name__ == "__main__":
    collect_google_trends()
    collect_hackernews()
    print(f"Collected data for {TODAY}")
