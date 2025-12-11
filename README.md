# DriftMonitor  
### AI Drift & Safety Monitoring System (Lightweight · Automated · GitHub-Native)

[![Daily Collect](https://img.shields.io/badge/Collect-Automated-blue)]()
[![Daily Evaluate](https://img.shields.io/badge/Evaluate-Automated-green)]()
[![Weekly Metrics](https://img.shields.io/badge/Metrics-Automated-orange)]()
[![Report Build](https://img.shields.io/badge/Report-GitHub%20Pages-purple)]()
[![Tests](https://img.shields.io/badge/Tests-PyTest-success)]()

**DriftMonitor** is a fully automated AI drift & safety monitoring pipeline designed to run entirely on GitHub infrastructure.  
It collects small batches of real-world text daily, evaluates them for safety signals, computes drift over time, and publishes a live HTML report via GitHub Pages.

The system is engineered to be:

- **Lightweight** — zero external servers, zero heavy compute  
- **Reproducible** — sample fallbacks ensure pipelines never break  
- **Research-oriented** — drift metrics, toxicity summaries, sentiment signals  
- **Reviewer-friendly** — clean architecture + documented + automated  
- **Always live** — reports update automatically  

---

## 🌐 Live Demo (GitHub Pages)
👉 **https://Vineeth2002.github.io/DriftMonitor/**  
(Works after enabling GitHub Pages → source: `/docs`)

---

## ✨ Features

### 🔹 Data Collectors  
- Google Trends (pytrends)  
- Hacker News (public Firebase API)  
- Custom Prompts Collector  
- Template for new collectors  
- Sample fallback for reproducibility

### 🔹 Evaluation Engine  
- SafetyClassifier combining:  
  - Lightweight sentiment runner (transformers optional)  
  - Rule-based toxicity scoring  
- Always runs in GitHub Actions (fallback ensures reliability)

### 🔹 Drift Metrics  
- Jensen–Shannon Divergence (normalized 0–1)  
- KL Divergence  
- Toxicity statistics across time windows  

### 🔹 Reporting  
- Jinja2-powered HTML reports  
- Embedded drift metrics  
- Toxicity comparison panels  
- GitHub Pages auto-publishing

### 🔹 Automation  
- **Daily Collect** → fetch raw data  
- **Daily Evaluate** → compute safety results  
- **Weekly Metrics** → compute drift summary  
- **Report Build** → publish HTML report to Pages  
- All artifacts saved in repo (`data/live/raw`, `data/live/processed`)

---

## 🏗 Architecture Overview

         ┌───────────────────────────────┐
         │         GitHub Actions         │
         │  (scheduled / manual triggers) │
         └──────────────┬────────────────┘
                        │
             ┌──────────▼───────────┐
             │      Collectors       │
             │ google_trends         │
             │ hackernews            │
             │ custom/template       │
             └──────────┬───────────┘
                        │ raw data
                        ▼
             ┌──────────▼───────────┐
             │      Evaluation       │
             │  SafetyClassifier     │
             │ sentiment + toxicity  │
             └──────────┬───────────┘
                        │ processed eval
                        ▼
             ┌──────────▼───────────┐
             │       Metrics         │
             │  JSD drift, toxicity  │
             └──────────┬───────────┘
                        │ drift summary
                        ▼
             ┌──────────▼───────────┐
             │       Reporting       │
             │ HTML builder (Jinja2) │
             │ Pages publishing      │
             └──────────┬───────────┘
                        ▼
              GitHub Pages (Live Report)



---

## 🚀 Quick Start (Local)

```bash
git clone https://github.com/<your-username>/DriftMonitor
cd DriftMonitor
pip install -r requirements.txt

# Collect sample + real data
python -m driftmonitor.collectors.hackernews.cli
python -m driftmonitor.collectors.google_trends.cli

# Run evaluation
python -m driftmonitor.scripts.evaluate.run_evaluation

# Compute drift
python -m driftmonitor.scripts.metrics.run_metrics

# Build report
python -m driftmonitor.report.html.report_builder
 
