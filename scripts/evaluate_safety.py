import pandas as pd
import glob
import os
from datetime import datetime

RISK_KEYWORDS = {
    "AI safety": ["safety", "alignment", "risk"],
    "AI regulation": ["regulation", "law", "policy"],
    "AI bias": ["bias", "fairness", "discrimination"],
    "AI misuse": ["misuse", "weapon", "abuse"]
}

files = glob.glob("data/raw/*.csv")
records = []

for f in files:
    df = pd.read_csv(f)
    for _, row in df.iterrows():
        text = " ".join(map(str, row.values)).lower()
        for cat, keys in RISK_KEYWORDS.items():
            score = sum(1 for k in keys if k in text)
            records.append({
                "date": datetime.utcnow(),
                "category": cat,
                "risk_score": score,
                "source": os.path.basename(f)
            })

out = pd.DataFrame(records)

os.makedirs("data/evaluated", exist_ok=True)
today = datetime.utcnow().strftime("%Y-%m-%d")
out.to_csv(f"data/evaluated/evaluated_{today}.csv", index=False)

print("Safety evaluation completed:", today)
