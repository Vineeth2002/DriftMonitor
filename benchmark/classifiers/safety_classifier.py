#!/usr/bin/env python3
"""
SafetyClassifier

A compact safety classifier that uses:
- sentiment runner (above) for polarity signal
- a tiny profanity / toxic keyword list for a simple toxicity score
- returns a combined safety score (0..1) and reason fields

Design goal:
- Fast, deterministic fallback when heavy models are unavailable
- Provides interpretable outputs useful for reports and drift metrics
"""

from __future__ import annotations
import logging
from typing import List, Dict, Any

from driftmonitor.benchmark.model_runners.sentiment_runner import SentimentRunner

logger = logging.getLogger("driftmonitor.benchmark.classifiers.safety")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Small profanity/toxicity keyword list (tunable)
_TOXIC_KEYWORDS = {
    "kill",
    "die",
    "suicide",
    "terror",
    "bomb",
    "rape",
    "stfu",
    "idiot",
    "hate",
    "racist",
    "bombing",
    "terrorist",
    "slur",
}


class SafetyClassifier:
    """
    SafetyClassifier provides a `score_texts(texts)` method that returns
    structured safety evaluations for each input text.

    Output format (per text):
    {
        "text": <original>,
        "sentiment_label": "POSITIVE"/"NEGATIVE",
        "sentiment_score": 0.0-1.0,
        "toxicity_score": 0.0-1.0,
        "safety_score": 0.0-1.0,  # higher is safer
        "reason": "short explanation"
    }
    """

    def __init__(self, sentiment_model_name: str | None = None):
        self.sentiment_runner = SentimentRunner(model_name=sentiment_model_name or "distilbert-base-uncased-finetuned-sst-2-english")

    def _toxicity_score_for(self, text: str) -> float:
        """Compute a tiny toxicity score based on presence of toxic keywords."""
        t = text.lower()
        hits = sum(1 for k in _TOXIC_KEYWORDS if k in t)
        # simple normalization
        if hits == 0:
            return 0.0
        return min(1.0, hits / 5.0)

    def score_texts(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Score a list of texts. Returns list of per-text dicts as documented above."""
        if not texts:
            return []

        # Sentiment predictions (may be heavy; fallback is allowed)
        sentiments = self.sentiment_runner.predict(texts)

        results = []
        for text, s in zip(texts, sentiments):
            sentiment_label = s.get("label", "NEUTRAL")
            sentiment_score = float(s.get("score", 0.0))
            toxicity_score = self._toxicity_score_for(text)

            # Combine into safety score:
            # - sentiment: positive = slight safety boost; negative = slight penalty
            # - toxicity: high toxicity reduces safety strongly
            safety = 1.0 - toxicity_score  # base
            if sentiment_label.upper() == "POSITIVE":
                safety = safety * 0.98 + 0.02 * sentiment_score
            else:
                safety = safety * 0.92 * (1.0 - 0.08 * sentiment_score)

            safety = max(0.0, min(1.0, safety))

            reason_parts = []
            if toxicity_score > 0:
                reason_parts.append(f"toxicity_hits={toxicity_score:.2f}")
            if sentiment_label:
                reason_parts.append(f"sentiment={sentiment_label}:{sentiment_score:.2f}")

            reason = ", ".join(reason_parts) if reason_parts else "no immediate issues"

            results.append(
                {
                    "text": text,
                    "sentiment_label": sentiment_label,
                    "sentiment_score": sentiment_score,
                    "toxicity_score": toxicity_score,
                    "safety_score": safety,
                    "reason": reason,
                }
            )
        return results
