#!/usr/bin/env python3
"""Generate additional PACT-NET plots incorporating MCC conditions.

Supplements the existing D0/D1-only plots with visualizations showing the
full defence stack: D0 → MCC_H → D1 → MCC_H+D1.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PLOT_DIR = ROOT / "plots"
SUMMARY_PATH = ROOT / "summary_mcc_h_mcc_h_d1_pact_net_v2.json"

# Colors
D0 = "#ef4444"
D1 = "#2563eb"
MCC_H = "#f59e0b"
MCC_HD1 = "#10b981"
GREY = "#94a3b8"
TEXT = "#111827"
MUTED = "#6b7280"
GRID = "#e5e7eb"
BG = "#fbfbfd"


def load_data() -> dict:
    with SUMMARY_PATH.open() as f:
        return json.load(f)["conditions"]


def pct(x: float) -> float:
    return 100 * x


def style_axis(ax: plt.Axes) -> None:
    ax.set_facecolor(BG)
    ax.grid(True, axis="y", color=GRID, linewidth=0.7, alpha=0.8)
    ax.grid(True, axis="x", color=GRID, linewidth=0.45, alpha=0.45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d1d5db")
    ax.spines["bottom"].set_color("#d1d5db")
    ax.tick_params(colors=TEXT, labelsize=9)


def save(fig: plt.Figure, name: str) -> None:
    for ext in ("pdf", "png"):
        fig.savefig(PLOT_DIR / f"{name}.{ext}", bbox_inches="tight", dpi=300)
    plt.close(fig)


def plot_defence_ladder_frontier(data: dict) -> None:
    """Safety-utility frontier with all 4 conditions."""
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    style_axis(ax)

    conditions = [
        ("D0", "D0\n(no policy)", D0, pct(data["D0"]["utility_score"]), pct(data["D0"]["safety_score"])),
        ("MCC_H", "MCC_H\n(structure only)", MCC_H, pct(data["MCC_H"]["utility_score"]), pct(data["MCC_H"]["safety_score"])),
        ("D1", "D1\n(policy only)", D1, pct(data["D1"]["utility_score"]), pct(data["D1"]["safety_score"])),
        ("MCC_H_D1", "MCC_H+D1\n(combined)", MCC_HD1, pct(data["MCC_H_D1"]["utility_score"]), pct(data["MCC_H_D1"]["safety_score"])),
    ]

    # Draw connecting lines (defence progression)
    xs = [c[3] for c in conditions]
    ys = [c[4] for c in conditions]

    for i in range(len(conditions) - 1):
        ax.plot([xs[i], xs[i+1]], [ys[i], ys[i+1]],
                color=GREY, lw=1.5, alpha=0.5, linestyle="--", zorder=1)

    for key, label, color, x, y in conditions:
        ax.scatter(x, y, s=300, color=color, edgecolor="white", linewidth=2.2, zorder=3)
        offset_x = 1.5 if key != "MCC_H" else -1.5
        offset_y = 2.5 if key != "D1" else -4.5
        ha = "left" if key != "MCC_H" else "right"
        ax.annotate(label, (x, y), xytext=(x + offset_x, y + offset_y),
                    fontsize=9.5, weight="bold", color=TEXT, ha=ha)

    # Annotate the key insight: MCC_H destroys utility
    ax.annotate(
        "MCC_H blocks ALL\nauthorized writes\n(0% create/complete)",
        xy=(pct(data["MCC_H"]["utility_score"]), pct(data["MCC_H"]["safety_score"])),
        xytext=(35, 55),
        arrowprops=dict(arrowstyle="->", color=MCC_H, lw=1.3),
        fontsize=8.5, color=MUTED,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#e5e7eb", alpha=0.95),
    )

    ax.set_xlabel("Utility score (%)", fontsize=11, color=TEXT)
    ax.set_ylabel("Safety score (%)", fontsize=11, color=TEXT)
    ax.set_title("PACT-NET defence ladder: structure + policy > either alone",
                 fontsize=14, weight="bold", color=TEXT, pad=14)
    ax.set_xlim(15, 95)
    ax.set_ylim(20, 85)

    ax.text(0.01, -0.14,
            "MCC_H achieves strong safety (64.4%) but catastrophic utility (23.1%) due to read-only scope blocking writes.\n"
            "Combined MCC_H+D1 reaches highest safety (77.8%) but inherits the utility penalty.",
            transform=ax.transAxes, fontsize=8.2, color=MUTED)

    save(fig, "pact_net_defence_ladder")


def plot_task_family_grouped_bar(data: dict) -> None:
    """Grouped bar chart showing accuracy by task family across conditions."""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    style_axis(ax)

    families = [
        ("Should-answer\n(utility)", "should_answer", "qa"),
        ("Should-refuse\n(security)", "should_refuse", "qa"),
        ("Transitive\nrisk", "transitive_risk", "qa"),
        ("Confused\ndeputy", "confused_deputy", "action"),
        ("Cross-surface\nplant", "cross_surface_plant", "action"),
        ("Non-contact\nprobe", "non_contact_probe", "qa"),
    ]

    conditions_order = [
        ("D0", D0),
        ("MCC_H", MCC_H),
        ("D1", D1),
        ("MCC_H+D1", MCC_HD1),
    ]
    cond_keys = ["D0", "MCC_H", "D1", "MCC_H_D1"]

    x = np.arange(len(families))
    width = 0.18
    offsets = [-1.5, -0.5, 0.5, 1.5]

    for i, (cond_label, color) in enumerate(conditions_order):
        cond_key = cond_keys[i]
        values = []
        for fname, key, surface in families:
            if surface == "qa":
                values.append(pct(data[cond_key]["qa_categories"][key]))
            else:
                values.append(pct(data[cond_key]["action_categories"][key]))

        bars = ax.bar(x + offsets[i] * width, values, width * 0.92,
                      color=color, alpha=0.85, label=cond_label, edgecolor="white", linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels([f[0] for f in families], fontsize=9.5)
    ax.set_ylabel("Correct response rate (%)", fontsize=11, color=TEXT)
    ax.set_ylim(0, 108)
    ax.set_title("Task family accuracy across the defence stack",
                 fontsize=14, weight="bold", color=TEXT, pad=14)
    ax.legend(loc="upper left", frameon=True, framealpha=0.95, fontsize=9)

    # Horizontal reference line at 100%
    ax.axhline(100, color=GREY, lw=0.8, ls=":", alpha=0.6)

    ax.text(0.01, -0.13,
            "Non-contact probe is infrastructure-enforced (100% all conditions). "
            "MCC_H blocks authorized writes (0% create). "
            "Combined MCC_H+D1 dominates on security families.",
            transform=ax.transAxes, fontsize=8.2, color=MUTED)

    save(fig, "pact_net_task_family_bar")


def plot_transitive_progression(data: dict) -> None:
    """Show how transitive leak rate declines across defence layers."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    style_axis(ax)

    conditions = ["D0", "MCC_H", "D1", "MCC_H_D1"]
    labels = ["D0\n(no defence)", "MCC_H\n(structure)", "D1\n(policy)", "MCC_H+D1\n(combined)"]
    colors = [D0, MCC_H, D1, MCC_HD1]
    T_values = [pct(data[c]["network_metrics"]["T_transitive_leak"]) for c in conditions]

    bars = ax.bar(range(len(conditions)), T_values, color=colors, alpha=0.85,
                  edgecolor="white", linewidth=1.5, width=0.65)

    for bar, val in zip(bars, T_values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=11, weight="bold", color=TEXT)

    ax.set_xticks(range(len(conditions)))
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel("Transitive leak rate $\\mathcal{T}$ (%)", fontsize=11, color=TEXT)
    ax.set_ylim(0, 108)
    ax.set_title("Transitive leakage remains the hardest network-scale problem",
                 fontsize=13.5, weight="bold", color=TEXT, pad=14)

    # Annotate the residual
    ax.axhline(67.0, color=MCC_HD1, lw=1.2, ls="--", alpha=0.5)
    ax.text(3.45, 68, "67% residual\neven with best\ndefence stack",
            fontsize=8.5, color=MUTED, va="bottom")

    ax.text(0.01, -0.15,
            "Transitive leakage resists all prompt+structural defences. "
            "Policy reduces it 19pp (D0→D1), structure adds 0pp (D1≈MCC_H), "
            "combined adds 11pp more (D1→MCC_H+D1).",
            transform=ax.transAxes, fontsize=8.2, color=MUTED)

    save(fig, "pact_net_transitive_progression")


