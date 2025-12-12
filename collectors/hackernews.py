import requests
import json
import os
from datetime import datetime

HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"

def collect_hackernews(limit=50):
    ids = requests.get(HN_TOP).json()[:limit]
    stories = []

    for i in ids:
        item = requests.get(HN_ITEM.format(i)).json()
        if item and "title" in item:
            stories.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "text": item.get("text", ""),
                "url": item.get("url", ""),
                "score": item.get("score", 0)
            })
    return stories


def save_hackernews():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    out_dir = f"data/live/raw/{today}"
    os.makedirs(out_dir, exist_ok=True)

    data = collect_hackernews()

    output = {
        "source": "hackernews",
        "date": today,
        "items": data
    }

    path = f"{out_dir}/hackernews.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return path
