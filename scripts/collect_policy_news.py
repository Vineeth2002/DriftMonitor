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
    print("No policy news collected.")
    exit(0)

df = pd.DataFrame(records)

os.makedirs("data/raw", exist_ok=True)
today = datetime.utcnow().strftime("%Y-%m-%d")

out_file = f"data/raw/policy_news_{today}.csv"
df.to_csv(out_file, index=False)

print(f"Policy news collected: {out_file}")
