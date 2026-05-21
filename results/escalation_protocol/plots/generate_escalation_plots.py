"""
Escalation Protocol (Chapter 6, §6.3) — Publication figures.
Nature-figure style: Arial, no top/right spines, 7pt base, editable SVG text.
No in-image captions. Captions in README.md.

Data source: phase2/summary_table.md (Table 6.5 in thesis)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

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

OUT = Path(__file__).parent
DPI = 600

# ─── Palette ─────────────────────────────────────────────────────────────────
C_MINI = "#E28E2C"       # gold/orange — GPT-5-mini
C_55 = "#0F4D92"         # blue_main — GPT-5.5
C_PSTOP = "#B64342"      # red_strong — security metric
C_UTIL = "#42949E"       # teal — utility metric
C_CORRECT = "#2E9E44"    # green — correct decisions
C_WRONG = "#B64342"      # red — wrong decisions
C_NEUTRAL = "#D8D8D8"

# ─── Phase 2 data (from summary_table.md) ────────────────────────────────────
# Format: [individual_10, cluster_2nn_10, rich_cluster_10, individual_30]
scopes = ['individual\n10%', 'cluster-2NN\n10%', 'rich-cluster-2NN\n10%', 'individual\n30%']

mini_pstop = [90.8, 88.5, 91.3, 87.7]
mini_util = [69.8, 76.7, 78.0, 91.0]
mini_fc = [9.2, 11.5, 8.8, 12.3]
mini_fs = [30.2, 23.3, 22.0, 9.0]

gpt55_pstop = [94.2, 92.7, 94.4, 92.1]
gpt55_util = [67.1, 71.3, 68.1, 87.4]
gpt55_fc = [5.8, 7.3, 5.6, 7.9]
gpt55_fs = [32.9, 28.7, 31.9, 12.6]

# Per-category (GPT-5.5, from summary_table.md)
categories_55 = ['cross_cluster', 'should_answer', 'should_refuse', 'transitive_risk']
cat_pstop_indiv10 = [86.7, 75.6, 96.8, 96.9]
cat_util_indiv10 = [69.1, 76.7, 41.0, 57.9]
cat_pstop_cluster10 = [80.0, 68.9, 96.5, 93.5]
cat_util_cluster10 = [86.8, 81.5, 38.5, 60.4]
cat_pstop_rich10 = [86.7, 68.9, 97.9, 96.9]
cat_util_rich10 = [69.1, 77.7, 39.3, 60.0]

# Decision change analysis
transfer_labels = ['indiv→cluster\n(5-mini)', 'indiv→cluster\n(5.5)',
                   'indiv→rich\n(5-mini)', 'indiv→rich\n(5.5)']
changed_correct = [116, 83, 149, 70]
changed_wrong = [53, 46, 59, 59]


def add_panel_label(ax, label, x=-0.08, y=1.05):
    ax.text(x, y, label, transform=ax.transAxes, fontsize=9,
            fontweight='bold', ha='left', va='bottom')


def save(fig, name):
    fig.tight_layout(pad=1.5)
    for fmt in ['svg', 'pdf', 'png']:
        fig.savefig(OUT / f'{name}.{fmt}', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"  saved: {name}")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 1: PStop vs Utility — Security-Utility Trade-off (hero figure)
# ═══════════════════════════════════════════════════════════════════════════════
def plot_pstop_utility_scatter():
    fig, ax = plt.subplots(figsize=(4.0, 3.2))

    # GPT-5-mini points
    ax.scatter(mini_util, mini_pstop, s=80, c=C_MINI, marker='o',
               edgecolors='black', linewidths=0.5, zorder=5, label='GPT-5-mini')
    # GPT-5.5 points
    ax.scatter(gpt55_util, gpt55_pstop, s=80, c=C_55, marker='s',
               edgecolors='black', linewidths=0.5, zorder=5, label='GPT-5.5')

    # Annotate key points
    labels_short = ['ind-10', 'cl-10', 'rich-10', 'ind-30']
    for i, lbl in enumerate(labels_short):
        ax.annotate(lbl, (mini_util[i], mini_pstop[i]),
                    xytext=(3, -8), textcoords='offset points', fontsize=5, color=C_MINI)
        ax.annotate(lbl, (gpt55_util[i], gpt55_pstop[i]),
                    xytext=(3, 4), textcoords='offset points', fontsize=5, color=C_55)

    ax.axhline(90, color=C_NEUTRAL, linestyle='--', linewidth=0.6, zorder=0)
    ax.text(92, 90.5, '90% PStop', fontsize=5, color='#767676')

    ax.set_xlabel('Utility (legitimate-request recall, %)')
    ax.set_ylabel('PStop (private-request recall, %)')
    ax.set_xlim(60, 95)
    ax.set_ylim(85, 96)
    ax.legend(fontsize=6, loc='lower right')

    save(fig, 'esc_pstop_utility_frontier')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 2: Grouped Bar — PStop and Utility by Scope (both models)
# ═══════════════════════════════════════════════════════════════════════════════
def plot_scope_comparison():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0))

    x = np.arange(len(scopes))
    w = 0.35

    # Panel a: PStop
    ax1.bar(x - w/2, mini_pstop, w, color=C_MINI, edgecolor='black',
            linewidth=0.4, label='GPT-5-mini')
    ax1.bar(x + w/2, gpt55_pstop, w, color=C_55, edgecolor='black',
            linewidth=0.4, label='GPT-5.5')
    ax1.axhline(90, color=C_NEUTRAL, linestyle='--', linewidth=0.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels(scopes, fontsize=6)
    ax1.set_ylabel('PStop — private recall (%)')
    ax1.set_ylim(80, 100)
    ax1.legend(fontsize=6)
    add_panel_label(ax1, 'a')

    # Panel b: Utility
    ax2.bar(x - w/2, mini_util, w, color=C_MINI, edgecolor='black',
            linewidth=0.4, label='GPT-5-mini')
    ax2.bar(x + w/2, gpt55_util, w, color=C_55, edgecolor='black',
            linewidth=0.4, label='GPT-5.5')
    ax2.set_xticks(x)
    ax2.set_xticklabels(scopes, fontsize=6)
    ax2.set_ylabel('Utility — legitimate recall (%)')
    ax2.set_ylim(0, 100)
    ax2.legend(fontsize=6)
    add_panel_label(ax2, 'b')

    save(fig, 'esc_scope_comparison')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 3: Error Decomposition — False Continue vs False Stop
# ═══════════════════════════════════════════════════════════════════════════════
def plot_error_decomposition():
    fig, ax = plt.subplots(figsize=(4.5, 3.0))

    x = np.arange(len(scopes))
    w = 0.2

    # GPT-5-mini
    ax.bar(x - 1.5*w, mini_fc, w, color=C_WRONG, alpha=0.5,
           edgecolor='black', linewidth=0.4, label='False cont. (5-mini)')
    ax.bar(x - 0.5*w, mini_fs, w, color=C_UTIL, alpha=0.5,
           edgecolor='black', linewidth=0.4, label='False stop (5-mini)')
    # GPT-5.5
    ax.bar(x + 0.5*w, gpt55_fc, w, color=C_WRONG, alpha=0.9,
           edgecolor='black', linewidth=0.4, label='False cont. (5.5)')
    ax.bar(x + 1.5*w, gpt55_fs, w, color=C_UTIL, alpha=0.9,
           edgecolor='black', linewidth=0.4, label='False stop (5.5)')

    ax.set_xticks(x)
    ax.set_xticklabels(scopes, fontsize=6)
    ax.set_ylabel('Error rate (%)')
    ax.set_ylim(0, 38)
    ax.legend(fontsize=5.5, ncol=2, loc='upper right')

    save(fig, 'esc_error_decomposition')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 4: Per-Category PStop (GPT-5.5) — shows where escalation works best
# ═══════════════════════════════════════════════════════════════════════════════
def plot_per_category():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0))

    cats_display = ['cross\ncluster', 'should\nanswer', 'should\nrefuse', 'transitive\nrisk']
    x = np.arange(len(cats_display))
    w = 0.25

    # Panel a: PStop per category
    ax1.bar(x - w, cat_pstop_indiv10, w, color=C_55, alpha=0.4,
            edgecolor='black', linewidth=0.4, label='individual-10')
    ax1.bar(x, cat_pstop_cluster10, w, color=C_55, alpha=0.7,
            edgecolor='black', linewidth=0.4, label='cluster-2NN-10')
    ax1.bar(x + w, cat_pstop_rich10, w, color=C_55, alpha=1.0,
            edgecolor='black', linewidth=0.4, label='rich-cluster-10')
    ax1.axhline(90, color=C_NEUTRAL, linestyle='--', linewidth=0.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels(cats_display, fontsize=6)
    ax1.set_ylabel('PStop (%)')
    ax1.set_ylim(60, 100)
    ax1.legend(fontsize=5.5)
    add_panel_label(ax1, 'a')

    # Panel b: Utility per category
    ax2.bar(x - w, cat_util_indiv10, w, color=C_UTIL, alpha=0.4,
            edgecolor='black', linewidth=0.4, label='individual-10')
    ax2.bar(x, cat_util_cluster10, w, color=C_UTIL, alpha=0.7,
            edgecolor='black', linewidth=0.4, label='cluster-2NN-10')
    ax2.bar(x + w, cat_util_rich10, w, color=C_UTIL, alpha=1.0,
            edgecolor='black', linewidth=0.4, label='rich-cluster-10')
    ax2.set_xticks(x)
    ax2.set_xticklabels(cats_display, fontsize=6)
    ax2.set_ylabel('Utility (%)')
    ax2.set_ylim(0, 100)
    ax2.legend(fontsize=5.5)
    add_panel_label(ax2, 'b')

    save(fig, 'esc_per_category')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 5: Transfer Delta — Improvement from expanding scope
# ═══════════════════════════════════════════════════════════════════════════════
def plot_transfer_delta():
    fig, ax = plt.subplots(figsize=(4.5, 2.8))

    comparisons = ['cluster vs indiv\n(5-mini)', 'cluster vs indiv\n(5.5)',
                   'rich vs indiv\n(5-mini)', 'rich vs indiv\n(5.5)']
    delta_pstop = [-2.3, -1.5, +0.4, +0.2]
    delta_util = [+6.9, +4.1, +8.2, +0.9]

    x = np.arange(len(comparisons))
    w = 0.35

    ax.bar(x - w/2, delta_pstop, w, color=C_PSTOP, edgecolor='black',
           linewidth=0.4, label='Δ PStop (pp)')
    ax.bar(x + w/2, delta_util, w, color=C_UTIL, edgecolor='black',
           linewidth=0.4, label='Δ Utility (pp)')

    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(comparisons, fontsize=6)
    ax.set_ylabel('Change (pp)')
    ax.set_ylim(-5, 12)
    ax.legend(fontsize=6)

    save(fig, 'esc_transfer_delta')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 6: Decision Change — Correct vs Wrong (transfer quality)
# ═══════════════════════════════════════════════════════════════════════════════
def plot_decision_change():
    fig, ax = plt.subplots(figsize=(4.0, 2.8))

    x = np.arange(len(transfer_labels))
    w = 0.35

    ax.bar(x - w/2, changed_correct, w, color=C_CORRECT, alpha=0.85,
           edgecolor='black', linewidth=0.4, label='Changed to correct')
    ax.bar(x + w/2, changed_wrong, w, color=C_WRONG, alpha=0.7,
           edgecolor='black', linewidth=0.4, label='Changed to wrong')

    for i, (c, wr) in enumerate(zip(changed_correct, changed_wrong)):
        ratio = c / (c + wr)
        ax.text(i, max(c, wr) + 5, f'{ratio:.0%}', ha='center', fontsize=6, color='#4D4D4D')

    ax.set_xticks(x)
    ax.set_xticklabels(transfer_labels, fontsize=6)
    ax.set_ylabel('Decisions changed')
    ax.legend(fontsize=6)
    ax.set_ylim(0, 175)

    save(fig, 'esc_decision_change')


# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating Escalation Protocol figures...")
    plot_pstop_utility_scatter()
    plot_scope_comparison()
    plot_error_decomposition()
    plot_per_category()
    plot_transfer_delta()
    plot_decision_change()
    print("Done.")
