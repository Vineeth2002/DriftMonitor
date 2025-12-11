#!/usr/bin/env python3
"""
Google Trends collector.

Design goals:
- Lightweight: sample size limit, small payloads.
- Robust: fallback to bundled sample data if pytrends/network fails.
- GitHub Actions friendly: no secrets required.
"""

from __future__ import annotations
import json
import logging
import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    # pytrends is optional — we'll handle ImportError gracefully.
    from pytrends.request import TrendReq
except Exception:  # pragma: no cover - import-time fallback
    TrendReq = None  # type: ignore

DEFAULT_OUTPUT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "live", "raw")
)
SAMPLE_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "live", "raw", "google_trends_sample.json")
)

logger = logging.getLogger("driftmonitor.collectors.google_trends")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class GoogleTrendsCollector:
    """
    Collector for Google Trends data.

    Basic usage:
        collector = GoogleTrendsCollector(output_dir="data/live/raw", kw_list=["ai safety", "llm safety"])
        results = collector.collect()
        collector.save(results)

    It will try to use pytrends if available and network works. Otherwise it will load SAMPLE_FILE.
    """

    def __init__(
        self,
        output_dir: str = DEFAULT_OUTPUT_DIR,
        kw_list: Optional[List[str]] = None,
        timeframe: str = "now 7-d",
        geo: str = "",
        max_terms: int = 50,
    ):
        self.kw_list = kw_list or ["ai safety", "llm", "chatbot safety"]
        self.timeframe = timeframe
        self.geo = geo
        self.max_terms = int(max_terms)
        self.output_dir = os.path.abspath(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        logger.debug("GoogleTrendsCollector initialized", extra={
            "kw_list": self.kw_list, "timeframe": self.timeframe, "geo": self.geo
        })

    def _fetch_with_pytrends(self) -> List[Dict[str, Any]]:
        """Fetch interest_over_time for each keyword using pytrends."""
        if TrendReq is None:
            raise RuntimeError("pytrends not installed or unavailable.")

        pytrends = TrendReq(timeout=(10, 25))
        results: List[Dict[str, Any]] = []
        keywords = self.kw_list[: self.max_terms]
        for kw in keywords:
            try:
                logger.info("Fetching Google Trends for: %s", kw)
                pytrends.build_payload([kw], timeframe=self.timeframe, geo=self.geo)
                df = pytrends.interest_over_time()
                if df is None or df.empty:
                    logger.warning("No data returned for keyword: %s", kw)
                    continue
                series = df[kw].dropna().astype(int).to_dict()
                results.append(
                    {
                        "keyword": kw,
                        "timeframe": self.timeframe,
                        "geo": self.geo,
                        "data_points": len(series),
                        "series": series,
                    }
                )
            except Exception as exc:
                logger.exception("pytrends fetch failed for %s: %s", kw, exc)
                # don't fail the whole job; continue with other keywords
                continue
        return results

    def _load_sample(self) -> List[Dict[str, Any]]:
        """Load bundled sample file as fallback."""
        logger.info("Loading sample Google Trends data from %s", SAMPLE_FILE)
        if not os.path.exists(SAMPLE_FILE):
            logger.error("Sample file not found: %s", SAMPLE_FILE)
            return []
        with open(SAMPLE_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        # Ensure it's a list
        if isinstance(data, dict):
            data = [data]
        return data

    def collect(self) -> List[Dict[str, Any]]:
        """
        Main collect method.

        Tries pytrends first; if anything fails, falls back to bundled sample.
        """
        try:
            if TrendReq is None:
                raise RuntimeError("pytrends unavailable")
            data = self._fetch_with_pytrends()
            if not data:
                logger.warning("pytrends returned no results; using sample fallback.")
                data = self._load_sample()
            return data
        except Exception as exc:
            logger.warning("pytrends path failed (%s); using sample data.", exc)
            return self._load_sample()

    def save(self, results: List[Dict[str, Any]]) -> str:
        """Save raw results to timestamped JSON and also create a small processed CSV summary."""
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = os.path.join(self.output_dir, f"google_trends_{ts}.json")
        logger.info("Saving %d results to %s", len(results), filename)
        with open(filename, "w", encoding="utf-8") as fh:
            json.dump({"collected_at": ts, "results": results}, fh, indent=2, ensure_ascii=False)

        # also write a compact CSV summary (keyword, data_points)
        try:
            import csv

            csvfile = os.path.join(self.output_dir, f"google_trends_{ts}.summary.csv")
            with open(csvfile, "w", newline="", encoding="utf-8") as cf:
                writer = csv.writer(cf)
                writer.writerow(["keyword", "data_points", "timeframe", "geo"])
                for r in results:
                    writer.writerow([r.get("keyword"), r.get("data_points"), r.get("timeframe"), r.get("geo")])
            logger.info("Wrote summary CSV to %s", csvfile)
        except Exception:
            logger.exception("Failed to write CSV summary (non-fatal).")

        return filename


def main_cli():
    """Simple CLI entrypoint for quick manual runs."""
    import argparse

    parser = argparse.ArgumentParser(description="DriftMonitor: Google Trends collector (lightweight).")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Where to save raw JSON output.")
    parser.add_argument("--keywords", nargs="+", help="List of keywords to collect.", default=None)
    parser.add_argument("--timeframe", default="now 7-d", help="Google Trends timeframe (e.g. 'now 7-d').")
    parser.add_argument("--geo", default="", help="Geo code (country) for trends, default global.")
    parser.add_argument("--max-terms", default=50, type=int, help="Max number of terms to collect.")
    args = parser.parse_args()

    collector = GoogleTrendsCollector(
        output_dir=args.output_dir,
        kw_list=args.keywords,
        timeframe=args.timeframe,
        geo=args.geo,
        max_terms=args.max_terms,
    )
    results = collector.collect()
    saved = collector.save(results)
    print(f"Saved Google Trends raw output to: {saved}")


if __name__ == "__main__":
    main_cli()
