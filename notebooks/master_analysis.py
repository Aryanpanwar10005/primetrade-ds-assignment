"""
master_analysis.py
==================
Primetrade.ai — Full Analysis Pipeline
Runs end-to-end: data ingestion -> preprocessing -> metric engineering -> visual export

Author: Aryan | Primetrade.ai Hiring Assignment
Usage:
    python master_analysis.py
    (or import run_full_analysis from a notebook cell)
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)

# -- Ensure local imports resolve regardless of CWD --------------------------─
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from visualizer import PrimetradeVisualizer


# -- Sentiment Categoriser ----------------------------------------------------─
def _categorize_sentiment(val: float) -> str:
    if val <= 25: return "Extreme Fear"
    if val <= 45: return "Fear"
    if val <= 55: return "Neutral"
    if val <= 75: return "Greed"
    return "Extreme Greed"


# -- Programmatic Alpha Multiplier --------------------------------------------─
def _alpha_multiplier(regime: str, side: str) -> float:
    """
    Contrarian position-sizing logic:
      • Fear / Extreme Fear + BUY  -> increase exposure 1.5×
      • Extreme Greed       + BUY  -> de-risk 0.5×
      • All others                  -> no change (1.0×)
    """
    if regime in ("Extreme Fear", "Fear") and side == "BUY":
        return 1.5
    if regime == "Extreme Greed" and side == "BUY":
        return 0.5
    return 1.0


# -- Main Pipeline ------------------------------------------------------------─
def run_full_analysis(data_dir: str = "../data", output_dir: str = "../outputs") -> dict:
    """
    Execute the complete Primetrade.ai analysis pipeline.

    Returns
    -------
    dict with keys: merged_df, account_stats
    """
    print("=" * 60)
    print("  Primetrade.ai  |  Professional Analysis Pipeline")
    print("=" * 60)

    # -- 1. Data Ingestion ----------------------------------------------------─
    print("\n[1/4] Loading datasets ...")
    trade_path     = os.path.join(data_dir, "historical_data.csv")
    sentiment_path = os.path.join(data_dir, "fear_greed_index.csv")

    trade_df     = pd.read_csv(trade_path, low_memory=False)
    sentiment_df = pd.read_csv(sentiment_path)

    print(f"      Trades loaded      : {len(trade_df):>10,}")
    print(f"      Sentiment days     : {len(sentiment_df):>10,}")

    # -- 2. Preprocessing & Merge ----------------------------------------------
    print("\n[2/4] Preprocessing & merging ...")

    # Parse timestamps
    trade_df["Timestamp IST"] = pd.to_datetime(
        trade_df["Timestamp IST"], format="%d-%m-%Y %H:%M", errors="coerce"
    )
    trade_df = trade_df.dropna(subset=["Timestamp IST"])
    trade_df["date_only"] = trade_df["Timestamp IST"].dt.date

    # Numeric coercion (no silent NaNs)
    trade_df["Closed PnL"] = pd.to_numeric(trade_df["Closed PnL"], errors="coerce").fillna(0)
    trade_df["Size USD"]   = pd.to_numeric(trade_df["Size USD"],   errors="coerce").fillna(0)

    # Sentiment regime labelling
    sentiment_df["date"]             = pd.to_datetime(sentiment_df["date"]).dt.date
    sentiment_df["sentiment_regime"] = sentiment_df["value"].apply(_categorize_sentiment)

    # Merge on date
    merged_df = pd.merge(
        trade_df,
        sentiment_df[["date", "value", "classification", "sentiment_regime"]],
        left_on="date_only", right_on="date",
        how="inner",
    )

    print(f"      Merged rows        : {len(merged_df):>10,}")
    print(f"      Unique accounts    : {merged_df['Account'].nunique():>10,}")
    print(f"      Date range         : {merged_df['Timestamp IST'].min().date()} -> "
          f"{merged_df['Timestamp IST'].max().date()}")

    # -- 3. Feature Engineering ------------------------------------------------
    print("\n[3/4] Engineering features ...")

    # Effective leverage proxy (no direct leverage column in source data)
    merged_df["leverage"] = merged_df["Size USD"] / 1_000

    merged_df["leverage_tier"] = pd.cut(
        merged_df["leverage"],
        bins=[0, 5, 20, np.inf],
        labels=["Low", "Medium", "High"],
        right=True,
    )

    merged_df["is_win"] = (merged_df["Closed PnL"] > 0).astype(int)

    # Vectorised alpha multiplier (faster than row-wise apply)
    conditions = [
        (merged_df["sentiment_regime"].isin(["Extreme Fear", "Fear"])) & (merged_df["Side"] == "BUY"),
        (merged_df["sentiment_regime"] == "Extreme Greed") & (merged_df["Side"] == "BUY"),
    ]
    choices = [1.5, 0.5]
    merged_df["alpha_multiplier"]  = np.select(conditions, choices, default=1.0)
    merged_df["programmatic_pnl"]  = merged_df["Closed PnL"] * merged_df["alpha_multiplier"]

    # -- Account-level KPIs ----------------------------------------------------
    agg = merged_df.groupby("Account").agg(
        total_pnl   =("Closed PnL",  "sum"),
        trade_count =("Closed PnL",  "count"),
        avg_pnl     =("Closed PnL",  "mean"),
        pnl_std     =("Closed PnL",  "std"),
        avg_size    =("Size USD",    "mean"),
        avg_sentiment=("value",      "mean"),
    )

    wins = (merged_df[merged_df["Closed PnL"] > 0]
            .groupby("Account")["Closed PnL"].count())
    agg["win_rate"] = (wins / agg["trade_count"]).fillna(0)

    downside_std = (merged_df[merged_df["Closed PnL"] < 0]
                    .groupby("Account")["Closed PnL"].std().fillna(1))
    agg["sortino_ratio"] = (agg["avg_pnl"] / downside_std).fillna(0)

    print(f"      Leverage tiers     : {dict(merged_df['leverage_tier'].value_counts())}")
    print(f"      Overall win-rate   : {merged_df['is_win'].mean() * 100:.1f}%")

    # -- 4. Visual Gallery ----------------------------------------------------─
    print("\n[4/4] Generating institutional visual gallery ...")
    viz = PrimetradeVisualizer(output_dir=output_dir)

    viz.plot_cumulative_pnl(merged_df)
    viz.plot_sentiment_regime_distribution(merged_df)
    viz.plot_execution_heatmap(merged_df)
    viz.plot_size_vs_sentiment_correlation(merged_df)
    viz.plot_alpha_metrics(agg)
    viz.plot_long_short_bias(merged_df)
    viz.plot_leverage_distribution(merged_df)
    viz.plot_leverage_performance(merged_df)
    viz.plot_programmatic_backtest(merged_df)

    print("\n" + "=" * 60)
    print("  [DONE]  Pipeline complete. Charts saved to:", os.path.abspath(output_dir))
    print("=" * 60)

    return {"merged_df": merged_df, "account_stats": agg}


# -- Entry Point --------------------------------------------------------------─
if __name__ == "__main__":
    # Resolve paths relative to this script so it runs correctly from any CWD
    _here = os.path.dirname(os.path.abspath(__file__))
    run_full_analysis(
        data_dir=os.path.join(_here, "..", "data"),
        output_dir=os.path.join(_here, "..", "outputs"),
    )
