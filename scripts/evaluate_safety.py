import pandas as pd
import glob
import os
from datetime import datetime

RISK_KEYWORDS = {
    "misinformation": ["fake", "hallucination", "misinformation"],
    "bias": ["bias", "fairness", "discrimination"],
    "misuse": ["misuse", "weapon", "abuse"],
    "governance": ["regulation", "law", "policy"]
}

files = glob.glob("data/raw/*.csv")
records = []

for f in files:
    df = pd.read_csv(f)
    for _, row in df.iterrows():
        text = " ".join(map(str, row.values)).lower()
        for cat, keys in RISK_KEYWORDS.items():
            score = sum(k in text for k in keys)
            if score > 0:
                records.append({
                    "date": datetime.utcnow().date(),
                    "category": cat,
                    "risk_score": score,
                    "source": os.path.basename(f)
                })

out = pd.DataFrame(records)
today = datetime.utcnow().strftime("%Y-%m-%d")

os.makedirs("data/evaluated", exist_ok=True)
out.to_csv(f"data/evaluated/evaluated_{today}.csv", index=False)

print("Safety evaluation done:", today)
