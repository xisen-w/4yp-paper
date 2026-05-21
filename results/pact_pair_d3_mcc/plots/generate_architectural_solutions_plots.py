"""
Architectural Solutions (Chapter 6) — Publication figures.
Nature-figure style: Arial, no top/right spines, 7pt base, editable SVG text.
No in-image captions. Captions in README.md.
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

# ─── Palette (Nature NMI pastel family + accent) ─────────────────────────────
C_D3 = "#E28E2C"        # gold/orange (policy-only)
C_MCC = "#42949E"       # teal (structure-only)
C_COMBINED = "#0F4D92"  # blue_main (best combined)
C_ESCALATION = "#B64342"  # red (escalation)
C_NEUTRAL = "#D8D8D8"
C_DELTA_UP = "#2E9E44"
C_DELTA_DOWN = "#E53935"

# ─── Data from summary_three_condition_combined.json ─────────────────────────
requesters = ['R0\nStranger', 'R1\nColleague', 'R2\nDelegate', 'R3\nFriend', 'R4\nInvestor', 'Aggregate']

d3_util = [21.0, 87.4, 87.1, 63.3, 87.4, 70.9]
d3_leak = [1.2, 8.0, 12.6, 38.7, 16.9, 15.5]

mcc_util = [23.8, 82.9, 86.6, 26.2, 59.7, 57.6]
mcc_leak = [1.6, 20.3, 17.9, 22.0, 1.6, 12.4]

combined_util = [23.9, 83.3, 85.9, 27.1, 60.6, 58.5]
combined_leak = [0.6, 6.3, 12.6, 18.1, 2.7, 8.0]

# ─── Escalation Phase 2 data ─────────────────────────────────────────────────
esc_scopes = ['individual\n10%', 'cluster-2NN\n10%', 'rich-cluster\n10%', 'individual\n30%']
esc_pstop_mini = [90.8, 88.5, 91.3, 87.7]
esc_util_mini = [69.8, 76.7, 78.0, 91.0]
esc_pstop_55 = [94.2, 92.7, 94.4, 92.1]
esc_util_55 = [67.1, 71.3, 68.1, 87.4]


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
# FIGURE 1: Security–Utility Frontier (D3 vs MCC_H vs MCC_H+D3)
# ═══════════════════════════════════════════════════════════════════════════════
def plot_frontier():
    fig, ax = plt.subplots(figsize=(3.5, 3.0))

    ax.scatter(d3_util[-1], d3_leak[-1], s=120, c=C_D3, zorder=5,
               edgecolors='black', linewidths=0.6)
    ax.scatter(mcc_util[-1], mcc_leak[-1], s=120, c=C_MCC, zorder=5,
               edgecolors='black', linewidths=0.6)
    ax.scatter(combined_util[-1], combined_leak[-1], s=120, c=C_COMBINED, zorder=5,
               edgecolors='black', linewidths=0.6)

    offset = 1.2
    ax.annotate('D3 (policy only)', (d3_util[-1], d3_leak[-1]),
                xytext=(d3_util[-1]-3, d3_leak[-1]+offset), fontsize=6.5,
                ha='right', color=C_D3, fontweight='bold')
    ax.annotate('MCC_H (structure only)', (mcc_util[-1], mcc_leak[-1]),
                xytext=(mcc_util[-1]+2, mcc_leak[-1]+offset), fontsize=6.5,
                ha='left', color=C_MCC, fontweight='bold')
    ax.annotate('MCC_H + D3', (combined_util[-1], combined_leak[-1]),
                xytext=(combined_util[-1]+2, combined_leak[-1]-offset), fontsize=6.5,
                ha='left', color=C_COMBINED, fontweight='bold')

    # Draw arrows showing improvement path
    ax.annotate('', xy=(combined_util[-1], combined_leak[-1]),
                xytext=(d3_util[-1], d3_leak[-1]),
                arrowprops=dict(arrowstyle='->', color='#767676', lw=1.0,
                                connectionstyle='arc3,rad=-0.2'))

    ax.set_xlabel('Utility (%)')
    ax.set_ylabel('Leak rate (%)')
    ax.set_xlim(45, 80)
    ax.set_ylim(0, 20)
    ax.axhline(y=10, color=C_NEUTRAL, linestyle='--', linewidth=0.6, zorder=0)

    save(fig, 'arch_frontier')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 2: Per-Requester Decomposition (grouped bar)
# ═══════════════════════════════════════════════════════════════════════════════
def plot_per_requester():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0))

    x = np.arange(len(requesters))
    w = 0.25

    # Panel a: Utility
    ax1.bar(x - w, d3_util, w, color=C_D3, edgecolor='black', linewidth=0.4, label='D3')
    ax1.bar(x, mcc_util, w, color=C_MCC, edgecolor='black', linewidth=0.4, label='MCC_H')
    ax1.bar(x + w, combined_util, w, color=C_COMBINED, edgecolor='black', linewidth=0.4, label='MCC_H+D3')
    ax1.set_xticks(x)
    ax1.set_xticklabels(requesters, fontsize=6)
    ax1.set_ylabel('Utility (%)')
    ax1.set_ylim(0, 100)
    ax1.legend(fontsize=6, loc='upper left')
    add_panel_label(ax1, 'a')

    # Panel b: Leak rate
    ax2.bar(x - w, d3_leak, w, color=C_D3, edgecolor='black', linewidth=0.4, label='D3')
    ax2.bar(x, mcc_leak, w, color=C_MCC, edgecolor='black', linewidth=0.4, label='MCC_H')
    ax2.bar(x + w, combined_leak, w, color=C_COMBINED, edgecolor='black', linewidth=0.4, label='MCC_H+D3')
    ax2.set_xticks(x)
    ax2.set_xticklabels(requesters, fontsize=6)
    ax2.set_ylabel('Leak rate (%)')
    ax2.set_ylim(0, 45)
    ax2.legend(fontsize=6, loc='upper right')
    add_panel_label(ax2, 'b')

    save(fig, 'arch_per_requester')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 3: Escalation Gate — PStop vs Utility (Phase 2)
# ═══════════════════════════════════════════════════════════════════════════════
def plot_escalation():
    fig, ax = plt.subplots(figsize=(4.0, 3.2))

    x = np.arange(len(esc_scopes))
    w = 0.18

    # GPT-5-mini
    ax.bar(x - 1.5*w, esc_pstop_mini, w, color=C_ESCALATION, alpha=0.6,
           edgecolor='black', linewidth=0.4, label='PStop (5-mini)')
    ax.bar(x - 0.5*w, esc_util_mini, w, color=C_ESCALATION, alpha=0.3,
           edgecolor='black', linewidth=0.4, label='Utility (5-mini)')

    # GPT-5.5
    ax.bar(x + 0.5*w, esc_pstop_55, w, color=C_COMBINED, alpha=0.8,
           edgecolor='black', linewidth=0.4, label='PStop (5.5)')
    ax.bar(x + 1.5*w, esc_util_55, w, color=C_COMBINED, alpha=0.35,
           edgecolor='black', linewidth=0.4, label='Utility (5.5)')

    ax.set_xticks(x)
    ax.set_xticklabels(esc_scopes, fontsize=6)
    ax.set_ylabel('Recall (%)')
    ax.set_ylim(0, 100)
    ax.axhline(y=90, color=C_DELTA_UP, linestyle='--', linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=5.5, ncol=2, loc='lower right')

    save(fig, 'arch_escalation_gate')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 4: Layered Defence Waterfall (aggregate leak rate reduction)
# ═══════════════════════════════════════════════════════════════════════════════
def plot_waterfall():
    fig, ax = plt.subplots(figsize=(3.5, 2.8))

    layers = ['D3\n(policy)', 'MCC_H\n(structure)', 'MCC_H+D3\n(combined)']
    leak_rates = [15.5, 12.4, 8.0]

    colors = [C_D3, C_MCC, C_COMBINED]

    bars = ax.bar(range(len(layers)), leak_rates, color=colors,
                  edgecolor='black', linewidth=0.6, width=0.55)

    for bar, val in zip(bars, leak_rates):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{val}%', ha='center', va='bottom', fontsize=7, fontweight='bold')

    ax.set_xticks(range(len(layers)))
    ax.set_xticklabels(layers, fontsize=6.5)
    ax.set_ylabel('Private/boundary disclosure rate (%)')
    ax.set_ylim(0, 20)

    for i in range(len(layers)-1):
        delta = leak_rates[i] - leak_rates[i+1]
        mid_x = i + 0.5
        mid_y = (leak_rates[i] + leak_rates[i+1]) / 2
        ax.annotate(f'−{delta:.1f}pp', xy=(mid_x, mid_y), fontsize=5.5,
                    ha='center', va='center', color=C_DELTA_DOWN, fontweight='bold')

    save(fig, 'arch_waterfall')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 5: Complementarity Matrix — Structure helps misaligned, policy helps aligned
# ═══════════════════════════════════════════════════════════════════════════════
def plot_complementarity():
    fig, ax = plt.subplots(figsize=(4.5, 3.0))

    req_short = ['R0\nStranger', 'R1\nColleague', 'R2\nDelegate', 'R3\nFriend', 'R4\nInvestor']

    # Delta from D3 to MCC_H (structure effect)
    struct_delta_leak = [mcc_leak[i] - d3_leak[i] for i in range(5)]
    # Delta from MCC_H to MCC_H+D3 (adding policy back)
    policy_delta_leak = [combined_leak[i] - mcc_leak[i] for i in range(5)]

    x = np.arange(5)
    w = 0.35

    bars1 = ax.bar(x - w/2, struct_delta_leak, w, color=C_MCC,
                   edgecolor='black', linewidth=0.4, label='D3 → MCC_H (structure effect)')
    bars2 = ax.bar(x + w/2, policy_delta_leak, w, color=C_D3,
                   edgecolor='black', linewidth=0.4, label='MCC_H → MCC_H+D3 (policy effect)')

    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(req_short, fontsize=6)
    ax.set_ylabel('Δ Leak rate (pp)')
    ax.legend(fontsize=5.5, loc='upper right')

    save(fig, 'arch_complementarity')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 6: Escalation Transfer Effect (decision change analysis)
# ═══════════════════════════════════════════════════════════════════════════════
def plot_escalation_transfer():
    fig, ax = plt.subplots(figsize=(4.0, 2.8))

    comparisons = ['indiv→cluster\n(5-mini)', 'indiv→cluster\n(5.5)',
                   'cluster→rich\n(5-mini)', 'cluster→rich\n(5.5)']
    changed_correct = [116, 83, 91, 32]
    changed_wrong = [53, 46, 64, 58]

    x = np.arange(len(comparisons))
    w = 0.35

    ax.bar(x - w/2, changed_correct, w, color=C_DELTA_UP, alpha=0.8,
           edgecolor='black', linewidth=0.4, label='Changed to correct')
    ax.bar(x + w/2, changed_wrong, w, color=C_DELTA_DOWN, alpha=0.7,
           edgecolor='black', linewidth=0.4, label='Changed to wrong')

    for i, (c, wr) in enumerate(zip(changed_correct, changed_wrong)):
        ratio = c / (c + wr)
        ax.text(i, max(c, wr) + 5, f'{ratio:.0%}', ha='center', fontsize=6, color='#4D4D4D')

    ax.set_xticks(x)
    ax.set_xticklabels(comparisons, fontsize=6)
    ax.set_ylabel('Decisions changed')
    ax.legend(fontsize=6)
    ax.set_ylim(0, 140)

    save(fig, 'arch_escalation_transfer')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 7: PACT-NET MCC Validation (Table 6.4 in thesis)
# Data: summary_mcc_h_mcc_h_d1_pact_net_v2.json — 4 conditions on 25-agent network
# ═══════════════════════════════════════════════════════════════════════════════
def plot_pact_net_mcc():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2))

    # Data from PACT-NET V2 summary JSON
    conditions = ['P0\n(no policy,\nno MCC)', 'P1\n(policy,\nno MCC)',
                  'MCC_H\n(no policy,\nMCC)', 'MCC_H+P1\n(policy\n+ MCC)']

    safety = [26.6, 71.5, 64.4, 77.8]
    utility = [88.7, 78.8, 23.1, 20.6]
    trans_leak = [96.3, 77.7, 77.7, 67.0]
    deputy = [47.0, 2.0, 6.0, 0.0]

    x = np.arange(4)
    w = 0.35

    # Panel a: Safety vs Utility
    bars_s = ax1.bar(x - w/2, safety, w, color=C_COMBINED, edgecolor='black',
                     linewidth=0.4, label='Safety')
    bars_u = ax1.bar(x + w/2, utility, w, color=C_MCC, edgecolor='black',
                     linewidth=0.4, label='Utility')
    ax1.set_xticks(x)
    ax1.set_xticklabels(conditions, fontsize=5.5)
    ax1.set_ylabel('Score (%)')
    ax1.set_ylim(0, 100)
    ax1.legend(fontsize=6)
    add_panel_label(ax1, 'a')

    # Panel b: Network-specific metrics
    C_TRANS = "#B64342"
    C_DEPUTY = "#E28E2C"
    bars_t = ax2.bar(x - w/2, trans_leak, w, color=C_TRANS, alpha=0.7,
                     edgecolor='black', linewidth=0.4, label='Transitive leak')
    bars_d = ax2.bar(x + w/2, deputy, w, color=C_DEPUTY, alpha=0.7,
                     edgecolor='black', linewidth=0.4, label='Confused deputy')
    ax2.set_xticks(x)
    ax2.set_xticklabels(conditions, fontsize=5.5)
    ax2.set_ylabel('Rate (%)')
    ax2.set_ylim(0, 100)
    ax2.legend(fontsize=6)
    add_panel_label(ax2, 'b')

    save(fig, 'arch_pact_net_mcc_validation')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 8: Combined MCC figure (frontier + waterfall + complementarity)
# Single image with matched heights for thesis Fig 6.1
# ═══════════════════════════════════════════════════════════════════════════════
def plot_ch6_mcc_combined():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(7.2, 2.8),
                                         gridspec_kw={"width_ratios": [1, 1, 1.3]})

    # ── Panel a: Frontier ──
    add_panel_label(ax1, 'a')
    ax1.scatter(d3_util[-1], d3_leak[-1], s=100, c=C_D3, zorder=5,
                edgecolors='black', linewidths=0.6)
    ax1.scatter(mcc_util[-1], mcc_leak[-1], s=100, c=C_MCC, zorder=5,
                edgecolors='black', linewidths=0.6)
    ax1.scatter(combined_util[-1], combined_leak[-1], s=100, c=C_COMBINED, zorder=5,
                edgecolors='black', linewidths=0.6)

    ax1.annotate('D3', (d3_util[-1], d3_leak[-1]),
                 xytext=(d3_util[-1]-2, d3_leak[-1]+1.0), fontsize=6,
                 ha='right', color=C_D3, fontweight='bold')
    ax1.annotate('MCC_H', (mcc_util[-1], mcc_leak[-1]),
                 xytext=(mcc_util[-1]+1.5, mcc_leak[-1]+1.0), fontsize=6,
                 ha='left', color=C_MCC, fontweight='bold')
    ax1.annotate('MCC_H+D3', (combined_util[-1], combined_leak[-1]),
                 xytext=(combined_util[-1]+1.5, combined_leak[-1]-1.0), fontsize=6,
                 ha='left', color=C_COMBINED, fontweight='bold')

    ax1.annotate('', xy=(combined_util[-1], combined_leak[-1]),
                 xytext=(d3_util[-1], d3_leak[-1]),
                 arrowprops=dict(arrowstyle='->', color='#767676', lw=0.8,
                                 connectionstyle='arc3,rad=-0.2'))
    ax1.set_xlabel('Utility (%)')
    ax1.set_ylabel('Leak rate (%)')
    ax1.set_xlim(45, 80)
    ax1.set_ylim(0, 20)
    ax1.axhline(y=10, color=C_NEUTRAL, linestyle='--', linewidth=0.5, zorder=0)
    ax1.set_title("Security–utility frontier", fontsize=7, fontweight="bold")

    # ── Panel b: Waterfall ──
    add_panel_label(ax2, 'b')
    layers = ['D3', 'MCC_H', 'MCC_H\n+D3']
    leak_rates = [15.5, 12.4, 8.0]
    colors = [C_D3, C_MCC, C_COMBINED]

    bars = ax2.bar(range(len(layers)), leak_rates, color=colors,
                   edgecolor='black', linewidth=0.6, width=0.55)
    for bar, val in zip(bars, leak_rates):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                 f'{val}%', ha='center', va='bottom', fontsize=6.5, fontweight='bold')
    ax2.set_xticks(range(len(layers)))
    ax2.set_xticklabels(layers, fontsize=6.5)
    ax2.set_ylabel('Leak rate (%)')
    ax2.set_ylim(0, 20)
    for i in range(len(layers)-1):
        delta = leak_rates[i] - leak_rates[i+1]
        mid_x = i + 0.5
        mid_y = (leak_rates[i] + leak_rates[i+1]) / 2
        ax2.annotate(f'−{delta:.1f}pp', xy=(mid_x, mid_y), fontsize=5.5,
                     ha='center', va='center', color=C_DELTA_DOWN, fontweight='bold')
    ax2.set_title("Progressive leak reduction", fontsize=7, fontweight="bold")

    # ── Panel c: Complementarity ──
    add_panel_label(ax3, 'c')
    req_short = ['R0', 'R1', 'R2', 'R3', 'R4']
    struct_delta_leak = [mcc_leak[i] - d3_leak[i] for i in range(5)]
    policy_delta_leak = [combined_leak[i] - mcc_leak[i] for i in range(5)]
    x = np.arange(5)
    w = 0.35
    ax3.bar(x - w/2, struct_delta_leak, w, color=C_MCC,
            edgecolor='black', linewidth=0.4, label='Structure effect')
    ax3.bar(x + w/2, policy_delta_leak, w, color=C_D3,
            edgecolor='black', linewidth=0.4, label='Policy effect')
    ax3.axhline(0, color='black', linewidth=0.5)
    ax3.set_xticks(x)
    ax3.set_xticklabels(req_short, fontsize=6.5)
    ax3.set_ylabel('Δ Leak rate (pp)')
    ax3.legend(fontsize=5.5, loc='upper right')
    ax3.set_title("Per-requester decomposition", fontsize=7, fontweight="bold")

    save(fig, 'arch_ch6_mcc_combined')


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 9: Combined escalation figure (2 rows)
# Row 1: PStop–Utility frontier scatter
# Row 2: Scope comparison (a: PStop, b: Utility) + Error decomposition
# ═══════════════════════════════════════════════════════════════════════════════
def plot_ch6_escalation_combined():
    fig = plt.figure(figsize=(7.2, 5.0))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.1], hspace=0.4, wspace=0.35)

    # ── Row 1: PStop–Utility frontier (spans full width) ──
    ax_top = fig.add_subplot(gs[0, :])
    add_panel_label(ax_top, 'a', x=-0.04)

    scope_labels_short = ['indiv-10%', 'clust-10%', 'rich-10%', 'indiv-30%']
    for i, (ps_m, u_m, ps_5, u_5) in enumerate(zip(esc_pstop_mini, esc_util_mini,
                                                      esc_pstop_55, esc_util_55)):
        ax_top.scatter(u_m, ps_m, s=80, color=C_ESCALATION, alpha=0.7,
                       edgecolors='black', linewidths=0.5, zorder=3)
        ax_top.scatter(u_5, ps_5, s=80, color=C_COMBINED, alpha=0.7,
                       edgecolors='black', linewidths=0.5, zorder=3)
        ax_top.annotate(scope_labels_short[i], (u_m, ps_m),
                        xytext=(u_m-1, ps_m-1.5), fontsize=5, ha='right', color=C_ESCALATION)
        ax_top.annotate(scope_labels_short[i], (u_5, ps_5),
                        xytext=(u_5+1, ps_5+0.8), fontsize=5, ha='left', color=C_COMBINED)

    ax_top.scatter([], [], s=60, color=C_ESCALATION, label='GPT-5-mini')
    ax_top.scatter([], [], s=60, color=C_COMBINED, label='GPT-5.5')
    ax_top.legend(fontsize=6, loc='lower right')
    ax_top.set_xlabel('Utility (%)')
    ax_top.set_ylabel('PStop (%)')
    ax_top.set_xlim(60, 95)
    ax_top.set_ylim(85, 97)
    ax_top.axhline(90, color=C_DELTA_UP, linestyle='--', linewidth=0.5, alpha=0.6)
    ax_top.set_title("PStop vs. Utility frontier", fontsize=7, fontweight="bold")

    # ── Row 2 left: Scope PStop ──
    ax_bl = fig.add_subplot(gs[1, 0])
    add_panel_label(ax_bl, 'b', x=-0.15)
    x = np.arange(len(esc_scopes))
    w = 0.35
    ax_bl.bar(x - w/2, esc_pstop_mini, w, color=C_ESCALATION, alpha=0.7,
              edgecolor='black', linewidth=0.4, label='5-mini')
    ax_bl.bar(x + w/2, esc_pstop_55, w, color=C_COMBINED, alpha=0.7,
              edgecolor='black', linewidth=0.4, label='5.5')
    ax_bl.set_xticks(x)
    ax_bl.set_xticklabels(esc_scopes, fontsize=5)
    ax_bl.set_ylabel('PStop (%)')
    ax_bl.set_ylim(82, 100)
    ax_bl.legend(fontsize=5, loc='lower right')
    ax_bl.set_title("PStop by scope", fontsize=6.5, fontweight="bold")

    # ── Row 2 centre: Scope Utility ──
    ax_bm = fig.add_subplot(gs[1, 1])
    add_panel_label(ax_bm, 'c', x=-0.15)
    ax_bm.bar(x - w/2, esc_util_mini, w, color=C_ESCALATION, alpha=0.7,
              edgecolor='black', linewidth=0.4, label='5-mini')
    ax_bm.bar(x + w/2, esc_util_55, w, color=C_COMBINED, alpha=0.7,
              edgecolor='black', linewidth=0.4, label='5.5')
    ax_bm.set_xticks(x)
    ax_bm.set_xticklabels(esc_scopes, fontsize=5)
    ax_bm.set_ylabel('Utility (%)')
    ax_bm.set_ylim(55, 100)
    ax_bm.legend(fontsize=5, loc='lower right')
    ax_bm.set_title("Utility by scope", fontsize=6.5, fontweight="bold")

    # ── Row 2 right: Error decomposition ──
    ax_br = fig.add_subplot(gs[1, 2])
    add_panel_label(ax_br, 'd', x=-0.15)
    false_cont_mini = [100-p for p in esc_pstop_mini]
    false_stop_mini = [100-u for u in esc_util_mini]
    false_cont_55 = [100-p for p in esc_pstop_55]
    false_stop_55 = [100-u for u in esc_util_55]

    w2 = 0.2
    ax_br.bar(x - 1.5*w2, false_cont_mini, w2, color=C_ESCALATION, alpha=0.9,
              edgecolor='black', linewidth=0.4, label='F-cont (5-mini)')
    ax_br.bar(x - 0.5*w2, false_stop_mini, w2, color=C_ESCALATION, alpha=0.35,
              edgecolor='black', linewidth=0.4, label='F-stop (5-mini)')
    ax_br.bar(x + 0.5*w2, false_cont_55, w2, color=C_COMBINED, alpha=0.9,
              edgecolor='black', linewidth=0.4, label='F-cont (5.5)')
    ax_br.bar(x + 1.5*w2, false_stop_55, w2, color=C_COMBINED, alpha=0.35,
              edgecolor='black', linewidth=0.4, label='F-stop (5.5)')
    ax_br.set_xticks(x)
    ax_br.set_xticklabels(esc_scopes, fontsize=5)
    ax_br.set_ylabel('Error rate (%)')
    ax_br.set_ylim(0, 40)
    ax_br.legend(fontsize=4.5, ncol=2, loc='upper right')
    ax_br.set_title("Error decomposition", fontsize=6.5, fontweight="bold")

    save(fig, 'arch_ch6_escalation_combined')


# ═══════════════════════════════════════════════════════════════════════════════
# Run all
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating Architectural Solutions (Chapter 6) figures...")
    plot_frontier()
    plot_per_requester()
    plot_escalation()
    plot_waterfall()
    plot_complementarity()
    plot_escalation_transfer()
    plot_pact_net_mcc()
    plot_ch6_mcc_combined()
    plot_ch6_escalation_combined()
    print("Done.")
