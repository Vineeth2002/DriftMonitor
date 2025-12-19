# DriftMonitor  
### AI Drift & Safety Monitoring System  
*(Lightweight · Automated · GitHub-Native)*

![Collect](https://img.shields.io/badge/Collect-Daily-blue)
![Evaluate](https://img.shields.io/badge/Evaluate-Daily-green)
![Metrics](https://img.shields.io/badge/Metrics-Weekly-orange)
![Report](https://img.shields.io/badge/Report-GitHub%20Pages-purple)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-success)

---

## 📌 Overview

**DriftMonitor** is a fully automated AI safety and risk monitoring system designed
to run entirely on **GitHub infrastructure**.

It continuously:
- Collects small batches of **real-world public text**
- Evaluates them for **AI safety, toxicity, and misuse risks**
- Tracks **risk drift over time**
- Publishes a **live HTML dashboard** via GitHub Pages

The system is designed to be:

- **Lightweight** — no external servers, no GPUs, no paid APIs  
- **Reproducible** — deterministic outputs, versioned data  
- **Research-oriented** — longitudinal drift & risk tracking  
- **Reviewer-friendly** — clean architecture, explainable logic  
- **Always live** — fully automated via GitHub Actions  

---

## 🌐 Live Demo (GitHub Pages)

👉 **https://vineeth2002.github.io/driftmonitor/**  

---

## ✨ Key Features

### 🔹 Data Collection
- Google Trends (via `pytrends`)
- Hacker News (public Firebase API)
- Daily timestamped snapshots
- Append-only historical storage

### 🔹 Safety Evaluation
- Hybrid **SafetyClassifier** combining:
  - Sentiment analysis (DistilBERT)
  - Rule-based toxicity detection
  - Misuse & jailbreak pattern detection
- Produces:
  - Safety score (0–1)
  - Risk label: **SAFE / WARNING / RISKY**
  - Human-readable explanation

### 🔹 Risk & Drift Metrics
- Daily safety summaries
- Weekly risk aggregation
- Monthly risk aggregation
- Enables longitudinal safety drift analysis

### 🔹 Reporting
- Static HTML dashboard
- Daily / Weekly / Monthly views
- Automatically published via GitHub Pages

### 🔹 Automation
All stages are automated using GitHub Actions:

- **Daily Collect** → fetch public data  
- **Daily Evaluate** → compute safety results  
- **Weekly Metrics** → aggregate trends  
- **Monthly Metrics** → long-term drift  
- **Report Build** → publish dashboard  

All artifacts are committed to the repository for transparency and reproducibility.

---

## 🏗 System Architecture

```mermaid
flowchart TD
    A["GitHub Actions (Scheduled and Manual Triggers)"]

    A --> B["Data Collectors
    - Google Trends (pytrends)
    - HackerNews API"]

    B --> C["Raw Data Storage
    data/live/raw/YYYY-MM-DD"]

    C --> D["Safety Evaluation Layer
    - Sentiment Analysis
    - Toxicity Detection
    - Misuse and Jailbreak Detection"]

    D --> E["Processed Data Storage
    data/live/processed/YYYY-MM-DD"]

    E --> F["Metrics and Drift Analysis
    - Daily Summaries
    - Weekly Aggregation
    - Monthly Aggregation"]

    F --> G["Reporting Layer
    Static HTML Dashboard"]

    G --> H["GitHub Pages
    Live Public Dashboard"]
