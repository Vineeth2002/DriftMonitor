from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime
import os

pytrends = TrendReq(hl="en-US", tz=330)

KEYWORDS = [
    "AI safety",
    "AI regulation",
    "AI bias",
    "AI misuse",
    "artificial intelligence risk"
]

pytrends.build_payload(KEYWORDS, timeframe="now 1-d")
df = pytrends.interest_over_time()

if df.empty:
    raise RuntimeError("No Google Trends data returned")

df.reset_index(inplace=True)

today = datetime.utcnow().strftime("%Y-%m-%d")
os.makedirs("data/raw", exist_ok=True)
df.to_csv(f"data/raw/google_trends_{today}.csv", index=False)

print("Google Trends collected:", today)
