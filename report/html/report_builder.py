#!/usr/bin/env python3
"""
DriftMonitor HTML Report Builder (full file).

- Loads latest evaluation and summary
- Loads metrics (daily/weekly/monthly)
- Renders template into report/html/report.html
- Copies metrics JSON into report/html/assets/data/
"""

import os
import json
import glob
import logging
import shutil
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "live", "processed")
OUTPUT_DIR = os.path.join(BASE_DIR, "report", "html")
TEMPLATE_DIR = os.path.join(BASE_DIR, "report", "templates")

logger = logging.getLogger("driftmonitor.report.html.builder")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def load_latest_json_by_pattern(dirpath: str, pattern: str):
    files = sorted(glob.glob(os.path.join(dirpath, pattern)))
    if not files:
        return None
    path = files[-1]
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        data["_source_file"] = os.path.basename(path)
        return data
    except Exception:

        return None

def load_metrics_file(name: str):
    p = os.path.join(PROCESSED_DIR, name)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return None
    return None

def render_html():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    eval_data = load_latest_json_by_pattern(PROCESSED_DIR, "eval_*.json")
    eval_summary = load_latest_json_by_pattern(PROCESSED_DIR, "eval_summary_*.json")
    drift = load_latest_json_by_pattern(PROCESSED_DIR, "drift_summary_*.json")

    metrics_daily = load_metrics_file("metrics_daily.json")
    metrics_weekly = load_metrics_file("metrics_weekly.json")
    metrics_monthly = load_metrics_file("metrics_monthly.json")

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("report_template.html")
@@ -45,16 +65,28 @@ def render_html():
        eval=eval_data,
        summary=eval_summary,
        drift_summary=drift,
        metrics_daily=metrics_daily,
        metrics_weekly=metrics_weekly,
        metrics_monthly=metrics_monthly,
    )

    output_path = os.path.join(OUTPUT_DIR, "report.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    assets_data_dir = os.path.join(OUTPUT_DIR, "assets", "data")
    os.makedirs(assets_data_dir, exist_ok=True)
    for fname in ("metrics_daily.json", "metrics_weekly.json", "metrics_monthly.json", "drift_summary.json"):
        src = os.path.join(PROCESSED_DIR, fname)
        if os.path.exists(src):
            try:
                shutil.copy(src, os.path.join(assets_data_dir, fname))
            except Exception:
                logger.warning("Failed copying metrics file: %s", src)

    logger.info("Saved HTML report → %s", output_path)
    return output_path


if __name__ == "__main__":
    path = render_html()
    print("Report generated →", path)
