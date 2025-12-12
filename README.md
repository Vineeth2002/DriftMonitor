# DriftMonitor  
### AI Drift & Safety Monitoring System (Lightweight · Automated · GitHub-Native)

![Collect](https://img.shields.io/badge/Collect-Daily-blue)
![Evaluate](https://img.shields.io/badge/Evaluate-Daily-green)
![Metrics](https://img.shields.io/badge/Metrics-Weekly-orange)
![Report](https://img.shields.io/badge/Report-GitHub%20Pages-purple)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-success)

**DriftMonitor** is a fully automated AI safety and risk monitoring system designed
to run entirely on GitHub infrastructure.

It collects small batches of real-world public text daily, evaluates them for
AI safety and misuse signals, tracks risk trends over time, and publishes a
live HTML dashboard via GitHub Pages.

The system is engineered to be:

- **Lightweight** — no external servers, no GPUs, no paid APIs  
- **Reproducible** — deterministic outputs with safe fallbacks  
- **Research-oriented** — safety scoring, risk trends, drift over time  
- **Reviewer-friendly** — clean architecture, documented, automated  
- **Always live** — dashboards update automatically  

---

## 🌐 Live Demo (GitHub Pages)

👉 **https://vineeth2002.github.io/driftmonitor/**  

---

## ✨ Key Features

### 🔹 Data Collection
- Google Trends (via `pytrends`)
- Hacker News (public Firebase API)
- Timestamped daily snapshots
- Append-only historical storage

### 🔹 Safety Evaluation
- Hybrid **SafetyClassifier** combining:
  - Lightweight sentiment analysis (DistilBERT)
  - Rule-based toxicity detection
  - Misuse & jailbreak pattern detection
- Produces:
  - Safety score (0–1)
  - Risk label: SAFE / WARNING / RISKY
  - Human-readable explanation

### 🔹 Risk & Trend Metrics
- Daily risk summaries
- Weekly risk aggregation
- Monthly risk aggregation
- Enables safety drift analysis over time

### 🔹 Reporting
- Static HTML dashboard
- Daily / weekly / monthly sections
- Auto-published via GitHub Pages

### 🔹 Automation
All stages are automated using GitHub Actions:

- **Daily Collect** → fetch public data
- **Daily Evaluate** → compute safety results
- **Weekly Metrics** → aggregate risk trends
- **Monthly Metrics** → long-term trends
- **Report Build** → publish dashboard

All outputs are committed to the repository for transparency and reproducibility.

---

## 🏗 System Architecture

┌──────────────────────────────────────────────┐
│                GitHub Actions                │
│        (Scheduled & Manual Workflows)        │
└──────────────────────────┬───────────────────┘
                           │
        ┌──────────────────▼──────────────────┐
        │             Data Collectors          │
        │                                      │
        │  • Google Trends (pytrends)          │
        │  • HackerNews (Firebase API)         │
        │  • Custom / Template Collectors      │
        │                                      │
        │  Output: timestamped raw JSON        │
        └──────────────────┬──────────────────┘
                           │
                     Raw Data Storage
                  data/live/raw/YYYY-MM-DD/
                           │
        ┌──────────────────▼──────────────────┐
        │          Safety Evaluation Layer     │
        │                                      │
        │  SafetyClassifier (Hybrid):          │
        │   • Sentiment analysis               │
        │   • Toxicity keyword scoring         │
        │   • Misuse / jailbreak detection    │
        │                                      │
        │  Output: safety scores + labels      │
        └──────────────────┬──────────────────┘
                           │
                  Processed Evaluation Data
              data/live/processed/YYYY-MM-DD/
                           │
        ┌──────────────────▼──────────────────┐
        │    Metrics & Drift Analysis Layer    │
        │                                      │
        │  • Daily risk summaries              │
        │  • Weekly risk aggregation           │
        │  • Monthly risk aggregation          │
        │                                      │
        │  Enables longitudinal drift tracking│
        └──────────────────┬──────────────────┘
                           │
        ┌──────────────────▼──────────────────┐
        │             Reporting Layer          │
        │                                      │
        │  • Static HTML dashboard             │
        │  • Daily / Weekly / Monthly views   │
        │                                      │
        │  Auto-published via GitHub Pages     │
        └──────────────────┬──────────────────┘
                           ▼
                 Live Dashboard (Public)
           https://vineeth2002.github.io/driftmonitor/

---

## 🚀 Quick Start (Local)

```bash
git clone https://github.com/Vineeth2002/driftmonitor
cd driftmonitor
pip install -r requirements.txt

# Run collectors (real data)
python scripts/collect/run_collectors.py

# Run daily safety evaluation
python scripts/evaluate/run_safety_eval.py

# Generate dashboard
python -m driftmonitor.report.html.report_builder
