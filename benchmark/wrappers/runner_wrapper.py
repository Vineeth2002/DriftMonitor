import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RunnerWrapper:
    """
    Standard wrapper to normalize runner outputs.
    """

    def __init__(self, name: str):
        self.name = name

    def run(self, runner, texts: List[str]) -> Dict[str, Any]:
        preds = runner.predict(texts)
        return {
            "runner": self.name,
            "n_items": len(texts),
            "predictions": preds,
        }
