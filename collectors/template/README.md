# Collector Template (DriftMonitor)

This folder contains a reusable template for building new collectors in DriftMonitor.

## Purpose
- Provide a minimal, well-documented starting point for new data sources.
- Demonstrate fallback behavior, saving, and CLI usage.
- Keep collector payloads small and Actions-friendly.

## How to extend
1. Copy `collector.py` into a new collector folder (e.g., `collectors/my_source/`).
2. Implement `_fetch_remote(self)` to fetch data from your source (API, scraping, etc.).
3. Add a sample fallback JSON to `data/live/raw/<your_sample>.json`.
4. Add test coverage under `tests/collectors/`.

## Quick local run
```bash
python -m driftmonitor.collectors.template.cli --output-dir data/live/raw --max-items 100
