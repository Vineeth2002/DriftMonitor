#!/usr/bin/env python3
"""
Build a minimal HTML dashboard.
"""

import json
from pathlib import Path
from datetime import datetime

PROCESSED = Path("data/live/processed")
DOCS = Path("docs")
DOCS.mkdir(exist_ok=True)


def main():
    dates = sorted(d.name for d in PROCESSED.iterdir() if d.is_dir())
    if not dates:
        DOCS.joinpath("index.html").write_text(
            "<h2>No data available yet</h2>",
            encoding="utf-8",
        )
        return

    latest = dates[-1]
    data = json.loads(
        (PROCESSED / latest / "evaluated.json").read_text(encoding="utf-8")
    )

    rows = "".join(
        f"<tr><td>{i.get('text','')[:80]}</td>"
        f"<td>{i.get('risk_label','')}</td>"
        f"<td>{i.get('safety_score',0):.2f}</td></tr>"
        for i in data.get("items", [])
    )

    html = f"""
    <html>
    <head><title>DriftMonitor</title></head>
    <body>
    <h1>DriftMonitor Dashboard</h1>
    <p>Last updated: {latest}</p>
    <table border="1">
      <tr><th>Text</th><th>Risk</th><th>Score</th></tr>
      {rows}
    </table>
    </body>
    </html>
    """

    DOCS.joinpath("index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()

