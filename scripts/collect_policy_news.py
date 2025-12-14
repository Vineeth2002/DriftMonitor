import feedparser
import pandas as pd
import os
from datetime import datetime

FEEDS = [
    "https://www.reuters.com/rssFeed/technologyNews",
    "https://www.theguardian.com/technology/artificialintelligence/rss",
    "https://economictimes.indiatimes.com/tech/artificial-intelligence/rssfeeds/78570527.cms"
]

records = []

for url in FEEDS:
    feed = feedparser.parse(url)

    for entry in feed.entries[:20]:
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        text = f"{title} {summary}"

        records.append({
            "date": datetime.utcnow().date(),
            "text": text,
            "source": "policy_news"
        })

if not records:
    records.append({
        "date": datetime.utcnow().date(),
        "text": "No policy news available today",
        "source": "policy_news"
    })

df = pd.DataFrame(records)

os.makedirs("data/raw", exist_ok=True)
today = datetime.utcnow().strftime("%Y-%m-%d")
df.to_csv(f"data/raw/policy_news_{today}.csv", index=False)

print("Policy news collection complete")
