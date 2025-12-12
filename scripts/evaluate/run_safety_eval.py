from datetime import datetime
from pathlib import Path
import json

from driftmonitor.benchmark.classifiers.safety_classifier import SafetyClassifier

TODAY = datetime.utcnow().strftime("%Y-%m-%d")

RAW_DIR = Path(f"data/live/raw/{TODAY}")
OUT_DIR = Path(f"data/live/processed/{TODAY}")
OUT_DIR.mkdir(parents=True, exist_ok=True)

classifier = SafetyClassifier()

def load_texts():
    texts = []

    for file in RAW_DIR.glob("*.json"):
        data = json.load(open(file))
        for item in data.get("results", []):
            texts.append({
                "source": item["source"],
                "title": item["title"],
                "text": item["text"]
            })
    return texts

def main():
    items = load_texts()
    results = []

    scores = classifier.score_texts([i["text"] for i in items])

    for item, score in zip(items, scores):
        results.append({
            "date": TODAY,
            "source": item["source"],
            "title": item["title"],
            **score
        })

    with open(OUT_DIR / "safety_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"[OK] Safety evaluation completed for {TODAY}")

if __name__ == "__main__":
    main()
