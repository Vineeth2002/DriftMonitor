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

    safe = sum(1 for i in data["items"] if i["safety_score"] >= 0.7)
    warning = sum(1 for i in data["items"] if 0.4 <= i["safety_score"] < 0.7)
    risky = sum(1 for i in data["items"] if i["safety_score"] < 0.4)

    rows = "".join(
        f"<tr><td>{i['source']}</td>"
        f"<td>{i['text'][:120]}</td>"
        f"<td>{i['risk_label']}</td>"
        f"<td>{i['safety_score']:.2f}</td></tr>"
        for i in data["items"]
    )

    html = f"""
    <html>
    <head>
        <title>DriftMonitor</title>
        <style>
            body {{ font-family: Arial; margin: 30px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background: #f4f4f4; }}
        </style>
    </head>
    <body>
        <h1>DriftMonitor Dashboard</h1>
        <p>Last updated: {latest}</p>

        <ul>
            <li>Total: {data['total']}</li>
            <li>Safe: {safe}</li>
            <li>Warning: {warning}</li>
            <li>Risky: {risky}</li>
        </ul>

        <table>
            <tr>
                <th>Source</th>
                <th>Text</th>
                <th>Risk</th>
                <th>Safety Score</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    DOCS.joinpath("index.html").write_text(html, encoding="utf-8")
    print("[OK] Dashboard built")


if __name__ == "__main__":
    main()
