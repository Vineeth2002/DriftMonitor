#!/usr/bin/env python3
"""
Generic Collector Template for DriftMonitor.

Purpose:
- Provide a small, well-documented template that other collectors can copy/extend.
- Demonstrates config-driven behavior, fallback sample usage, and a CLI.
- Keeps runtime small and GitHub Actions friendly.

How to use:
- Copy this file into a new collector folder and adapt the `_fetch_remote` method.
- Ensure you add a sample fallback in data/live/raw/<your_sample>.json.
"""

from __future__ import annotations
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger("driftmonitor.collectors.template")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DEFAULT_OUTPUT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "live", "raw")
)
SAMPLE_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "live", "raw", "custom_prompts.json")
)


class TemplateCollector:
    """
    TemplateCollector

    Attributes
    ----------
    output_dir : str
        Directory to save output files.
    sample_path : str
        Path to sample fallback JSON file.
    max_items : int
        Maximum number of items to fetch / include.
    """

    def __init__(self, output_dir: str = DEFAULT_OUTPUT_DIR, sample_path: Optional[str] = None, max_items: int = 200):
        self.output_dir = os.path.abspath(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        self.sample_path = sample_path or SAMPLE_FILE
        self.max_items = int(max_items)
        logger.debug("TemplateCollector initialized", extra={"output_dir": self.output_dir, "sample_path": self.sample_path})

    def _fetch_remote(self) -> List[Dict[str, Any]]:
        """
        Replace or extend this method to implement real fetching logic.

        It should return a list of JSON-serializable dicts representing items.
        Keep payload small: only include necessary fields.
        """
        raise NotImplementedError("Override `_fetch_remote` with actual logic.")

    def _load_sample(self) -> List[Dict[str, Any]]:
        """Load bundled sample file as fallback."""
        logger.info("Loading sample data from %s", self.sample_path)
        if not os.path.exists(self.sample_path):
            logger.error("Sample file not found: %s", self.sample_path)
            return []
        with open(self.sample_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            data = [data]
        # Limit to max_items
        return data[: self.max_items]

    def collect(self) -> List[Dict[str, Any]]:
        """
        Top-level collect logic:
        - Try to run `_fetch_remote`
        - On any error, fall back to bundled sample
        - Ensure result is a list and limited to max_items
        """
        try:
            items = self._fetch_remote()
            if not items:
                logger.warning("Remote fetch returned no items; using sample fallback.")
                return self._load_sample()
            return items[: self.max_items]
        except Exception as exc:
            logger.exception("Remote fetch failed: %s", exc)
            return self._load_sample()

    def save(self, results: List[Dict[str, Any]]) -> str:
        """Save collected results to a timestamped JSON file and return path."""
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = os.path.join(self.output_dir, f"custom_prompts_{ts}.json")
        logger.info("Saving %d items to %s", len(results), filename)
        with open(filename, "w", encoding="utf-8") as fh:
            json.dump({"collected_at": ts, "results": results}, fh, indent=2, ensure_ascii=False)
        return filename


# Example subclass to demonstrate how to extend the template:
class CustomPromptsCollector(TemplateCollector):
    """
    Example implementation: returns local curated prompts (no network).

    This is a very small demo collector for reproducibility in GH Actions.
    """

    def _fetch_remote(self) -> List[Dict[str, Any]]:
        """
        For the demo, simply load the sample file as the main source (acts like an offline collector).
        Replace this with API calls, scraping, or other logic for real collectors.
        """
        logger.info("CustomPromptsCollector: using sample as primary source (demo mode).")
        return self._load_sample()


def main_cli():
    """CLI for running the template/demo collector."""
    import argparse

    parser = argparse.ArgumentParser(description="DriftMonitor: Template Collector (demo/custom).")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output directory for JSON files.")
    parser.add_argument("--max-items", default=200, type=int, help="Maximum number of items to collect.")
    args = parser.parse_args()

    collector = CustomPromptsCollector(output_dir=args.output_dir, max_items=args.max_items)
    results = collector.collect()
    saved = collector.save(results)
    print(f"Saved custom prompts output to: {saved}")


if __name__ == "__main__":
    main_cli()
