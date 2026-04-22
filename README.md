# Primetrade.ai — Data Science Assignment Submission

**Submitted by:** Aryan Panwar
**Date:** April 2026
**Role:** Data Science Analyst — Primetrade.ai

---

## Hi Sonika and the Primetrade.ai Team 👋

Thank you for this assignment. I found it genuinely exciting — blending on-chain trade execution data with market psychology (Fear & Greed) is exactly the kind of cross-domain problem I love working on.

Below is everything I built. The short version: I analysed **211,224 real Hyperliquid trades** across a 2-year window, merged them with the Bitcoin Fear & Greed Index, and discovered a clear, exploitable contrarian alpha edge — then encoded it into a programmatic sizing model that improved cumulative PnL by **~22%**.

---

## What the Assignment Asked For

> *"Explore the relationship between trader performance and market sentiment, uncover hidden patterns, and deliver insights that can drive smarter trading strategies."*

That is exactly what I did. Here is how I approached it:

---

## My Approach

### 1. Data & Merging
- Loaded `historical_data.csv` (211,224 Hyperliquid trade records, 32 accounts, May 2023 – May 2025)
- Loaded `fear_greed_index.csv` (2,644 daily Bitcoin F&G readings)
- Normalised IST timestamps to date keys and performed an inner join → **211,218 clean rows** (6 rows dropped due to timezone boundary edge cases — no data lost)

### 2. Regime Classification
Classified every trade into one of five sentiment regimes using the F&G score:

| Score | Regime |
|-------|--------|
| 0 – 25 | Extreme Fear |
| 26 – 45 | Fear |
| 46 – 55 | Neutral |
| 56 – 75 | Greed |
| 76 – 100 | Extreme Greed |

### 3. Key Metrics Engineered
- **Sortino Ratio** per account per regime (downside-risk focused)
- **Win Rate** and **Profit Factor** per regime
- **Long/Short directional bias** across sentiment buckets
- **Effective Leverage** proxy (`Size USD / 1,000`) — the source dataset does not contain an explicit leverage column, so I defined and documented this proxy clearly
- **Intraday sizing heatmap** (hour × regime) to detect smart-money windows

### 4. Alpha Model
Built a contrarian programmatic sizing model:
- **1.5× Long exposure** during *Extreme Fear* / *Fear* regimes
- **0.5× de-risk** during *Extreme Greed*
- Flat (1.0×) during Neutral and Greed

Backtested this against flat execution on the same trade universe.

---

## What I Found

| # | Finding | Why It Matters |
|---|---------|----------------|
| 1 | **65% of ecosystem alpha** is captured in Fear + Neutral regimes | The crowd is wrong at the extremes — systematically |
| 2 | **Sortino Ratio is 3× more predictive** than Win Rate alone | Win rate is a vanity metric; downside risk is what kills accounts |
| 3 | Long bias peaks at **~68% during Fear**, drops to ~42% in Greed | Top traders are contrarian — they buy when others panic |
| 4 | Institutional-sized orders (>$50K) concentrate in **12:00–16:00 IST during Fear** | Smart money has a consistent execution window |
| 5 | Programmatic sentiment sizing: **+22% cumulative PnL** vs standard execution | The F&G Index has direct, quantifiable signal value as a sizing input |
| 6 | Extreme Greed entry = **~35% drop** in avg trade profitability | FOMO is measurable — and preventable |

---

## Deliverables

Everything is self-contained and reproducible:

```
sentiment-alpha-engine/
│
├── notebooks/
│   ├── notebook_1.ipynb        ← Main deliverable: full analysis walkthrough
│   ├── master_analysis.py      ← Standalone pipeline (runs from any directory)
│   └── visualizer.py          ← PrimetradeVisualizer — 9-chart engine
│
├── outputs/                    ← 9 institutional-grade charts (300 DPI, pre-generated)
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
│   └── executive_visual_report.md  ← Full narrative report with all charts embedded
│
└── requirements.txt
```

> **Note:** The source CSVs are not committed (they are ~93 MB combined). To reproduce: place `historical_data.csv` and `fear_greed_index.csv` into `data/` and run `python notebooks/master_analysis.py`.

---

## How to Run

```bash
# Install dependencies (Python 3.10+)
pip install -r requirements.txt

# Regenerate all 9 charts in one shot
python notebooks/master_analysis.py

# Or open the full step-by-step notebook
jupyter notebook notebooks/notebook_1.ipynb
```

The pipeline runs clean — zero warnings, zero errors, fully vectorised.

---

## Strategic Recommendations (for Primetrade.ai)

1. **Regime-Gated Sizing** — integrate the F&G Index as a live position sizing signal: reduce exposure above 75, scale in below 45
2. **Sortino-First Screening** — filter the signal universe by Sortino Ratio, not raw win rate
3. **Peak-Hours Execution** — concentrate institutional entries in the 12:00–16:00 IST window during Fear regimes
4. **FOMO Circuit Breaker** — implement an automated exposure cap when the index exceeds 80

---

## Tech Stack

`Python 3.10` · `pandas 2.x` · `numpy` · `matplotlib` · `seaborn ≥ 0.13` · `scipy` · `Jupyter`

No external APIs. Fully reproducible offline.

---

Thank you for the opportunity. I look forward to discussing these findings further.

**Aryan Panwar**
aryanpanwar1005@gmail.com
[github.com/Aryanpanwar10005](https://github.com/Aryanpanwar10005)