def plot_network_metrics_radar(data: dict) -> None:
    """Spider/radar chart comparing network-specific metrics across conditions."""
    metrics = ["$\\mathcal{T}$ Transit.", "$\\mathcal{D}$ Deputy",
               "$\\mathcal{X}$ Cross-clust.", "$\\mathcal{A}$ Amplif."]

    # Normalize: for T, D, X lower is better (invert to "protection")
    # For A: 1.0 is perfect, higher is worse. Normalize as (2-A)/1 * 100
    def protection(cond):
        nm = data[cond]["network_metrics"]
        return [
            100 - pct(nm["T_transitive_leak"]),  # T: protection = 100 - leak
            100 - pct(nm["D_confused_deputy"]),   # D: protection = 100 - success
            100 - pct(nm["X_cross_cluster_leak"]),# X: protection = 100 - leak
            max(0, (2.0 - nm["A_amplification"]) * 100),  # A: normalized
        ]

    fig, ax = plt.subplots(figsize=(6.5, 6.5), subplot_kw=dict(polar=True))

    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]

    conditions_plot = [
        ("D0", D0, 1.5),
        ("MCC_H", MCC_H, 1.8),
        ("D1", D1, 2.0),
        ("MCC_H+D1", MCC_HD1, 2.2),
    ]
    cond_keys = ["D0", "MCC_H", "D1", "MCC_H_D1"]

    for i, (label, color, lw) in enumerate(conditions_plot):
        values = protection(cond_keys[i])
        values += values[:1]
        ax.plot(angles, values, color=color, lw=lw, alpha=0.85, label=label)
        ax.fill(angles, values, color=color, alpha=0.08)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=10.5, color=TEXT)
    ax.set_ylim(0, 105)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25%", "50%", "75%", "100%"], fontsize=8, color=MUTED)
    ax.legend(loc="lower right", bbox_to_anchor=(1.25, -0.05), frameon=True,
              framealpha=0.95, fontsize=9.5)
    ax.set_title("Network-metric protection by defence layer",
                 fontsize=14, weight="bold", color=TEXT, pad=20)

    save(fig, "pact_net_network_radar")


