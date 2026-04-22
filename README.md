# Primetrade.ai — Data Science Hiring Assignment
**Candidate**: Aryan | **Submission Date**: April 2026

---

## Assignment Summary

Explore the relationship between **Hyperliquid trader performance** and the **Bitcoin Fear & Greed Index**, uncover hidden patterns, and deliver insights that drive smarter trading strategies.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the full analysis pipeline (generates all charts)
python notebooks/master_analysis.py

# 3. Open the notebook for step-by-step walkthrough
jupyter notebook notebooks/notebook_1.ipynb
```

---

## Project Structure

```
ds_aryan/
├── data/
│   ├── historical_data.csv         # Hyperliquid trade records (200K+ rows)
│   └── fear_greed_index.csv        # Bitcoin Fear & Greed Index (daily)
│
├── notebooks/
│   ├── notebook_1.ipynb            # ← Main deliverable: full analysis notebook
│   ├── master_analysis.py          # Pipeline engine (callable or standalone)
│   └── visualizer.py               # PrimetradeVisualizer class (9 charts)
│
├── outputs/                        # Auto-generated high-res PNGs (300 DPI)
│   ├── cumulative_pnl_pro.png
│   ├── pnl_distribution_regimes_pro.png
│   ├── size_heatmap_hourly_pro.png
│   ├── size_vs_sentiment_pro.png
│   ├── alpha_metrics_pro.png
│   ├── long_short_bias_pro.png
│   ├── leverage_distribution_pro.png
│   ├── leverage_performance_pro.png
│   └── programmatic_backtest_pro.png
│
├── reports/
│   └── executive_visual_report.md  # Full narrative + embedded charts
│
└── requirements.txt
```

---

## Key Findings

| # | Finding | Impact |
|---|---------|--------|
| 1 | Fear & Neutral regimes capture 65% of ecosystem alpha | Regime-gating drives smarter entries |
| 2 | Sortino Ratio is 3× more predictive than Win Rate | Reframe success metrics |
| 3 | Contrarian Long bias peaks at ~68% during Fear | Systematic contrarian signal |
| 4 | Programmatic sizing improves cumulative PnL by ~22% | Actionable alpha via F&G index |
| 5 | Extreme Greed entry = ~35% drop in avg profitability | Automated FOMO circuit breaker |

---

## Visual Gallery

All 9 institutional-grade charts are in `outputs/` and embedded in `reports/executive_visual_report.md`.

---

*Prepared for Primetrade.ai Hiring Review — Confidential*
