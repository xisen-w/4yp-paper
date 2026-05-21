#!/usr/bin/env python3
"""Generate PACT-NET thesis figures (P0 vs P1 only).

Plots match Chapter 5 (PACT-NET: Network Evaluation) exactly.
The chapter uses P0/P1 notation (not D0/D1) to avoid confusion with PACT-PAIR.
All plots focus on the bimodal policy effectiveness story:
  - Policy crushes bilateral threats (should_refuse, confused_deputy, cross_surface_plant)
  - Policy barely touches network-native threats (transitive, cross_cluster, amplification)

Nature-figure style: Arial, no top/right spines, 7pt base, editable SVG text.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
PLOT_DIR = ROOT / "plots"
SUMMARY_PATH = ROOT / "summary_mcc_h_mcc_h_d1_pact_net_v2.json"

# ─── Nature-figure mandatory rules ───────────────────────────────────────────
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['font.size'] = 7
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['legend.frameon'] = False

DPI = 600

# ─── Unified palette (matches arch + escalation scripts) ─────────────────────
P0_COLOR = "#B64342"      # red — no policy (danger)
P1_COLOR = "#0F4D92"      # navy — with policy (improved)
BILATERAL = "#42949E"     # teal — policy-responsive threats
NETWORK = "#E28E2C"       # gold/orange — policy-resistant (network-native)
STRUCTURAL = "#767676"    # neutral grey — infrastructure guarantee
UTILITY_C = "#E28E2C"    # gold — utility metrics
C_DELTA_UP = "#2E9E44"
C_DELTA_DOWN = "#B64342"
C_NEUTRAL = "#D8D8D8"


def pct(x: float) -> float:
    return 100 * x


def load_data() -> dict[str, dict]:
    with SUMMARY_PATH.open() as f:
        conditions = json.load(f)["conditions"]
    return {"P0": conditions["D0"], "P1": conditions["D1"]}


def add_panel_label(ax, label, x=-0.08, y=1.05):
    ax.text(x, y, label, transform=ax.transAxes, fontsize=9,
            fontweight='bold', ha='left', va='bottom')


def save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout(pad=1.5)
    for ext in ("svg", "pdf", "png"):
        fig.savefig(PLOT_DIR / f"{name}.{ext}", bbox_inches="tight", dpi=DPI)
    plt.close(fig)
    print(f"  saved: {name}")


# =========================================================================
# Plot 1: Security-Utility Frontier (P0 → P1 movement)
# =========================================================================
def plot_frontier(data: dict) -> None:
    """Two-point frontier showing the 4.6:1 safety/utility tradeoff."""
    fig, ax = plt.subplots(figsize=(3.5, 3.0))

    p0_util = pct(data["P0"]["utility_score"])
    p0_safe = pct(data["P0"]["safety_score"])
    p1_util = pct(data["P1"]["utility_score"])
    p1_safe = pct(data["P1"]["safety_score"])

    arrow = FancyArrowPatch(
        (p0_util, p0_safe), (p1_util, p1_safe),
        arrowstyle="-|>", mutation_scale=12,
        linewidth=1.2, color="#767676", alpha=0.7, zorder=1,
    )
    ax.add_patch(arrow)

    ax.scatter(p0_util, p0_safe, s=120, color=P0_COLOR, edgecolor="black",
               linewidth=0.6, zorder=3)
    ax.scatter(p1_util, p1_safe, s=120, color=P1_COLOR, edgecolor="black",
               linewidth=0.6, zorder=3)

    ax.annotate('P0 (no policy)', (p0_util, p0_safe),
                xytext=(p0_util + 1, p0_safe + 2.5), fontsize=6.5,
                ha='left', color=P0_COLOR, fontweight='bold')
    ax.annotate('P1 (per-agent policy)', (p1_util, p1_safe),
                xytext=(p1_util + 1, p1_safe + 2.5), fontsize=6.5,
                ha='left', color=P1_COLOR, fontweight='bold')

    mid_x = (p0_util + p1_util) / 2
    mid_y = (p0_safe + p1_safe) / 2
    ax.annotate(
        f"+{p1_safe - p0_safe:.1f}pp safety\n{p1_util - p0_util:.1f}pp utility",
        xy=(mid_x, mid_y), xytext=(mid_x + 4, mid_y + 8),
        arrowprops=dict(arrowstyle="-", color='#767676', lw=0.8),
        fontsize=6, ha='left',
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=C_NEUTRAL, alpha=0.9),
    )

    ax.set_xlabel("Utility (%)")
    ax.set_ylabel("Safety (%)")
    ax.set_xlim(74, 92)
    ax.set_ylim(18, 78)

    save(fig, "pact_net_frontier")


# =========================================================================
# Plot 2: Bimodal effectiveness — the chapter's core message
# =========================================================================
def plot_bimodal_effectiveness(data: dict) -> None:
    """Horizontal dumbbell: policy-responsive vs policy-resistant families."""
    fig, ax = plt.subplots(figsize=(5.5, 3.5))

    rows = [
        ("Cross-surface plant\n(action)", pct(data["P0"]["action_categories"]["cross_surface_plant"]),
         pct(data["P1"]["action_categories"]["cross_surface_plant"]), "bilateral"),
        ("Should-refuse\n(QA)", pct(data["P0"]["qa_categories"]["should_refuse"]),
         pct(data["P1"]["qa_categories"]["should_refuse"]), "bilateral"),
        ("Unauthorized mutation\n(action)", pct(data["P0"]["action_categories"]["unauthorized_mutation"]),
         pct(data["P1"]["action_categories"]["unauthorized_mutation"]), "bilateral"),
        ("Confused deputy\n(action)", pct(data["P0"]["action_categories"]["confused_deputy"]),
         pct(data["P1"]["action_categories"]["confused_deputy"]), "bilateral"),
        ("Contact enforcement\n(routing)", pct(data["P0"]["qa_categories"]["non_contact_probe"]),
         pct(data["P1"]["qa_categories"]["non_contact_probe"]), "structural"),
        ("Cross-cluster leak\n(QA)", pct(data["P0"]["qa_categories"]["cross_cluster"]),
         pct(data["P1"]["qa_categories"]["cross_cluster"]), "network"),
        ("Transitive risk\n(QA)", pct(data["P0"]["qa_categories"]["transitive_risk"]),
         pct(data["P1"]["qa_categories"]["transitive_risk"]), "network"),
    ]

    group_colors = {"bilateral": BILATERAL, "network": NETWORK, "structural": STRUCTURAL}

    for y, (label, p0, p1, group) in enumerate(rows):
        color = group_colors[group]
        ax.axhspan(y - 0.42, y + 0.42, color=color, alpha=0.06, lw=0)
        ax.plot([p0, p1], [y, y], color=color, lw=2.0, alpha=0.5, solid_capstyle="round")
        ax.scatter(p0, y, s=40, color=P0_COLOR, edgecolor="black", linewidth=0.4, zorder=3)
        ax.scatter(p1, y, s=50, color=P1_COLOR, edgecolor="black", linewidth=0.4, zorder=4)
        delta = p1 - p0
        x_label = min(max(p1 + 2.0, 2), 102)
        ax.text(x_label, y, f"{delta:+.1f}pp", va="center", fontsize=5.5, color='#4D4D4D')

    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=6)
    ax.set_xlim(-2, 108)
    ax.set_xlabel("Correct protection / correct decision (%)")

    ax.axhline(4.5, color=C_NEUTRAL, lw=0.6, ls="--", alpha=0.6)
    ax.text(104, 5.5, "Network-native\n(policy-resistant)", fontsize=5.5, color=NETWORK,
            ha="right", va="center", fontweight="bold")
    ax.text(104, 2.0, "Bilateral\n(policy-responsive)", fontsize=5.5, color=BILATERAL,
            ha="right", va="center", fontweight="bold")

    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="w", label="P0 (no policy)",
                   markerfacecolor=P0_COLOR, markersize=5),
        plt.Line2D([0], [0], marker="o", color="w", label="P1 (per-agent policy)",
                   markerfacecolor=P1_COLOR, markersize=5),
    ]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=6)

    save(fig, "pact_net_bimodal_effectiveness")


# =========================================================================
# Plot 3: Per-family grouped bar (P0 vs P1)
# =========================================================================
def plot_family_accuracy_bar(data: dict) -> None:
    """Grouped bar showing 9 task families, P0 vs P1."""
    fig, ax = plt.subplots(figsize=(7.2, 3.2))

    families = [
        ("should\nanswer", "should_answer", "qa", "utility"),
        ("auth.\ncreate", "authorized_create", "action", "utility"),
        ("auth.\ncomplete", "authorized_complete", "action", "utility"),
        ("should\nrefuse", "should_refuse", "qa", "safety"),
        ("unauth.\nmutation", "unauthorized_mutation", "action", "safety"),
        ("confused\ndeputy", "confused_deputy", "action", "safety"),
        ("cross-surface\nplant", "cross_surface_plant", "action", "safety"),
        ("transitive\nrisk", "transitive_risk", "qa", "safety"),
        ("cross\ncluster", "cross_cluster", "qa", "safety"),
    ]

    x = np.arange(len(families))
    width = 0.38

    p0_vals = []
    p1_vals = []
    for _, key, surface, _ in families:
        cat = "qa_categories" if surface == "qa" else "action_categories"
        p0_vals.append(pct(data["P0"][cat][key]))
        p1_vals.append(pct(data["P1"][cat][key]))

    ax.bar(x - width/2, p0_vals, width, color=P0_COLOR, alpha=0.75,
           edgecolor="black", linewidth=0.4, label="P0 (no policy)")
    bars_p1 = ax.bar(x + width/2, p1_vals, width, color=P1_COLOR, alpha=0.75,
                     edgecolor="black", linewidth=0.4, label="P1 (per-agent policy)")

    for bar, val in zip(bars_p1, p1_vals):
        if val > 5:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.0,
                    f"{val:.0f}", ha="center", va="bottom", fontsize=5.5, color=P1_COLOR)

    ax.set_xticks(x)
    ax.set_xticklabels([f[0] for f in families], fontsize=5.5)
    ax.set_ylabel("Correct response rate (%)")
    ax.set_ylim(0, 108)
    ax.legend(loc="upper right", fontsize=6)

    ax.axvspan(-0.5, 2.5, color=UTILITY_C, alpha=0.04)
    ax.axvspan(2.5, 8.5, color=P1_COLOR, alpha=0.03)
    ax.text(1.0, 104, "UTILITY", fontsize=5.5, color=UTILITY_C, ha="center", fontweight="bold")
    ax.text(5.5, 104, "SAFETY", fontsize=5.5, color=P1_COLOR, ha="center", fontweight="bold")

    save(fig, "pact_net_family_accuracy")


# =========================================================================
# Plot 4: Network metrics — the four findings panel (P0 vs P1 slope chart)
# =========================================================================
def plot_four_findings(data: dict) -> None:
    """2x2 panel showing F1–F4 as slope charts."""
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 4.5))

    def slope(ax, title, p0_val, p1_val, xlim, unit, note, finding_color, panel_lbl):
        y = 0
        ax.plot([p0_val, p1_val], [y, y], color=finding_color, lw=2.0, alpha=0.5,
                solid_capstyle="round")
        ax.scatter(p0_val, y, s=60, color=P0_COLOR, edgecolor="black", linewidth=0.4, zorder=3)
        ax.scatter(p1_val, y, s=70, color=P1_COLOR, edgecolor="black", linewidth=0.4, zorder=4)
        ax.text(p0_val, y + 0.12, f"P0\n{p0_val:.1f}{unit}", ha="center", va="bottom",
                fontsize=6, fontweight="bold")
        ax.text(p1_val, y - 0.12, f"P1\n{p1_val:.1f}{unit}", ha="center", va="top",
                fontsize=6, fontweight="bold")
        delta = p1_val - p0_val
        ax.set_title(f"{title}  ({delta:+.1f}{unit})", fontsize=7, fontweight="bold")
        ax.set_xlim(*xlim)
        ax.set_ylim(-0.55, 0.55)
        ax.set_yticks([])
        ax.set_xlabel(note, fontsize=5.5, color='#767676')
        add_panel_label(ax, panel_lbl)

    nm_p0 = data["P0"]["network_metrics"]
    nm_p1 = data["P1"]["network_metrics"]

    slope(axes[0, 0], "F1. Transitive leak",
          pct(nm_p0["T_transitive_leak"]), pct(nm_p1["T_transitive_leak"]),
          (0, 105), "%", "leak rate — lower is better", NETWORK, "a")

    slope(axes[0, 1], "F2. Cross-cluster leak",
          pct(nm_p0["X_cross_cluster_leak"]), pct(nm_p1["X_cross_cluster_leak"]),
          (0, 105), "%", "leak rate — lower is better", NETWORK, "b")

    slope(axes[1, 0], "F3. Amplification",
          nm_p0["A_amplification"], nm_p1["A_amplification"],
          (1.35, 1.68), "×", "facts per leak event — lower is better", NETWORK, "c")

    slope(axes[1, 1], "F4. Confused deputy",
          pct(nm_p0["D_confused_deputy"]), pct(nm_p1["D_confused_deputy"]),
          (0, 55), "%", "attack success — lower is better", BILATERAL, "d")

    save(fig, "pact_net_four_findings")


# =========================================================================
# Plot 5: Waterfall — where does the 10pp utility loss come from?
# =========================================================================
def plot_utility_cost_waterfall(data: dict) -> None:
    """Show which utility families absorb the cost of P1 policy."""
    fig, ax = plt.subplots(figsize=(4.0, 3.0))

    families = [
        ("should_answer", 172, "qa"),
        ("authorized_create", 184, "action"),
        ("authorized_complete", 115, "action"),
    ]

    labels = ["Should-answer\n(N=172)", "Auth. create\n(N=184)", "Auth. complete\n(N=115)"]
    p0_vals = []
    p1_vals = []
    for key, n, surface in families:
        cat = "qa_categories" if surface == "qa" else "action_categories"
        p0_vals.append(pct(data["P0"][cat][key]))
        p1_vals.append(pct(data["P1"][cat][key]))

    x = np.arange(len(families))
    width = 0.35

    ax.bar(x - width/2, p0_vals, width, color=P0_COLOR, alpha=0.75,
           edgecolor="black", linewidth=0.4, label="P0")
    ax.bar(x + width/2, p1_vals, width, color=P1_COLOR, alpha=0.75,
           edgecolor="black", linewidth=0.4, label="P1")

    for i, (p0, p1) in enumerate(zip(p0_vals, p1_vals)):
        delta = p1 - p0
        ax.text(i, max(p0, p1) + 1.5, f"{delta:+.1f}pp", ha="center",
                fontsize=6, color='#4D4D4D', fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=6)
    ax.set_ylabel("Correct execution rate (%)")
    ax.set_ylim(0, 108)
    ax.legend(loc="lower right", fontsize=6)

    save(fig, "pact_net_utility_cost")


# =========================================================================
# Plot 6: Heatmap — protection matrix (cleaner, P0/P1 labeled)
# =========================================================================
def plot_protection_heatmap(data: dict) -> None:
    """Clean heatmap with all task families, P0 vs P1."""
    families_ordered = [
        ("Should-answer (utility)", "should_answer", "qa"),
        ("Auth. create (utility)", "authorized_create", "action"),
        ("Auth. complete (utility)", "authorized_complete", "action"),
        ("Should-refuse (security)", "should_refuse", "qa"),
        ("Unauth. mutation (security)", "unauthorized_mutation", "action"),
        ("Confused deputy (security)", "confused_deputy", "action"),
        ("Cross-surface plant (security)", "cross_surface_plant", "action"),
        ("Transitive risk (network)", "transitive_risk", "qa"),
        ("Cross-cluster (network)", "cross_cluster", "qa"),
        ("Non-contact probe (infra)", "non_contact_probe", "qa"),
    ]

    matrix = np.zeros((len(families_ordered), 2))
    labels = []
    for i, (label, key, surface) in enumerate(families_ordered):
        cat = "qa_categories" if surface == "qa" else "action_categories"
        matrix[i, 0] = pct(data["P0"][cat][key])
        matrix[i, 1] = pct(data["P1"][cat][key])
        labels.append(label)

    fig, ax = plt.subplots(figsize=(3.5, 4.5))
    im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto", vmin=0, vmax=100)
    cbar = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.04)
    cbar.set_label("Correct rate (%)", fontsize=6)
    cbar.ax.tick_params(labelsize=5.5)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["P0", "P1"], fontsize=7)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=5.5)

    for (i, j), val in np.ndenumerate(matrix):
        color = "white" if val < 40 else "black"
        ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=5.5, color=color)

    ax.set_frame_on(False)
    save(fig, "pact_net_protection_heatmap")


# =========================================================================
# Plot 7: Residual gap — what policy cannot fix
# =========================================================================
def plot_residual_gap(data: dict) -> None:
    """Bar chart showing residual leak rates under P1 for network families."""
    fig, ax = plt.subplots(figsize=(3.5, 2.8))

    metrics = [
        ("Transitive", pct(data["P1"]["network_metrics"]["T_transitive_leak"])),
        ("Cross-cluster", pct(data["P1"]["network_metrics"]["X_cross_cluster_leak"])),
        ("Confused deputy", pct(data["P1"]["network_metrics"]["D_confused_deputy"])),
    ]

    x = np.arange(len(metrics))
    colors = [NETWORK, NETWORK, BILATERAL]
    values = [m[1] for m in metrics]

    bars = ax.bar(x, values, color=colors, alpha=0.8, edgecolor="black",
                  linewidth=0.6, width=0.55)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=7, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([m[0] for m in metrics], fontsize=6.5)
    ax.set_ylabel("Residual rate under P1 (%)")
    ax.set_ylim(0, 90)

    ax.axhline(10, color=C_DELTA_UP, lw=0.6, ls="--", alpha=0.6)
    ax.text(2.35, 11, "~solved", fontsize=5.5, color=C_DELTA_UP, va="bottom")

    save(fig, "pact_net_residual_gap")


# =========================================================================
# Plot 8: Delta chart — sorted by improvement magnitude
# =========================================================================
def plot_improvement_waterfall(data: dict) -> None:
    """Sorted horizontal bar of P0→P1 improvement by family."""
    fig, ax = plt.subplots(figsize=(4.5, 3.5))

    families = [
        ("Cross-surface plant", "cross_surface_plant", "action"),
        ("Should-refuse", "should_refuse", "qa"),
        ("Unauthorized mutation", "unauthorized_mutation", "action"),
        ("Confused deputy", "confused_deputy", "action"),
        ("Transitive risk", "transitive_risk", "qa"),
        ("Cross-cluster", "cross_cluster", "qa"),
        ("Non-contact probe", "non_contact_probe", "qa"),
        ("Auth. complete", "authorized_complete", "action"),
        ("Should-answer", "should_answer", "qa"),
        ("Auth. create", "authorized_create", "action"),
    ]

    deltas = []
    for label, key, surface in families:
        cat = "qa_categories" if surface == "qa" else "action_categories"
        d = pct(data["P1"][cat][key]) - pct(data["P0"][cat][key])
        deltas.append(d)

    y = np.arange(len(families))
    colors = [BILATERAL if d > 20 else (NETWORK if d > 0 else C_DELTA_DOWN) for d in deltas]

    ax.barh(y, deltas, color=colors, alpha=0.75, edgecolor="black", linewidth=0.4, height=0.6)

    for i, (d, label) in enumerate(zip(deltas, [f[0] for f in families])):
        offset = 1.0 if d >= 0 else -1.0
        ha = "left" if d >= 0 else "right"
        ax.text(d + offset, i, f"{d:+.1f}pp", va="center", ha=ha, fontsize=5.5)

    ax.set_yticks(y)
    ax.set_yticklabels([f[0] for f in families], fontsize=6)
    ax.axvline(0, color="black", lw=0.5)
    ax.set_xlabel("Improvement P0 → P1 (pp)")

    save(fig, "pact_net_improvement_sorted")


def plot_ch5_combined(data: dict) -> None:
    """Two-panel combined figure: frontier (left) + family accuracy (right)."""
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(7.2, 3.0),
                                      gridspec_kw={"width_ratios": [1, 2.2]})

    # ── Left panel: frontier ──
    add_panel_label(ax_l, "a")
    p0_util = pct(data["P0"]["utility_score"])
    p0_safe = pct(data["P0"]["safety_score"])
    p1_util = pct(data["P1"]["utility_score"])
    p1_safe = pct(data["P1"]["safety_score"])

    arrow = FancyArrowPatch(
        (p0_util, p0_safe), (p1_util, p1_safe),
        arrowstyle="-|>", mutation_scale=12,
        linewidth=1.2, color="#767676", alpha=0.7, zorder=1,
    )
    ax_l.add_patch(arrow)
    ax_l.scatter(p0_util, p0_safe, s=100, color=P0_COLOR, edgecolor="black",
                 linewidth=0.6, zorder=3)
    ax_l.scatter(p1_util, p1_safe, s=100, color=P1_COLOR, edgecolor="black",
                 linewidth=0.6, zorder=3)
    ax_l.annotate('P0', (p0_util, p0_safe),
                  xytext=(p0_util + 1, p0_safe + 3), fontsize=6.5,
                  ha='left', color=P0_COLOR, fontweight='bold')
    ax_l.annotate('P1', (p1_util, p1_safe),
                  xytext=(p1_util + 1, p1_safe + 3), fontsize=6.5,
                  ha='left', color=P1_COLOR, fontweight='bold')
    ax_l.set_xlabel("Utility (%)")
    ax_l.set_ylabel("Safety (%)")
    ax_l.set_xlim(55, 100)
    ax_l.set_ylim(15, 85)
    ax_l.set_title("Security–utility frontier", fontsize=7, fontweight="bold")

    # ── Right panel: family accuracy bar ──
    add_panel_label(ax_r, "b")
    families = [
        ("should\nanswer", "should_answer", "qa", "utility"),
        ("auth.\ncreate", "authorized_create", "action", "utility"),
        ("auth.\ncomplete", "authorized_complete", "action", "utility"),
        ("should\nrefuse", "should_refuse", "qa", "safety"),
        ("unauth.\nmutation", "unauthorized_mutation", "action", "safety"),
        ("confused\ndeputy", "confused_deputy", "action", "safety"),
        ("cross-surface\nplant", "cross_surface_plant", "action", "safety"),
        ("transitive\nrisk", "transitive_risk", "qa", "safety"),
        ("cross\ncluster", "cross_cluster", "qa", "safety"),
    ]

    x = np.arange(len(families))
    width = 0.38

    p0_vals = []
    p1_vals = []
    for _, key, surface, _ in families:
        cat = "qa_categories" if surface == "qa" else "action_categories"
        p0_vals.append(pct(data["P0"][cat][key]))
        p1_vals.append(pct(data["P1"][cat][key]))

    ax_r.bar(x - width/2, p0_vals, width, color=P0_COLOR, alpha=0.75,
             edgecolor="black", linewidth=0.4, label="P0 (no policy)")
    bars_p1 = ax_r.bar(x + width/2, p1_vals, width, color=P1_COLOR, alpha=0.75,
                       edgecolor="black", linewidth=0.4, label="P1 (per-agent policy)")

    for bar, val in zip(bars_p1, p1_vals):
        if val > 5:
            ax_r.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.0,
                      f"{val:.0f}", ha="center", va="bottom", fontsize=5, color=P1_COLOR)

    ax_r.set_xticks(x)
    ax_r.set_xticklabels([f[0] for f in families], fontsize=5.5)
    ax_r.set_ylabel("Correct response rate (%)")
    ax_r.set_ylim(0, 108)
    ax_r.legend(loc="upper right", fontsize=5.5)

    ax_r.axvspan(-0.5, 2.5, color=UTILITY_C, alpha=0.04)
    ax_r.axvspan(2.5, 8.5, color=P1_COLOR, alpha=0.03)
    ax_r.text(1.0, 104, "UTILITY", fontsize=5.5, color=UTILITY_C, ha="center", fontweight="bold")
    ax_r.text(5.5, 104, "SAFETY", fontsize=5.5, color=P1_COLOR, ha="center", fontweight="bold")
    ax_r.set_title("Per-family accuracy", fontsize=7, fontweight="bold")

    save(fig, "pact_net_ch5_combined")


def main() -> None:
    PLOT_DIR.mkdir(parents=True, exist_ok=True)

    data = load_data()

    print("Generating PACT-NET (Chapter 5) figures...")
    plot_frontier(data)
    plot_bimodal_effectiveness(data)
    plot_family_accuracy_bar(data)
    plot_four_findings(data)
    plot_utility_cost_waterfall(data)
    plot_protection_heatmap(data)
    plot_residual_gap(data)
    plot_improvement_waterfall(data)
    plot_ch5_combined(data)
    print("Done.")


if __name__ == "__main__":
    main()
