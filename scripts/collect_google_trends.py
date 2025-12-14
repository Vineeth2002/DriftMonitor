from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime
import os

os.makedirs("data/raw", exist_ok=True)

try:
    pytrends = TrendReq(hl="en-US", tz=360)
    kw_list = ["AI safety", "AI regulation", "AI bias", "AI misuse"]

    pytrends.build_payload(kw_list, timeframe="now 1-d")
    df = pytrends.interest_over_time()

    if not df.empty:
        df.reset_index(inplace=True)
        today = datetime.utcnow().strftime("%Y-%m-%d")
        df.to_csv(f"data/raw/google_trends_{today}.csv", index=False)

        print("Google Trends collected")

except Exception as e:
    print("Google Trends skipped:", e)
