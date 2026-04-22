"""
visualizer.py
=============
Primetrade.ai — Professional Visualization Engine
"Cyber-Dark" Institutional-Grade Plotting Suite

Author: Aryan | Primetrade.ai Hiring Assignment
"""

import os
import warnings

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

# Suppress seaborn FutureWarnings on palette deprecation
warnings.filterwarnings("ignore", category=FutureWarning)


class PrimetradeVisualizer:
    """
    Centralised plotting engine implementing the 'Primetrade Pro' Cyber-Dark aesthetic.
    All methods are self-contained, export high-DPI PNGs, and require no Kaleido dependency.
    """

    # -- Primetrade Pro Palette ------------------------------------------------
    BG      = "#0B0E11"   # Deep Space
    PANEL   = "#141A21"   # Card surface
    GRID    = "#2B2F36"   # Subtle grid lines
    BORDER  = "#2B2F36"   # Axis borders
    CYAN    = "#00FFD1"   # Primary accent
    PURPLE  = "#7000FF"   # Secondary accent
    GREEN   = "#02C076"   # Profit / Long
    GOLD    = "#F0B90B"   # Warning / Highlight
    RED     = "#CF304A"   # Loss / Short
    WHITE   = "#EAECEF"   # Primary text
    GRAY    = "#848E9C"   # Secondary text

    REGIME_ORDER = ["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"]
    REGIME_COLORS = {
        "Extreme Fear": "#CF304A",
        "Fear":         "#F0B90B",
        "Neutral":      "#848E9C",
        "Greed":        "#02C076",
        "Extreme Greed":"#00FFD1",
    }

    # -- Constructor -----------------------------------------------------------
    def __init__(self, output_dir: str = "../outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self._apply_global_style()

    # -- Global Matplotlib Style -----------------------------------------------
    def _apply_global_style(self):
        plt.rcParams.update({
            "figure.facecolor":    self.BG,
            "axes.facecolor":      self.BG,
            "axes.edgecolor":      self.BORDER,
            "axes.labelcolor":     self.GRAY,
            "axes.titlecolor":     self.WHITE,
            "axes.grid":           True,
            "grid.color":          self.GRID,
            "grid.linestyle":      "--",
            "grid.alpha":          0.35,
            "text.color":          self.WHITE,
            "xtick.color":         self.GRAY,
            "ytick.color":         self.GRAY,
            "font.family":         "sans-serif",
            "font.size":           11,
            "axes.spines.top":     False,
            "axes.spines.right":   False,
            "axes.spines.left":    True,
            "axes.spines.bottom":  True,
            "figure.dpi":          150,
            "savefig.dpi":         300,
            "savefig.bbox":        "tight",
            "savefig.facecolor":   self.BG,
            "legend.frameon":      False,
            "legend.labelcolor":   self.WHITE,
        })

    # -- Internal Helpers ------------------------------------------------------
    def _save(self, fig, filename: str):
        path = os.path.join(self.output_dir, filename)
        fig.savefig(path)
        plt.close(fig)
        print(f"  [OK] Exported -> {filename}")

    def _styled_fig(self, figsize=(14, 7)):
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor(self.BG)
        ax.set_facecolor(self.BG)
        return fig, ax

    def _title(self, ax, title: str, subtitle: str = ""):
        ax.set_title(title, fontsize=16, fontweight="bold", color=self.WHITE, pad=14)
        if subtitle:
            ax.annotate(subtitle, xy=(0.5, 1.01), xycoords="axes fraction",
                        ha="center", fontsize=9, color=self.GRAY)

    def _watermark(self, fig):
        fig.text(0.99, 0.01, "(c) Primetrade.ai", fontsize=7,
                 color=self.GRAY, ha="right", va="bottom", alpha=0.6)

    # =========================================================================
    # Chart 1 — Cumulative PnL
    # =========================================================================
    def plot_cumulative_pnl(self, df: pd.DataFrame, filename: str = "cumulative_pnl_pro.png"):
        """Aggregate equity curve with sentiment-shaded backgrounds."""
        df = df.sort_values("Timestamp IST").copy()
        df["cum_pnl"] = df["Closed PnL"].cumsum()

        fig, ax = self._styled_fig((14, 7))

        # Regime background bands
        regime_map = df.set_index("Timestamp IST")["sentiment_regime"]
        prev_regime = None
        band_start = df["Timestamp IST"].iloc[0]
        times = df["Timestamp IST"].values

        for i, (ts, regime) in enumerate(zip(df["Timestamp IST"], df["sentiment_regime"])):
            if regime != prev_regime:
                if prev_regime is not None:
                    ax.axvspan(band_start, ts,
                               color=self.REGIME_COLORS.get(prev_regime, self.GRAY),
                               alpha=0.05)
                band_start = ts
                prev_regime = regime
        ax.axvspan(band_start, df["Timestamp IST"].iloc[-1],
                   color=self.REGIME_COLORS.get(prev_regime, self.GRAY), alpha=0.05)

        # Fill area
        ax.fill_between(df["Timestamp IST"], df["cum_pnl"],
                        color=self.CYAN, alpha=0.08)

        # Main line
        ax.plot(df["Timestamp IST"], df["cum_pnl"],
                color=self.CYAN, linewidth=2, label="Ecosystem Cumulative PnL", zorder=5)

        # Zero line
        ax.axhline(0, color=self.WHITE, linestyle="--", linewidth=0.8, alpha=0.4)

        self._title(ax, "INSTITUTIONAL EQUITY CURVE: AGGREGATE ALPHA CAPTURE",
                    "Sentiment regime bands overlaid · Cyan = Ecosystem PnL")
        ax.set_xlabel("Execution Timeline", fontsize=11)
        ax.set_ylabel("Cumulative Profit / Loss (USD)", fontsize=11)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax.legend(fontsize=10)
        self._watermark(fig)
        self._save(fig, filename)

    # =========================================================================
    # Chart 2 — Regime PnL Distribution (Violin)
    # =========================================================================
    def plot_sentiment_regime_distribution(self, df: pd.DataFrame,
                                           filename: str = "pnl_distribution_regimes_pro.png"):
        """Per-regime PnL density — violin + inner quartile lines."""
        q_low  = df["Closed PnL"].quantile(0.01)
        q_high = df["Closed PnL"].quantile(0.99)
        fdf = df[(df["Closed PnL"] > q_low) & (df["Closed PnL"] < q_high)].copy()

        palette = {r: self.REGIME_COLORS[r] for r in self.REGIME_ORDER if r in fdf["sentiment_regime"].unique()}

        fig, ax = self._styled_fig((14, 8))

        sns.violinplot(
            data=fdf, x="sentiment_regime", y="Closed PnL",
            order=[r for r in self.REGIME_ORDER if r in fdf["sentiment_regime"].unique()],
            hue="sentiment_regime",
            palette=palette,
            inner="quartile",
            linewidth=1.2,
            legend=False,
            ax=ax,
        )

        ax.axhline(0, color=self.WHITE, linestyle="--", linewidth=0.9, alpha=0.5)
        self._title(ax, "REGIME-AWARE PROFITABILITY DENSITY",
                    "1st–99th percentile trimmed · Quartile lines inside violins")
        ax.set_xlabel("Market Sentiment Regime", fontsize=11)
        ax.set_ylabel("Closed PnL Distribution (USD)", fontsize=11)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        self._watermark(fig)
        self._save(fig, filename)

    # =========================================================================
    # Chart 3 — Execution Intensity Heatmap
    # =========================================================================
    def plot_execution_heatmap(self, df: pd.DataFrame,
                               filename: str = "size_heatmap_hourly_pro.png"):
        """Mean trade size by sentiment regime × hour-of-day."""
        df = df.copy()
        df["hour"] = pd.to_datetime(df["Timestamp IST"]).dt.hour

        pivot = (df.pivot_table(index="sentiment_regime", columns="hour",
                                values="Size USD", aggfunc="mean")
                   .reindex([r for r in self.REGIME_ORDER if r in df["sentiment_regime"].unique()]))

        fig, ax = self._styled_fig((16, 6))

        sns.heatmap(
            pivot, cmap="magma", annot=False,
            linewidths=0.4, linecolor=self.BG,
            cbar_kws={"label": "Mean Size (USD)", "shrink": 0.75},
            ax=ax,
        )
        ax.collections[0].colorbar.ax.yaxis.label.set_color(self.GRAY)
        ax.collections[0].colorbar.ax.tick_params(colors=self.GRAY)

        self._title(ax, "EXECUTION INTENSITY MATRIX: LIQUIDITY CONCENTRATION BY REGIME",
                    "Rows = Sentiment Regime · Columns = Hour of Day (IST)")
        ax.set_xlabel("Hour of Day (IST)", fontsize=11)
        ax.set_ylabel("Sentiment Regime", fontsize=11)
        self._watermark(fig)
        self._save(fig, filename)

    # =========================================================================
    # Chart 4 — Sentiment vs Position Size (Joint)
    # =========================================================================
    def plot_size_vs_sentiment_correlation(self, df: pd.DataFrame,
                                           filename: str = "size_vs_sentiment_pro.png"):
        """Scatter + regression + marginal histograms."""
        sample = df.sample(min(len(df), 5_000), random_state=42)

        fig = plt.figure(figsize=(12, 10))
        fig.patch.set_facecolor(self.BG)

        g = sns.JointGrid(data=sample, x="value", y="Size USD", space=0)
        g.fig.patch.set_facecolor(self.BG)
        g.ax_joint.set_facecolor(self.BG)
        g.ax_marg_x.set_facecolor(self.BG)
        g.ax_marg_y.set_facecolor(self.BG)

        g.plot_joint(sns.regplot,
                     scatter_kws={"alpha": 0.25, "color": self.CYAN, "s": 8},
                     line_kws={"color": self.GOLD, "linewidth": 2})
        g.plot_marginals(sns.histplot, color=self.PURPLE, alpha=0.6, kde=True)

        g.ax_joint.set_xlabel("Fear & Greed Index Score (0=Fear · 100=Greed)", fontsize=11)
        g.ax_joint.set_ylabel("Execution Size (USD)", fontsize=11)
        g.ax_joint.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

        g.fig.suptitle("SENTIMENT–SIZE CORRELATION: DETECTING PRO-CYCLICAL BIAS",
                       fontsize=15, fontweight="bold", color=self.WHITE, y=1.01)
        g.fig.text(0.99, 0.01, "(c) Primetrade.ai", fontsize=7,
                   color=self.GRAY, ha="right", va="bottom", alpha=0.6)

        path = os.path.join(self.output_dir, filename)
        g.fig.savefig(path, bbox_inches="tight", dpi=300, facecolor=self.BG)
        plt.close(g.fig)
        print(f"  [OK] Exported -> {filename}")

    # =========================================================================
    # Chart 5 — Alpha Metric Clustering (Bubble)
    # =========================================================================
    def plot_alpha_metrics(self, account_stats: pd.DataFrame,
                           filename: str = "alpha_metrics_pro.png"):
        """Bubble chart: Win Rate vs Sortino Ratio, sized by |total_pnl|."""
        fig, ax = self._styled_fig((14, 8))

        size = np.sqrt(np.abs(account_stats["total_pnl"])).clip(lower=5) / 1.5

        sc = ax.scatter(
            account_stats["win_rate"] * 100,
            account_stats["sortino_ratio"],
            s=size,
            c=account_stats["total_pnl"],
            cmap="RdYlGn",
            alpha=0.75,
            edgecolors=self.WHITE,
            linewidth=0.4,
            zorder=5,
        )

        cbar = fig.colorbar(sc, ax=ax, shrink=0.75)
        cbar.set_label("Total PnL (USD)", fontsize=10, color=self.GRAY)
        cbar.ax.tick_params(colors=self.GRAY)

        # Quadrant lines
        ax.axvline(50, color=self.GRAY, linestyle="--", linewidth=0.8, alpha=0.5)
        ax.axhline(0,  color=self.GRAY, linestyle="--", linewidth=0.8, alpha=0.5)

        self._title(ax, "ALPHA DISCOVERY: WIN RATE vs RISK-ADJUSTED RETURN",
                    "Bubble size = |Total PnL| · Colour = Profit (green) / Loss (red)")
        ax.set_xlabel("Win Rate (%)", fontsize=11)
        ax.set_ylabel("Sortino Ratio (Risk-Adjusted)", fontsize=11)
        self._watermark(fig)
        self._save(fig, filename)

    # =========================================================================
    # Chart 6 — Long / Short Bias by Regime
    # =========================================================================
    def plot_long_short_bias(self, df: pd.DataFrame,
                             filename: str = "long_short_bias_pro.png"):
        """Grouped bar: BUY vs SELL count per sentiment regime."""
        valid = [r for r in self.REGIME_ORDER if r in df["sentiment_regime"].unique()]
        bias = (df.groupby(["sentiment_regime", "Side"])
                  .size().unstack(fill_value=0)
                  .reindex(valid))

        fig, ax = self._styled_fig((14, 7))
        x = np.arange(len(bias))
        w = 0.38
        sides = bias.columns.tolist()
        colors = {"BUY": self.GREEN, "SELL": self.RED}

        for i, side in enumerate(sides):
            offset = (i - 0.5) * w
            bars = ax.bar(x + offset, bias[side], width=w,
                          color=colors.get(side, self.GRAY),
                          alpha=0.85, label=side, zorder=5)
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, h + h * 0.015,
                        f"{h:,.0f}", ha="center", va="bottom",
                        fontsize=8, color=self.WHITE)

        ax.set_xticks(x)
        ax.set_xticklabels(valid, rotation=0)
        ax.legend(["LONG (BUY)", "SHORT (SELL)"], fontsize=10)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
        self._title(ax, "CONTRARIAN ANALYSIS: LONG / SHORT BIAS BY SENTIMENT REGIME",
                    "Green = BUY (Long) · Red = SELL (Short)")
        ax.set_xlabel("Market Sentiment Regime", fontsize=11)
        ax.set_ylabel("Trade Count", fontsize=11)
        self._watermark(fig)
        self._save(fig, filename)

    # =========================================================================
    # Chart 7 — Average Effective Leverage by Regime
    # =========================================================================
    def plot_leverage_distribution(self, df: pd.DataFrame,
                                   filename: str = "leverage_distribution_pro.png"):
        """Bar chart: mean effective leverage (size proxy) per regime."""
        valid = [r for r in self.REGIME_ORDER if r in df["sentiment_regime"].unique()]
        avg_lev = df.groupby("sentiment_regime")["leverage"].mean().reindex(valid)

        fig, ax = self._styled_fig((12, 6))
        pal = [self.REGIME_COLORS[r] for r in valid]
        bars = ax.bar(avg_lev.index, avg_lev.values, color=pal, alpha=0.85, zorder=5)

        for bar, val in zip(bars, avg_lev.values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    val + val * 0.015,
                    f"{val:.1f}×", ha="center", va="bottom",
                    fontsize=10, color=self.WHITE, fontweight="bold")

        self._title(ax, "RISK PROFILE: EFFECTIVE LEVERAGE ACROSS SENTIMENT REGIMES",
                    "Leverage proxy = Size USD / $1 000 · higher = more capital at risk")
        ax.set_xlabel("Market Sentiment Regime", fontsize=11)
        ax.set_ylabel("Avg Effective Leverage (×)", fontsize=11)
        self._watermark(fig)
        self._save(fig, filename)

    # =========================================================================
    # Chart 8 — Leverage Tier vs PnL & Win Rate (Dual-Axis)
    # =========================================================================
    def plot_leverage_performance(self, df: pd.DataFrame,
                                  filename: str = "leverage_performance_pro.png"):
        """Dual-axis: leverage tier -> avg PnL bars + win-rate line."""
        order = ["Low", "Medium", "High"]
        valid = [t for t in order if t in df["leverage_tier"].unique()]
        stats = (df.groupby("leverage_tier")
                   .agg(avg_pnl=("Closed PnL", "mean"),
                        win_rate=("is_win", "mean"))
                   .reindex(valid))

        fig, ax1 = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(self.BG)
        ax1.set_facecolor(self.BG)

        bars = ax1.bar(stats.index, stats["avg_pnl"],
                       color=self.GOLD, alpha=0.8, zorder=5, label="Avg PnL")
        ax1.set_xlabel("Leverage Tier", fontsize=11)
        ax1.set_ylabel("Average PnL per Trade (USD)", fontsize=11, color=self.GOLD)
        ax1.tick_params(axis="y", labelcolor=self.GOLD)
        ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.set_facecolor(self.BG)
        ax1.tick_params(colors=self.GRAY)
        ax1.xaxis.label.set_color(self.GRAY)

        ax2 = ax1.twinx()
        ax2.plot(stats.index, stats["win_rate"] * 100,
                 color=self.CYAN, marker="o", linewidth=2.5,
                 markersize=10, label="Win Rate %", zorder=6)
        ax2.set_ylabel("Win Rate (%)", fontsize=11, color=self.CYAN)
        ax2.tick_params(axis="y", labelcolor=self.CYAN)
        ax2.set_ylim(0, 100)
        ax2.set_facecolor(self.BG)

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2,
                   loc="upper right", fontsize=10, frameon=False,
                   labelcolor=self.WHITE)

        ax1.set_title("LEVERAGE OPTIMIZATION: RISK–RETURN TRADEOFF",
                      fontsize=15, fontweight="bold", color=self.WHITE, pad=14)
        ax1.grid(True, color=self.GRID, linestyle="--", alpha=0.35)
        fig.text(0.99, 0.01, "(c) Primetrade.ai", fontsize=7,
                 color=self.GRAY, ha="right", va="bottom", alpha=0.6)
        self._save(fig, filename)

    # =========================================================================
    # Chart 9 — Programmatic Alpha Backtest
    # =========================================================================
    def plot_programmatic_backtest(self, df: pd.DataFrame,
                                   filename: str = "programmatic_backtest_pro.png"):
        """Equity curve: standard execution vs sentiment-optimised sizing."""
        df = df.sort_values("Timestamp IST").copy()
        df["cum_std"] = df["Closed PnL"].cumsum()
        df["cum_opt"] = df["programmatic_pnl"].cumsum()

        fig, ax = self._styled_fig((14, 7))

        ax.plot(df["Timestamp IST"], df["cum_std"],
                color=self.GRAY, linestyle="--", linewidth=1.2,
                label="Standard Execution", alpha=0.65)
        ax.plot(df["Timestamp IST"], df["cum_opt"],
                color=self.CYAN, linewidth=2.5,
                label="Sentiment-Optimised (Programmatic)")

        ax.fill_between(df["Timestamp IST"], df["cum_opt"], df["cum_std"],
                        where=(df["cum_opt"] > df["cum_std"]),
                        color=self.GREEN, alpha=0.12, interpolate=True,
                        label="Alpha Gain")

        ax.axhline(0, color=self.WHITE, linestyle="--", linewidth=0.7, alpha=0.4)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

        # Annotation box
        final_std = df["cum_std"].iloc[-1]
        final_opt = df["cum_opt"].iloc[-1]
        if final_std != 0:
            uplift = (final_opt - final_std) / abs(final_std) * 100
            ax.annotate(f"Programmatic Alpha: {uplift:+.1f}%",
                        xy=(0.97, 0.06), xycoords="axes fraction",
                        ha="right", fontsize=11, color=self.CYAN,
                        fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.3",
                                  fc=self.PANEL, ec=self.CYAN, alpha=0.85))

        self._title(ax, "STRATEGIC ALPHA: SENTIMENT-AWARE POSITION SIZING BACKTEST",
                    "1.5× Long in Fear · 0.5× de-risk in Extreme Greed")
        ax.set_xlabel("Execution Timeline", fontsize=11)
        ax.set_ylabel("Cumulative Profit / Loss (USD)", fontsize=11)
        ax.legend(fontsize=10)
        self._watermark(fig)
        self._save(fig, filename)
