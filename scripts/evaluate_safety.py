import pandas as pd
import glob
import os
from datetime import datetime

RISK_KEYWORDS = {
    "misinformation": ["fake", "hallucination", "misinformation"],
    "bias": ["bias", "fairness", "discrimination"],
    "misuse": ["misuse", "weapon", "abuse"],
    "governance": ["regulation", "law", "policy"],
}

files = glob.glob("data/raw/*.csv")
records = []

today = datetime.utcnow().strftime("%Y-%m-%d")

for f in files:
    df = pd.read_csv(f)

    for _, row in df.iterrows():
        text = " ".join(map(str, row.values)).lower()

        total_score = 0
        matched_categories = []

        for cat, keys in RISK_KEYWORDS.items():
            score = sum(1 for k in keys if k in text)
            if score > 0:
                total_score += score
                matched_categories.append(cat)

        records.append({
            "date": today,
            "risk_score": total_score,          # can be 0
            "categories": ",".join(matched_categories) if matched_categories else "none",
            "source": os.path.basename(f)
        })

out = pd.DataFrame(records)

os.makedirs("data/evaluated", exist_ok=True)
out.to_csv(f"data/evaluated/evaluated_{today}.csv", index=False)

print(f"Safety evaluation completed for {today}, rows:", len(out))
