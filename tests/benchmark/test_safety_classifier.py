
---

### File: `DriftMonitor/tests/benchmark/test_safety_classifier.py`
```python
from driftmonitor.benchmark.classifiers.safety_classifier import SafetyClassifier

def test_score_texts_basic():
    clf = SafetyClassifier()
    texts = [
        "I love this model, it is safe and helpful.",
        "You should kill the process and delete files. This is dangerous!",
        "This is mediocre, sometimes wrong but not toxic."
    ]
    results = clf.score_texts(texts)
    assert isinstance(results, list)
    assert len(results) == 3
    # check expected keys
    for r in results:
        assert "safety_score" in r
        assert 0.0 <= r["safety_score"] <= 1.0
        assert "reason" in r
