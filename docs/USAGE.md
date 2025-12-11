# Usage Guide — DriftMonitor

This guide explains common usage patterns for local runs and GitHub Actions demos.

## Local full run (quick demo)
```bash
# 1. Run collectors (local)
python -m driftmonitor.collectors.google_trends.cli --output-dir data/live/raw
python -m driftmonitor.collectors.hackernews.cli --fetch-top-n 50 --output-dir data/live/raw
python -m driftmonitor.collectors.template.cli --output-dir data/live/raw

# 2. Evaluate
python -m driftmonitor.scripts.evaluate.run_evaluation

# 3. Compute drift summary (optional)
python -m driftmonitor.scripts.metrics.run_metrics --processed-dir data/live/processed

# 4. Build report
python -m driftmonitor.report.html.report_builder

# 5. Serve report locally (simple)
python -m http.server --directory report/html 8000
# then open: http://localhost:8000/report.html
