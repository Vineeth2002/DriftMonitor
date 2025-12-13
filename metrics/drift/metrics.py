import math
from collections import Counter
from typing import Dict, Iterable, List

EPS = 1e-12


def tokenize(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    text = text.lower()
    for ch in '.,;:"()[]{}<>!?/\\|`~@#$%^&*-_=+':
        text = text.replace(ch, " ")
    return [t for t in text.split() if t]


def texts_to_unigram_dist(texts: Iterable[str]) -> Dict[str, float]:
    counter = Counter()
    total = 0

    for t in texts:
        toks = tokenize(t)
        counter.update(toks)
        total += len(toks)

    if total == 0:
        return {}

    return {k: v / total for k, v in counter.items()}


def _union(p: Dict[str, float], q: Dict[str, float]):
    return set(p.keys()) | set(q.keys())


def kldiv(p: Dict[str, float], q: Dict[str, float]) -> float:
    kl = 0.0
    for k in _union(p, q):
        p_k = p.get(k, 0.0)
        if p_k == 0:
            continue
        q_k = q.get(k, EPS) or EPS
        kl += p_k * math.log(p_k / q_k)
    return kl


def jensen_shannon(p: Dict[str, float], q: Dict[str, float]) -> float:
    if not p and not q:
        return 0.0

    m = {k: 0.5 * (p.get(k, 0.0) + q.get(k, 0.0)) for k in _union(p, q)}
    jsd = 0.5 * (kldiv(p, m) + kldiv(q, m))
    return min(1.0, jsd / math.log(2.0))
