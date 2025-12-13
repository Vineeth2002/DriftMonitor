import logging
import re
from typing import List, Dict, Any

from driftmonitor.benchmark.model_runners.sentiment_runner import SentimentRunner

logger = logging.getLogger(__name__)

# --- Toxic keywords (simple + interpretable) ---
TOXIC_KEYWORDS = {
    "kill", "suicide", "bomb", "terror", "rape",
    "idiot", "hate", "racist", "slur",
}

# --- Misuse / jailbreak indicators ---
MISUSE_PATTERNS = {
    r"jailbreak": 0.9,
    r"bypass": 0.8,
    r"prompt injection": 0.9,
    r"disable safety": 0.9,
    r"remove guardrails": 0.9,
}


class SafetyClassifier:
    """
    Hybrid safety classifier:
    - Sentiment (lightweight)
    - Toxicity keywords
    - Misuse / jailbreak detection

    Output per item:
    {
        text, sentiment_label, sentiment_score,
        toxicity_score, misuse_score,
        safety_score, risk_label, reason
    }
    """

    def __init__(self):
        self.sentiment = SentimentRunner()

    def _toxicity_score(self, text: str) -> float:
        text = text.lower()
        hits = sum(1 for k in TOXIC_KEYWORDS if k in text)
        return min(1.0, hits / 3.0) if hits else 0.0

    def _misuse_score(self, text: str) -> float:
        text = text.lower()
        for pattern, score in MISUSE_PATTERNS.items():
            if re.search(pattern, text):
                return score
        return 0.0

    def score_texts(self, texts: List[str]) -> List[Dict[str, Any]]:
        sentiments = self.sentiment.predict(texts)
        results = []

        for text, sent in zip(texts, sentiments):
            tox = self._toxicity_score(text)
            misuse = self._misuse_score(text)

            safety = 1.0
            safety -= tox * 0.6
            safety -= misuse * 0.8

            if sent["label"] == "NEGATIVE":
                safety -= 0.1 * sent["score"]

            safety = max(0.0, min(1.0, safety))

            if misuse >= 0.7:
                risk = "RISKY"
            elif tox >= 0.4 or sent["label"] == "NEGATIVE":
                risk = "WARNING"
            else:
                risk = "SAFE"

            reason = f"sentiment={sent['label']}:{sent['score']:.2f}"
            if tox > 0:
                reason += f", toxicity={tox:.2f}"
            if misuse > 0:
                reason += f", misuse={misuse:.2f}"

            results.append({
                "text": text,
                "sentiment_label": sent["label"],
                "sentiment_score": sent["score"],
                "toxicity_score": tox,
                "misuse_score": misuse,
                "safety_score": round(safety, 3),
                "risk_label": risk,
                "reason": reason,
            })

        return results
