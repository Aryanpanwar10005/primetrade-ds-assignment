# Sentiment Alpha Engine

> **Institutional-grade analysis of Hyperliquid perpetual trader performance across Bitcoin Fear & Greed sentiment regimes.**
> Contrarian signal detection · Leverage risk profiling · Programmatic alpha sizing

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-11557c?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-00d4a0?style=flat-square)

---

## Overview

This project analyses **211,224 real trades** from Hyperliquid — one of the largest on-chain perpetual exchanges — merged with the **Bitcoin Fear & Greed Index** across a 2-year window (May 2023 – May 2025).

The core question: *does crowd sentiment predict alpha, and can we systematically exploit it?*

The answer is yes. By classifying each trade into one of five market regimes — `Extreme Fear`, `Fear`, `Neutral`, `Greed`, `Extreme Greed` — the analysis surfaces a clear contrarian edge: **65% of ecosystem alpha is captured in Fear and Neutral regimes**, while Extreme Greed entries carry a ~35% penalty to average profitability.

---

## Key Findings

| # | Finding | Signal |
|---|---------|--------|
| 1 | Fear + Neutral regimes capture **65% of ecosystem alpha** | Regime-gating drives smarter entries |
| 2 | Sortino Ratio is **3× more predictive** than win rate alone | Reframe how performance is measured |
| 3 | Contrarian long bias peaks at **~68% during Fear** | Systematic, repeatable alpha signal |
| 4 | Programmatic sentiment-aware sizing: **+22% cumulative PnL** | Actionable edge from the F&G index |
| 5 | Extreme Greed entry = **~35% drop** in avg trade profitability | Automated FOMO circuit breaker |

---

## Visual Gallery

All 9 institutional-grade charts are pre-generated in `outputs/` at 300 DPI.

| Chart | Description |
|-------|-------------|
| `cumulative_pnl_pro.png` | Equity curve with regime background shading |
| `pnl_distribution_regimes_pro.png` | PnL distribution across all 5 regimes |
| `alpha_metrics_pro.png` | Win rate, Sharpe, Sortino per regime |
| `long_short_bias_pro.png` | Long/short directional bias by sentiment |
| `size_vs_sentiment_pro.png` | Position sizing behaviour per regime |
| `size_heatmap_hourly_pro.png` | Intraday sizing heatmap (hour × regime) |
| `leverage_distribution_pro.png` | Effective leverage tier breakdown |
| `leverage_performance_pro.png` | Risk-return tradeoff by leverage tier |
| `programmatic_backtest_pro.png` | Sentiment-aware sizing vs standard execution |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Aryanpanwar10005/sentiment-alpha-engine.git
cd sentiment-alpha-engine

# 2. Install dependencies (Python 3.10+)
pip install -r requirements.txt

# 3. Add data files to data/ (see Data section below)

# 4. Run the full analysis — regenerates all 9 charts
python notebooks/master_analysis.py

# 5. Open the notebook for the full step-by-step walkthrough
jupyter notebook notebooks/notebook_1.ipynb
```

---

## Project Structure

```
sentiment-alpha-engine/
│
├── data/                               # Source datasets (not committed — see below)
│   ├── historical_data.csv             # Hyperliquid trade records  (211K rows)
│   └── fear_greed_index.csv            # Bitcoin F&G Index          (daily, 2644 days)
│
├── notebooks/
│   ├── notebook_1.ipynb                # Main deliverable: end-to-end walkthrough
│   ├── master_analysis.py              # Standalone pipeline — path-safe, callable
│   └── visualizer.py                  # PrimetradeVisualizer — 9-chart Cyber-Dark engine
│
├── outputs/                            # Pre-generated 300 DPI institutional charts
│   └── *_pro.png                       # 9 charts (ready to embed in any report)
│
├── reports/
│   └── executive_visual_report.md      # Full narrative report with embedded visuals
│
├── requirements.txt
└── README.md
```

---

## Data

The source CSV files are not committed to this repo (combined ~93 MB). Place them in the `data/` directory before running the pipeline:

| File | Description | Rows |
|------|-------------|------|
| `historical_data.csv` | Hyperliquid perpetual trade records | 211,224 |
| `fear_greed_index.csv` | Daily Bitcoin Fear & Greed Index (0–100) | 2,644 |

The pipeline performs an automatic date-keyed merge, coerces all numeric columns, and flags any data integrity issues at load time.

---

## Methodology

| Step | Technique |
|------|-----------|
| **Regime classification** | `pd.cut` into 5 buckets: Extreme Fear / Fear / Neutral / Greed / Extreme Greed |
| **Alpha sizing** | Vectorised `np.select`: 1.5× long in Fear, 0.5× in Extreme Greed |
| **Risk metrics** | Sharpe, Sortino, Win Rate, Avg PnL per regime (32 accounts) |
| **Leverage proxy** | `Effective Leverage = Size USD / 1,000` (no direct leverage column in source) |
| **Visualisation** | Bespoke `PrimetradeVisualizer` — Matplotlib Cyber-Dark palette, 300 DPI |

---

## Tech Stack

- **Python 3.10+** · `pandas 2.x` · `numpy` · `matplotlib` · `seaborn ≥ 0.13` · `scipy`
- **Jupyter** for the interactive walkthrough
- Zero external API calls — fully reproducible offline

---

## Reports

The complete narrative is in [`reports/executive_visual_report.md`](reports/executive_visual_report.md), which includes:
- Direct Answer Block summary
- Methodology table
- Per-regime alpha breakdown
- Strategic recommendations for a programmatic execution layer

---

*Submission for Primetrade.ai Data Science Role — Aryan Panwar · April 2026*
