# Executive Visual Intelligence Report
**Primetrade.ai Hiring Assignment** · Prepared by Aryan · April 2026

---

> **Direct Answer:** Analysis of 200K+ Hyperliquid trades merged with the Bitcoin Fear & Greed Index reveals that top-performing accounts exhibit "Sentiment Resilience" — consistent sizing regardless of market emotion — while retail flow over-levers into Extreme Greed. A contrarian programmatic model improves cumulative PnL by ~22%.

---

## 1. Executive Summary

This report presents findings from a deep-dive analysis of Hyperliquid trade flows correlated with Bitcoin market sentiment. We identify a significant relationship between **Sentiment Regimes** and **Execution Quality**, revealing a distinct *Performance Decay* during extreme market exuberance and a *Contrarian Alpha Edge* exploited by top-tier accounts.

**TL;DR — Key Findings**
- 📈 **65%** of total ecosystem alpha is captured during *Fear* and *Neutral* regimes
- 🎯 **Sortino Ratio** is a 3× stronger predictor of survivability than win rate alone
- 🔄 **Contrarian bias**: Long positioning peaks at ~68% during *Fear*, drops to ~42% in *Greed*
- ⚡ Programmatic sentiment-aware sizing delivers **+22% cumulative PnL** vs. standard execution
- ⚠️ *Extreme Greed* entry correlates with a **~35% drop** in average trade profitability

---

## 2. Methodology

| Step | Detail |
|------|--------|
| **Dataset** | 200,000+ Hyperliquid execution records + Bitcoin Fear & Greed Index (daily) |
| **Merge** | Inner join on date; IST timestamps normalised to date keys |
| **Regime Bins** | Extreme Fear (0–25) · Fear (26–45) · Neutral (46–55) · Greed (56–75) · Extreme Greed (76–100) |
| **Risk Metrics** | Sortino Ratio (downside deviation focus), Win Rate, Profit Factor |
| **Alpha Model** | Contrarian position sizing: 1.5× Long in Fear · 0.5× de-risk in Extreme Greed |

---

## 3. Institutional Equity Curve

Aggregate cumulative PnL shows robust ecosystem growth with visible regime-shift volatility. Sentiment background bands make regime transitions immediately actionable for systematic strategies.

![Institutional Equity Curve](../outputs/cumulative_pnl_pro.png)

---

## 4. Regime-Aware Profitability Density

PnL variance shifts dramatically across regimes. *Extreme Fear* shows wide loss tails (Revenge Trading); *Neutral* offers the most predictable execution environment.

![Regime Profitability Density](../outputs/pnl_distribution_regimes_pro.png)

---

## 5. Execution Intensity Matrix

Institutional-sized orders (>$50k USD) concentrate in the **12:00–16:00 IST** window during *Fear* regimes — a clear smart-money accumulation signal.

![Execution Intensity Heatmap](../outputs/size_heatmap_hourly_pro.png)

---

## 6. Sentiment–Size Correlation (FOMO Detection)

As the Fear & Greed Index climbs above 80, execution sizes increase exponentially — confirming **Pro-Cyclical Bias** that precedes the observed *Performance Dip* as liquidity exits into retail FOMO.

![Sentiment-Size Correlation](../outputs/size_vs_sentiment_pro.png)

---

## 7. Alpha Metric Clustering

Clustering accounts by Win Rate and Sortino Ratio isolates the *Professional Edge*. The high-alpha quadrant (top-right) is characterised by high risk-adjusted returns with execution independent of market noise.

![Alpha Metric Clustering](../outputs/alpha_metrics_pro.png)

---

## 8. Contrarian Analysis — Long / Short Bias

Long positioning is significantly elevated during *Fear* (~68%) and reaches its lowest point (~42%) during *Greed* regimes. The ecosystem's top performers systematically **trade against the crowd**.

![Long/Short Bias](../outputs/long_short_bias_pro.png)

---

## 9. Leverage Optimization — Risk–Return Tradeoff

The leverage–performance relationship is **non-linear**. *High Leverage* (>20×) captures higher nominal PnL but with a Win Rate nearly 30% lower than the *Low* tier (1–5×). Peak risk-adjusted efficiency sits in the 5–20× band.

![Leverage Distribution](../outputs/leverage_distribution_pro.png)

![Leverage Tier Performance](../outputs/leverage_performance_pro.png)

---

## 10. Strategic Alpha — Programmatic Sizing Model

A sentiment-aware execution strategy — **1.5× Long exposure in Fear, 0.5× de-risk in Extreme Greed** — outperformed flat execution by **~22%** with a materially smoother equity curve and reduced maximum drawdown. This heuristic demonstrates the direct signal value of the Fear & Greed Index as a real-time position sizing input.

![Programmatic Alpha Backtest](../outputs/programmatic_backtest_pro.png)

---

## 11. Strategic Recommendations

1. **Regime-Gated Sizing**: Integrate the Fear & Greed Index as a live sizing signal — reduce exposure above 75, increase below 45.
2. **Sortino-First Screening**: Filter signal universe by Sortino Ratio, not raw win rate, to identify survivable accounts.
3. **Peak-Hours Execution**: Concentrate institutional entries in the 12:00–16:00 IST window during *Fear* regimes.
4. **FOMO Circuit Breaker**: Implement an automated exposure cap when the index exceeds 80, preventing retail-correlated drawdowns.

---

*Confidential — Prepared for Primetrade.ai Hiring Review*
