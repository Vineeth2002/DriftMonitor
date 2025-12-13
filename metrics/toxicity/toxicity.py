from typing import Iterable, Dict

DEFAULT_TOXIC_KEYWORDS = {
    "kill", "suicide", "terror", "bomb", "rape",
    "idiot", "stfu", "hate", "racist", "slur"
}


def toxicity_hits(text: str, keywords: Iterable[str] = DEFAULT_TOXIC_KEYWORDS) -> int:
    if not isinstance(text, str):
        return 0
    t = text.lower()
    return sum(1 for k in keywords if k in t)


def batch_toxicity_stats(texts: Iterable[str]) -> Dict[str, float]:
    texts = list(texts)
    n = len(texts)
    if n == 0:
        return {
            "n_texts": 0,
            "total_hits": 0,
            "avg_hits_per_text": 0.0,
            "pct_with_hits": 0.0,
        }

    hits = [toxicity_hits(t) for t in texts]
    total = sum(hits)
    return {
        "n_texts": n,
        "total_hits": total,
        "avg_hits_per_text": total / n,
        "pct_with_hits": sum(1 for h in hits if h > 0) / n,
    }
