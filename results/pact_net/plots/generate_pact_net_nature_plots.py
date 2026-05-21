#!/usr/bin/env python3
"""Generate polished PACT-NET figures for the thesis.

These figures intentionally focus on the Chapter 5 PACT-NET story:
P0 (no policy) versus P1 (per-agent static policy). MCC conditions are present
in the source JSON, but are excluded here to avoid mixing the Chapter 5
benchmark findings with Chapter 6 solution ablations.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "summary_mcc_h_mcc_h_d1_pact_net_v2.json"
OUT = ROOT / "plots" / "nature"
OUT.mkdir(parents=True, exist_ok=True)


COLORS = {
    "P0": "#E64B35",          # muted red
    "P1": "#3C5488",          # muted blue
    "utility": "#00A087",     # teal
    "bilateral": "#4DBBD5",   # cyan
    "network": "#7E6148",     # brown
    "infra": "#8491B4",       # slate
    "accent": "#F39B7F",      # peach
    "text": "#1f2937",
    "muted": "#6b7280",
    "grid": "#e5e7eb",
}


plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "font.size": 7.5,
        "axes.titlesize": 8.5,
        "axes.labelsize": 7.8,
        "xtick.labelsize": 7.0,
        "ytick.labelsize": 7.0,
        "legend.fontsize": 7.0,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.55,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)


def pct(x: float) -> float:
    return 100 * x


def load() -> dict[str, dict]:
    with SUMMARY_PATH.open() as f:
        conditions = json.load(f)["conditions"]
    return {"P0": conditions["D0"], "P1": conditions["D1"]}


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=600, bbox_inches="tight")
    plt.close(fig)


def clean(ax: plt.Axes, *, xgrid: bool = False, ygrid: bool = True) -> None:
    ax.spines["left"].set_color("#cbd5e1")
    ax.spines["bottom"].set_color("#cbd5e1")
    ax.tick_params(color="#cbd5e1", labelcolor=COLORS["text"], width=0.5)
    if ygrid:
        ax.grid(True, axis="y", color=COLORS["grid"], lw=0.5, alpha=0.75)
    else:
        ax.grid(False, axis="y")
    if xgrid:
        ax.grid(True, axis="x", color=COLORS["grid"], lw=0.5, alpha=0.75)
    else:
        ax.grid(False, axis="x")


def write_source_data(data: dict[str, dict]) -> None:
    rows = []
    for family, p0, p1, group, unit in finding_rows(data):
        rows.append(
            {
                "metric": family,
                "group": group,
                "p0": round(p0, 4),
                "p1": round(p1, 4),
                "delta_p1_minus_p0": round(p1 - p0, 4),
                "unit": unit,
            }
        )

    for label, key, surface, group in task_family_rows():
        cat = "qa_categories" if surface == "qa" else "action_categories"
        rows.append(
            {
                "metric": label,
                "group": group,
                "p0": round(pct(data["P0"][cat][key]), 4),
                "p1": round(pct(data["P1"][cat][key]), 4),
                "delta_p1_minus_p0": round(
                    pct(data["P1"][cat][key]) - pct(data["P0"][cat][key]), 4
                ),
                "unit": "correct_decision_percent",
            }
        )

    with (OUT / "nature_pact_net_source_data.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def finding_rows(data: dict[str, dict]) -> list[tuple[str, float, float, str, str]]:
    return [
        (
            "Transitive leakage",
            pct(data["P0"]["network_metrics"]["T_transitive_leak"]),
            pct(data["P1"]["network_metrics"]["T_transitive_leak"]),
            "network-native",
            "leak_rate_percent",
        ),
        (
            "Cross-cluster leakage",
            pct(data["P0"]["network_metrics"]["X_cross_cluster_leak"]),
            pct(data["P1"]["network_metrics"]["X_cross_cluster_leak"]),
            "network-native",
            "leak_rate_percent",
        ),
        (
            "Amplification factor",
            data["P0"]["network_metrics"]["A_amplification"],
            data["P1"]["network_metrics"]["A_amplification"],
            "network-native",
            "facts_per_leaking_answer",
        ),
        (
            "Confused-deputy success",
            pct(data["P0"]["network_metrics"]["D_confused_deputy"]),
            pct(data["P1"]["network_metrics"]["D_confused_deputy"]),
            "authority-chain",
            "attack_success_percent",
        ),
    ]


def task_family_rows() -> list[tuple[str, str, str, str]]:
    return [
        ("Should-answer", "should_answer", "qa", "utility"),
        ("Authorized create", "authorized_create", "action", "utility"),
        ("Authorized complete", "authorized_complete", "action", "utility"),
        ("Should-refuse", "should_refuse", "qa", "bilateral safety"),
        ("Unauthorized mutation", "unauthorized_mutation", "action", "bilateral safety"),
        ("Confused deputy", "confused_deputy", "action", "authority-chain"),
        ("Cross-surface plant", "cross_surface_plant", "action", "bilateral safety"),
        ("Transitive risk", "transitive_risk", "qa", "network-native"),
        ("Cross-cluster", "cross_cluster", "qa", "network-native"),
        ("Non-contact probe", "non_contact_probe", "qa", "infrastructure"),
    ]


def plot_policy_effect_scatter(data: dict[str, dict]) -> None:
    rows = []
    for label, key, surface, group in task_family_rows():
        cat = "qa_categories" if surface == "qa" else "action_categories"
        rows.append(
            {
                "label": label,
                "p0": pct(data["P0"][cat][key]),
                "p1": pct(data["P1"][cat][key]),
                "group": group,
            }
        )

    color_map = {
        "utility": COLORS["utility"],
        "bilateral safety": COLORS["bilateral"],
        "authority-chain": COLORS["accent"],
        "network-native": COLORS["network"],
        "infrastructure": COLORS["infra"],
    }

    fig, ax = plt.subplots(figsize=(4.9, 4.35))
    clean(ax, xgrid=True, ygrid=True)
    ax.plot([0, 105], [0, 105], color="#9ca3af", lw=0.8, ls="--", zorder=0)

    for row in rows:
        ax.scatter(
            row["p0"],
            row["p1"],
            s=46,
            color=color_map[row["group"]],
            edgecolor="white",
            linewidth=0.7,
            zorder=3,
        )
        dx = 1.8 if row["p0"] < 92 else -1.8
        ha = "left" if dx > 0 else "right"
        ax.text(row["p0"] + dx, row["p1"] + 1.2, row["label"], fontsize=6.0, ha=ha)

    ax.text(7, 98, "Policy improves", color=COLORS["muted"], fontsize=6.8)
    ax.text(61, 53, "No net gain", color=COLORS["muted"], fontsize=6.8, rotation=37)
    ax.set_xlim(-2, 105)
    ax.set_ylim(-2, 105)
    ax.set_xlabel("P0 correct decision rate (%)")
    ax.set_ylabel("P1 correct decision rate (%)")
    ax.set_title("Policy effect by PACT-NET task family")

    handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=color, markeredgecolor="white",
               markersize=5.8, label=group)
        for group, color in color_map.items()
    ]
    ax.legend(handles=handles, loc="lower right", frameon=False, ncol=1)
    save(fig, "nature_pact_net_policy_effect_scatter")


def plot_four_findings(data: dict[str, dict]) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(6.75, 4.45))
    fig.subplots_adjust(wspace=0.34, hspace=0.48)
    axes = axes.ravel()

    subtitles = [
        "A. Third-party facts still leak",
        "B. Cluster boundaries remain porous",
        "C. Leaks disclose bundles, not atoms",
        "D. False delegation is policy-responsive",
    ]

    for ax, (title, p0, p1, _group, unit), subtitle in zip(axes, finding_rows(data), subtitles):
        clean(ax, xgrid=False, ygrid=True)
        if unit == "facts_per_leaking_answer":
            ax.set_ylim(1.35, 1.75)
            ylabel = "facts per leak"
            label_fmt = "{:.2f}"
        else:
            ax.set_ylim(0, 105)
            ylabel = "rate (%)"
            label_fmt = "{:.1f}%"

        ax.plot([0, 1], [p0, p1], color="#94a3b8", lw=1.5, zorder=1)
        ax.scatter([0], [p0], color=COLORS["P0"], s=58, edgecolor="white", linewidth=0.8, zorder=3)
        ax.scatter([1], [p1], color=COLORS["P1"], s=58, edgecolor="white", linewidth=0.8, zorder=3)

        ax.text(-0.08, p0, label_fmt.format(p0), ha="right", va="center", fontsize=6.8, color=COLORS["P0"], weight="bold")
        ax.text(1.08, p1, label_fmt.format(p1), ha="left", va="center", fontsize=6.8, color=COLORS["P1"], weight="bold")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["P0", "P1"])
        ax.set_ylabel(ylabel)
        ax.set_title(subtitle, loc="left", pad=5)

        delta = p1 - p0
        ax.text(
            0.5,
            0.08,
            f"Δ {delta:+.1f}" + (" pp" if unit != "facts_per_leaking_answer" else ""),
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=7.0,
            color=COLORS["text"],
            bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#e5e7eb", "lw": 0.6},
        )

    fig.suptitle(
        "PACT-NET exposes failures that dyadic benchmarks hide",
        x=0.02,
        ha="left",
        y=1.02,
        fontsize=9.5,
        weight="bold",
        color=COLORS["text"],
    )
    save(fig, "nature_pact_net_four_findings")


def plot_task_family_matrix(data: dict[str, dict]) -> None:
    labels = []
    matrix = []
    groups = []
    for label, key, surface, group in task_family_rows():
        cat = "qa_categories" if surface == "qa" else "action_categories"
        labels.append(label)
        matrix.append([pct(data["P0"][cat][key]), pct(data["P1"][cat][key])])
        groups.append(group)

    fig = plt.figure(figsize=(5.65, 4.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 0.055], wspace=0.035)
    ax = fig.add_subplot(gs[0, 0])
    group_ax = fig.add_subplot(gs[0, 1])

    cmap = sns.color_palette("rocket_r", as_cmap=True)
    sns.heatmap(
        np.array(matrix),
        ax=ax,
        cmap=cmap,
        vmin=0,
        vmax=100,
        annot=True,
        fmt=".0f",
        annot_kws={"fontsize": 6.4},
        linewidths=0.55,
        linecolor="white",
        cbar_kws={"label": "correct decision (%)", "shrink": 0.72, "pad": 0.02},
    )
    ax.set_xticklabels(["P0", "P1"], rotation=0)
    ax.set_yticklabels(labels, rotation=0)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("PACT-NET task-family outcome matrix", loc="left")

    group_palette = {
        "utility": COLORS["utility"],
        "bilateral safety": COLORS["bilateral"],
        "authority-chain": COLORS["accent"],
        "network-native": COLORS["network"],
        "infrastructure": COLORS["infra"],
    }
    group_codes = np.array([[list(group_palette).index(g)] for g in groups])
    group_cmap = matplotlib.colors.ListedColormap(list(group_palette.values()))
    group_ax.imshow(group_codes, aspect="auto", cmap=group_cmap)
    group_ax.set_xticks([])
    group_ax.set_yticks([])
    for spine in group_ax.spines.values():
        spine.set_visible(False)

    handles = [
        Line2D([0], [0], marker="s", color="none", markerfacecolor=color, markersize=5.5, label=group)
        for group, color in group_palette.items()
    ]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.48, -0.22), ncol=3, frameon=False)
    save(fig, "nature_pact_net_task_family_matrix")


def plot_frontier(data: dict[str, dict]) -> None:
    p0 = (pct(data["P0"]["utility_score"]), pct(data["P0"]["safety_score"]))
    p1 = (pct(data["P1"]["utility_score"]), pct(data["P1"]["safety_score"]))

    fig, ax = plt.subplots(figsize=(4.5, 3.65))
    clean(ax, xgrid=True, ygrid=True)
    ax.add_patch(
        FancyArrowPatch(
            p0,
            p1,
            arrowstyle="-|>",
            mutation_scale=13,
            lw=1.4,
            color="#64748b",
            alpha=0.85,
            zorder=1,
        )
    )
    ax.scatter(*p0, color=COLORS["P0"], s=74, edgecolor="white", linewidth=0.9, zorder=3)
    ax.scatter(*p1, color=COLORS["P1"], s=74, edgecolor="white", linewidth=0.9, zorder=3)
    ax.text(p0[0] + 0.6, p0[1] - 4.2, "P0\nno policy", color=COLORS["P0"], weight="bold")
    ax.text(p1[0] + 0.6, p1[1] + 1.4, "P1\nper-agent policy", color=COLORS["P1"], weight="bold")
    ax.text(
        82.2,
        51,
        "+44.8 pp safety\n-10.0 pp utility",
        fontsize=7.2,
        bbox={"boxstyle": "round,pad=0.28", "fc": "white", "ec": "#e5e7eb", "lw": 0.6},
    )
    ax.set_xlim(74, 92)
    ax.set_ylim(20, 76)
    ax.set_xlabel("utility score (%)")
    ax.set_ylabel("safety score (%)")
    ax.set_title("PACT-NET safety--utility movement")
    save(fig, "nature_pact_net_frontier")


def main() -> None:
    data = load()
    write_source_data(data)
    plot_policy_effect_scatter(data)
    plot_four_findings(data)
    plot_task_family_matrix(data)
    plot_frontier(data)
    print(f"Wrote polished PACT-NET figures to {OUT}")


if __name__ == "__main__":
    main()
