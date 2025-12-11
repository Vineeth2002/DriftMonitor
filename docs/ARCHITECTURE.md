
---

### File: `DriftMonitor/docs/ARCHITECTURE.md`
```markdown
# Architecture — DriftMonitor

This document explains the system architecture and component responsibilities.

## High-level components

[GitHub Actions] -> [Collectors] -> [Raw data (data/live/raw)] -> [Evaluation (SafetyClassifier)] -> [Processed data (data/live/processed)]
↳ [Metrics Runner (drift_summary)] -> [Report Builder] -> [docs/index.html] (GitHub Pages)

## Components

- **Collectors** (`collectors/`):
  - `google_trends` — pytrends (optional) + fallback
  - `hackernews` — public Firebase API
  - `template` — example/custom prompts collector
  - Design: small payloads, sample fallback, CLI interface

- **Benchmark** (`benchmark/`):
  - Model runners (transformers optional) with rule-based fallback
  - `SafetyClassifier` combines sentiment + toxicity heuristics to produce interpretable `safety_score`

- **Metrics** (`metrics/`):
  - Distributional drift: unigram distributions → Jensen–Shannon divergence (normalized)
  - Toxicity statistics: token/sub-string hits + batch summaries

- **Evaluation** (`scripts/evaluate/`):
  - Merge raw items → extract text fields → run safety classifier → write `eval_*.json`

- **Metrics Runner** (`scripts/metrics/`):
  - Compute drift & toxicity comparisons between two eval snapshots → write `drift_summary_*.json`

- **Reporting** (`report/`):
  - Jinja2 templates → static HTML `report.html` → copied to `docs/index.html` by workflow for GitHub Pages

- **Automation** (`.github/workflows/`):
  - `daily_collect.yml` — collects and commits raw data
  - `daily_evaluate.yml` — evaluates and commits processed outputs
  - `weekly_metrics.yml` — computes drift summary
  - `report_build.yml` — builds report and publishes to `docs/` branch (GitHub Pages)

## Data flow

1. Collectors run (daily/manual) and write timestamped JSON to `data/live/raw`.
2. Evaluation reads raw JSONs and writes `eval_<ts>.json` to `data/live/processed`.
3. Metrics runner compares latest evals and writes `drift_summary_<ts>.json` to `data/live/processed`.
4. Report builder reads latest processed + drift summary, renders HTML and copies to `docs/index.html`.
5. GitHub Pages serves `docs/index.html`.

## Design rationale

- **GitHub-only**: All compute fits into Actions; results are committed so the demo is reproducible.
- **Fallback-first**: Collectors include sample data so the pipeline never fails in demos.
- **Interpretable**: Safety scores, toxicity hits, and JSD are explainable to reviewers.
- **Lightweight**: Minimal external dependencies; transformers optional.


