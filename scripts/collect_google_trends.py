from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime
import os

# Setup
pytrends = TrendReq(hl="en-US", tz=330)
keywords = [
    "AI safety",
    "AI regulation",
    "AI bias",
    "AI misuse",
    "Artificial intelligence risk"
]

pytrends.build_payload(
    kw_list=keywords,
    timeframe="now 1-d",
    geo=""
)

df = pytrends.interest_over_time()

if df.empty:
    raise RuntimeError("Google Trends returned no data")

df.reset_index(inplace=True)

today = datetime.utcnow().strftime("%Y-%m-%d")
os.makedirs("data/raw", exist_ok=True)
output_path = f"data/raw/google_trends_{today}.csv"

df.to_csv(output_path, index=False)
print(f"[OK] Google Trends saved → {output_path}")