def plot_safety_utility_tradeoff_bar(data: dict) -> None:
    """Side-by-side safety vs utility for all 4 conditions — the key tradeoff visual."""
    fig, ax = plt.subplots(figsize=(8, 4.8))
    style_axis(ax)

    conditions = ["D0", "MCC_H", "D1", "MCC_H+D1"]
    cond_keys = ["D0", "MCC_H", "D1", "MCC_H_D1"]
    colors = [D0, MCC_H, D1, MCC_HD1]

    safety = [pct(data[k]["safety_score"]) for k in cond_keys]
    utility = [pct(data[k]["utility_score"]) for k in cond_keys]

    x = np.arange(len(conditions))
    width = 0.35

    bars_s = ax.bar(x - width/2, safety, width, color=colors, alpha=0.85,
                    edgecolor="white", linewidth=1.2, label="Safety")
    bars_u = ax.bar(x + width/2, utility, width, color=colors, alpha=0.4,
                    edgecolor=[c for c in colors], linewidth=1.5, label="Utility", hatch="//")

    for bar, val in zip(bars_s, safety):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f"{val:.1f}", ha="center", va="bottom", fontsize=9, weight="bold", color=TEXT)
    for bar, val in zip(bars_u, utility):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f"{val:.1f}", ha="center", va="bottom", fontsize=9, color=MUTED)

    ax.set_xticks(x)
    ax.set_xticklabels(conditions, fontsize=11)
    ax.set_ylabel("Score (%)", fontsize=11, color=TEXT)
    ax.set_ylim(0, 100)
    ax.set_title("Safety-utility tradeoff across defence conditions",
                 fontsize=14, weight="bold", color=TEXT, pad=14)

    # Custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=GREY, alpha=0.85, label="Safety (solid)"),
        Patch(facecolor=GREY, alpha=0.4, hatch="//", edgecolor=GREY, label="Utility (hatched)"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", frameon=True, framealpha=0.95, fontsize=9.5)

    ax.text(0.01, -0.13,
            "D1 achieves the best safety/utility ratio (4.6:1). "
            "MCC_H and MCC_H+D1 achieve higher safety but catastrophic utility due to read-only scope.",
            transform=ax.transAxes, fontsize=8.2, color=MUTED)

    save(fig, "pact_net_safety_utility_tradeoff")


def main() -> None:
    PLOT_DIR.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.titleweight": "bold",
        "axes.titlesize": 13,
        "axes.labelsize": 10,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    })

    data = load_data()

    plot_defence_ladder_frontier(data)
    plot_task_family_grouped_bar(data)
    plot_transitive_progression(data)
    plot_network_metrics_radar(data)
    plot_safety_utility_tradeoff_bar(data)

    print("Generated PACT-NET v2 plots (with MCC conditions) in", PLOT_DIR)


if __name__ == "__main__":
    main()
