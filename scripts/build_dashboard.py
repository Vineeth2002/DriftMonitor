import pandas as pd
import os
from datetime import datetime

BASE_DIR = "data/history"
DOCS_DIR = "docs"

os.makedirs(DOCS_DIR, exist_ok=True)

def severity_logic(p):
    if p > 30:
        return "HIGH"
    elif p > 10:
        return "MEDIUM"
    else:
        return "LOW"

def build_table(df, time_col):
    rows = []
    total_words_all = df["total_words"].sum()
    total_risk_all = df["risk_words"].sum()

    for _, r in df.iterrows():
        perc = (r["risk_words"] / r["total_words"] * 100) if r["total_words"] > 0 else 0
        sev = severity_logic(perc)
        rows.append(f"""
        <tr class="{sev.lower()}">
            <td>{r[time_col]}</td>
            <td>{r['category']}</td>
            <td>{r['total_words']}</td>
            <td>{r['risk_words']}</td>
            <td>{perc:.2f}%</td>
            <td><span class="badge {sev.lower()}">{sev}</span></td>
        </tr>
        """)

    return "\n".join(rows)

html = f"""
<!DOCTYPE html>
<html>
<head>
<title>AI Drift Monitor</title>
<style>
body {{
    font-family: "Segoe UI", Arial, sans-serif;
    background: #f4f6f9;
    margin: 0;
    padding: 30px;
    color: #212529;
}}

h1 {{
    margin-bottom: 5px;
}}

.subtitle {{
    color: #6c757d;
    margin-bottom: 30px;
}}

.section {{
    background: white;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th {{
    background: #212529;
    color: white;
    padding: 10px;
    font-size: 13px;
}}

td {{
    padding: 9px;
    text-align: center;
    font-size: 13px;
}}

tr:nth-child(even) {{
    background: #f8f9fa;
}}

.badge {{
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 12px;
}}

.low {{
    background: #e6f4ea;
    color: #0f5132;
}}

.medium {{
    background: #fff3cd;
    color: #664d03;
}}

.high {{
    background: #f8d7da;
    color: #842029;
}}

.footer {{
    text-align: center;
    font-size: 12px;
    color: #6c757d;
    margin-top: 40px;
}}
</style>
</head>

<body>

<h1>AI Drift Monitor</h1>
<div class="subtitle">
Automated AI Safety Risk Monitoring · Table-based · Policy-ready
</div>
"""

# ---------
