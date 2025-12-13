import json
from pathlib import Path
from datetime import datetime
from jinja2 import Template

BASE = Path("data/live/processed")
DOCS = Path("docs")
TEMPLATE = Path("driftmonitor/report/templates/report_template.html")
ASSETS_SRC = Path("driftmonitor/report/assets")
ASSETS_DST = DOCS / "assets"


def load_latest():
    if not BASE.exists():
        return None, []

    dates = sorted(d.name for d in BASE.iterdir() if d.is_dir())
    if not dates:
        return None, []

    latest = dates[-1]
    data_file = BASE / latest / "evaluated.json"
    if not data_file.exists():
        return None, []

    data = json.loads(data_file.read_text(encoding="utf-8"))
    return latest, data.get("items", [])


def main():
    DOCS.mkdir(exist_ok=True)
    ASSETS_DST.mkdir(exist_ok=True)

    # copy css
    for f in ASSETS_SRC.iterdir():
        (ASSETS_DST / f.name).write_text(f.read_text(encoding="utf-8"))

    date, items = load_latest()

    if not items:
        DOCS.joinpath("index.html").write_text(
            "<h2>No data available yet. Pipelines will update automatically.</h2>",
            encoding="utf-8",
        )
        return

    counts = {
        "safe": sum(1 for i in items if i["risk_label"] == "SAFE"),
        "warning": sum(1 for i in items if i["risk_label"] == "WARNING"),
        "risky": sum(1 for i in items if i["risk_label"] == "RISKY"),
        "total": len(items),
    }

    tpl = Template(TEMPLATE.read_text(encoding="utf-8"))
    html = tpl.render(
        date=date,
        items=items[:50],   # limit table size
        counts=counts,
    )

    DOCS.joinpath("index.html").write_text(html, encoding="utf-8")
    print(f"[OK] Dashboard built for {date}")


if __name__ == "__main__":
    main()
