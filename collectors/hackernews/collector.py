#!/usr/bin/env python3
"""
HackerNews collector.

Design goals:
- Lightweight and fast (limit number of items fetched).
- No secrets or API keys required (uses public Firebase API).
- Robust fallback to bundled sample data.
- GitHub Actions friendly.
"""

from __future__ import annotations
import json
import logging
import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

import requests

DEFAULT_OUTPUT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "live", "raw")
)
SAMPLE_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "live", "raw", "hackernews_sample.json")
)

HN_TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

logger = logging.getLogger("driftmonitor.collectors.hackernews")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class HackerNewsCollector:
    """
    Collector for Hacker News top stories.

    Example usage:
        collector = HackerNewsCollector(output_dir="data/live/raw", fetch_top_n=50)
        items = collector.collect()
        collector.save(items)
    """

    def __init__(
        self,
        output_dir: str = DEFAULT_OUTPUT_DIR,
        fetch_top_n: int = 100,
        include_comments: bool = False,
        timeout: int = 10,
    ):
        self.output_dir = os.path.abspath(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        self.fetch_top_n = int(fetch_top_n)
        self.include_comments = bool(include_comments)
        self.timeout = int(timeout)
        logger.debug("HackerNewsCollector initialized", extra={
            "fetch_top_n": self.fetch_top_n, "include_comments": self.include_comments
        })

    def _fetch_top_ids(self) -> List[int]:
        """Fetch top story IDs from HN API."""
        logger.info("Fetching top story IDs from Hacker News")
        resp = requests.get(HN_TOP_STORIES, timeout=self.timeout)
        resp.raise_for_status()
        ids = resp.json()
        if not isinstance(ids, list):
            raise RuntimeError("Unexpected topstories response")
        return ids[: self.fetch_top_n]

    def _fetch_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a single item by ID."""
        try:
            resp = requests.get(HN_ITEM_URL.format(item_id), timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            logger.exception("Failed to fetch item %s", item_id)
            return None

    def _load_sample(self) -> List[Dict[str, Any]]:
        """Load bundled sample file as fallback."""
        logger.info("Loading sample HackerNews data from %s", SAMPLE_FILE)
        if not os.path.exists(SAMPLE_FILE):
            logger.error("HackerNews sample file not found: %s", SAMPLE_FILE)
            return []
        with open(SAMPLE_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            data = [data]
        return data

    def collect(self) -> List[Dict[str, Any]]:
        """
        Main collect method.

        Tries to fetch from Hacker News API; falls back to bundled sample if anything fails.
        """
        try:
            top_ids = self._fetch_top_ids()
            results: List[Dict[str, Any]] = []
            for idx, item_id in enumerate(top_ids):
                item = self._fetch_item(item_id)
                if not item:
                    continue
                # Optionally drop long fields (keep payload small)
                trimmed = {
                    "id": item.get("id"),
                    "type": item.get("type"),
                    "by": item.get("by"),
                    "time": item.get("time"),
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "score": item.get("score"),
                    "descendants": item.get("descendants"),
                }
                results.append(trimmed)
                # pace requests a little to be polite
                time.sleep(0.1)
            if not results:
                logger.warning("No items fetched; using sample fallback.")
                return self._load_sample()
            return results
        except Exception as exc:
            logger.warning("HackerNews path failed (%s); using sample data.", exc)
            return self._load_sample()

    def save(self, results: List[Dict[str, Any]]) -> str:
        """Save raw results to timestamped JSON file and return path."""
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = os.path.join(self.output_dir, f"hackernews_{ts}.json")
        logger.info("Saving %d HackerNews items to %s", len(results), filename)
        with open(filename, "w", encoding="utf-8") as fh:
            json.dump({"collected_at": ts, "results": results}, fh, indent=2, ensure_ascii=False)
        return filename


def main_cli():
    """Command-line entrypoint for manual runs."""
    import argparse

    parser = argparse.ArgumentParser(description="DriftMonitor: HackerNews collector (lightweight).")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Where to save raw JSON output.")
    parser.add_argument("--fetch-top-n", default=50, type=int, help="Number of top stories to fetch.")
    parser.add_argument("--include-comments", action="store_true", help="Include comment counts/descendants.")
    parser.add_argument("--timeout", default=10, type=int, help="HTTP timeout in seconds.")
    args = parser.parse_args()

    collector = HackerNewsCollector(
        output_dir=args.output_dir,
        fetch_top_n=args.fetch_top_n,
        include_comments=args.include_comments,
        timeout=args.timeout,
    )
    results = collector.collect()
    saved = collector.save(results)
    print(f"Saved HackerNews raw output to: {saved}")


if __name__ == "__main__":
    main_cli()
