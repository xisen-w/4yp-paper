"""Generate Figure: Security-Utility Frontier (4 versions × 3 panels each).

Each version uses a different security metric on the x-axis:
  1. Refuse Rate
  2. Message Security (100 - msg leak)
  3. Global Security (100 - glob leak)
  4. Failed Attempt Rate

All panels: y = Utility (%).
Panel layout: [Policy | Erosion | Relationship]

Data sources (all verified 2026-05-07):
  - Panel 1: Cross-model single-step files QA (Table 4)
  - Panel 2: SS vs MS, 2 models (Tables 1,2 + appendix GPT-5.5)
  - Panel 3: Relationship aggregate (eval_relationship_aware.json)
             Evaluated on RELATIONSHIP-SPECIFIC labels (P/L per requester)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# DATA
# =============================================================================

# --- PANEL 1: Cross-model × policy (single-step files QA) ---
panel1_data = [
    # (model, policy, utility, refuse, msg_leak)
    ('gpt-5-mini', 'D0', 78, 0, 83),
    ('gpt-5-mini', 'D1', 79, 3, 81),
    ('gpt-5-mini', 'D2', 77, 72, 14),
    ('gpt-5.5', 'D0', 87, 1, 88),
    ('gpt-5.5', 'D1', 94, 7, 75),
    ('gpt-5.5', 'D2', 86, 78, 4),
    ('gpt-5.4-mini', 'D0', 96, 1, 87),
    ('gpt-5.4-mini', 'D1', 99, 5, 90),
    ('gpt-5.4-mini', 'D2', 91, 89, 7),
    ('gpt-5.4', 'D0', 98, 1, 92),
    ('gpt-5.4', 'D1', 97, 12, 80),
    ('gpt-5.4', 'D2', 74, 93, 1),
    ('Kimi K2', 'D0', 82, 0, 93),
    ('Kimi K2', 'D1', 86, 3, 87),
    ('Kimi K2', 'D2', 81, 86, 4),
    ('DeepSeek V3', 'D0', 91, 1, 93),
    ('DeepSeek V3', 'D1', 97, 2, 80),
    ('DeepSeek V3', 'D2', 62, 90, 9),
]

# --- PANEL 2: Erosion over time (cumulative leak curve) ---
# Source: V2 gold scan (bestTick field) for both models.
# Same method, same denominator (200 security Qs per level).
# x = tick number, y = cumulative % of security pool leaked.
# Extracted from eval_v2_gold_scan_gpt5mini.json and eval_v2_gold_scan.json (GPT-5.5).
# Tick bins: [10, 20, 40, 60, 100, 150, 200, 240]
panel2_ticks = [10, 20, 40, 60, 100, 150, 200, 240]
# gpt-5-mini cumulative leak % (of 200 security Qs)
panel2_mini = {
    'D0': [3.5, 45.5, 73.5, 76.0, 76.5, 77.5, 77.5, 77.5],
    'D1': [5.5, 40.5, 67.0, 72.5, 72.5, 73.0, 74.0, 74.5],
    'D2': [1.5, 3.5, 14.5, 18.5, 22.0, 24.0, 28.0, 29.0],
}
# GPT-5.5 cumulative leak % (of 200 security Qs)
panel2_55 = {
    'D0': [3.5, 7.0, 14.0, 16.0, 17.0, 26.5, 33.5, 36.5],
    'D1': [3.5, 4.5, 10.0, 11.5, 14.0, 22.5, 29.5, 31.5],
    'D2': [3.0, 3.5, 8.0, 10.0, 12.5, 16.5, 18.5, 19.5],
}

# --- PANEL 3: Relationship dual-failure (D2, gpt-5-mini) ---
# From l1_final_summary.md — relationship-specific labels
# Total P-item leak rate (all categories; driven by sensitive_work — others ≤5%)
# Over-refusal rate on L-items (utility failure — agent blocks legitimate requests)
panel3_requesters = ['Tina\n(Colleague)', 'Marcus\n(Boss)', 'Jordan\n(Friend)', 'Dana\n(Investor)']
panel3_leak = [1.7, 3.3, 9.2, 7.5]            # total P-item leak (OR-adjudicated)
panel3_overrefusal = [40.0, 59.2, 86.4, 31.2]  # L-items refused / L-pool

# =============================================================================
# STYLE
# =============================================================================

policy_colors = {'D0': '#d62728', 'D1': '#ff7f0e', 'D2': '#1f77b4'}
model_markers = {
    'gpt-5-mini': 'o', 'gpt-5.5': 's', 'gpt-5.4-mini': '^',
    'gpt-5.4': 'D', 'Kimi K2': 'P', 'DeepSeek V3': 'X'
}
model_names_short = {
    'gpt-5-mini': '5-mini', 'gpt-5.5': '5.5', 'gpt-5.4-mini': '5.4-mini',
    'gpt-5.4': '5.4', 'Kimi K2': 'Kimi', 'DeepSeek V3': 'DS-V3'
}

rel_colors = {
    'Tina\n(Colleague)': '#2ca02c',
    'Marcus\n(Boss)': '#9467bd',
    'Jordan\n(Friend)': '#e377c2',
    'Dana\n(Investor)': '#17becf',
}
rel_markers = {
    'Tina\n(Colleague)': 'o',
    'Marcus\n(Boss)': 's',
    'Jordan\n(Friend)': '^',
    'Dana\n(Investor)': 'D',
}


def make_figure(metric_name, x_label, get_x_fn, filename_suffix):
    """Create one 3-panel figure for a given security metric."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))

    # =========================================================================
    # Panel 1: Policy × Model
    # =========================================================================
    ax = axes[0]
    for model, policy, util, refuse, msg_leak in panel1_data:
        x = get_x_fn(refuse, msg_leak, msg_leak)
        ax.scatter(x, util, c=policy_colors[policy], marker=model_markers[model],
                   s=90, alpha=0.85, edgecolors='white', linewidths=0.5, zorder=3)

    policy_handles = []
    for policy, color in policy_colors.items():
        h = ax.scatter([], [], c=color, marker='o', s=60, alpha=0.85)
        policy_handles.append((h, policy))
    model_handles = []
    for model, marker in model_markers.items():
        h = ax.scatter([], [], c='gray', marker=marker, s=60, alpha=0.7)
        model_handles.append((h, model_names_short[model]))
    all_handles = [h for h, _ in policy_handles] + [h for h, _ in model_handles]
    all_labels = [l for _, l in policy_handles] + [l for _, l in model_handles]
    ax.legend(all_handles, all_labels, loc='lower left', fontsize=7.5,
              ncol=2, framealpha=0.9, columnspacing=1.0)

    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel('Utility (%)', fontsize=11)
    ax.set_title('Policy Specificity\n(6 models × 3 policies, files QA)', fontsize=11, fontweight='bold')
    ax.set_xlim(-5, 105)
    ax.set_ylim(55, 102)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.2, linestyle='--')

    # =========================================================================
    # Panel 2: Cumulative leak over time (tick-level erosion)
    # =========================================================================
    ax = axes[1]

    # gpt-5-mini (solid lines)
    for policy, vals in panel2_mini.items():
        ax.plot(panel2_ticks, vals, color=policy_colors[policy], linewidth=2.2,
                alpha=0.9, marker='o', markersize=5, zorder=4)

    # GPT-5.5 (dashed lines)
    for policy, vals in panel2_55.items():
        ax.plot(panel2_ticks, vals, color=policy_colors[policy], linewidth=1.8,
                alpha=0.7, linestyle='--', marker='s', markersize=4, zorder=3)

    # Phase boundary
    ax.axvline(60, color='gray', linestyle=':', alpha=0.5, linewidth=1)
    ax.text(62, 75, 'Phase 2\n(retries)', fontsize=7.5, color='gray', va='top')

    # Legend
    for policy, color in policy_colors.items():
        ax.plot([], [], color=color, linewidth=2, label=policy)
    ax.plot([], [], color='gray', linewidth=2, linestyle='-', label='gpt-5-mini')
    ax.plot([], [], color='gray', linewidth=1.5, linestyle='--', label='GPT-5.5')
    ax.legend(loc='upper left', fontsize=7.5, ncol=2, framealpha=0.9, columnspacing=0.8)

    ax.set_xlabel('Tick (interaction turn)', fontsize=10)
    ax.set_ylabel('Cumulative Leak (%)', fontsize=11)
    ax.set_title('Multi-Turn Erosion\n(cumulative leakage over 240 ticks)', fontsize=11, fontweight='bold')
    ax.set_xlim(0, 245)
    ax.set_ylim(0, 82)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.2, linestyle='--')

    # =========================================================================
    # Panel 3: Relationship — dual-failure bars (leak + over-refusal)
    # =========================================================================
    ax = axes[2]

    x_pos = np.arange(len(panel3_requesters))
    width = 0.35
    bars1 = ax.bar(x_pos - width/2, panel3_leak, width,
                   color='#d62728', alpha=0.85, label='Leak rate (P-items)')
    bars2 = ax.bar(x_pos + width/2, panel3_overrefusal, width,
                   color='#1f77b4', alpha=0.85, label='Over-refusal (L-items)')

    # Value annotations
    for bar in bars1:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2, h + 1.5, f'{h:.0f}%',
                    ha='center', va='bottom', fontsize=8, color='#d62728', fontweight='bold')
    for bar in bars2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1.5, f'{h:.0f}%',
                ha='center', va='bottom', fontsize=8, color='#1f77b4', fontweight='bold')

    ax.set_xticks(x_pos)
    ax.set_xticklabels([r.replace('\n', '\n') for r in panel3_requesters], fontsize=9)
    ax.set_ylabel('Rate (%)', fontsize=11)
    ax.set_ylim(0, 105)
    ax.set_title('Relationship: Dual Failure\n(D2, gpt-5-mini, rel.-specific labels)', fontsize=11, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    out_base = f'/Users/wangxiang/Desktop/my_workspace/pulse/thesis/neurips/figures/fig_frontier_{filename_suffix}'
    plt.savefig(f'{out_base}.pdf', dpi=300, bbox_inches='tight')
    plt.savefig(f'{out_base}.png', dpi=200, bbox_inches='tight')
    plt.close()
    print(f'  Saved {out_base}.pdf/.png')


# =============================================================================
# GENERATE ALL 4 VERSIONS
# =============================================================================

print('Generating frontier plots...\n')

make_figure('Refuse Rate', 'Refuse Rate (%)',
            lambda refuse, msg_leak, glob_leak: refuse, 'refuse')

make_figure('Message Security', 'Security (100 − Msg Leak %)',
            lambda refuse, msg_leak, glob_leak: 100 - msg_leak, 'msg_security')

make_figure('Global Security', 'Security (100 − Global Leak %)',
            lambda refuse, msg_leak, glob_leak: 100 - glob_leak, 'glob_security')

make_figure('Failed Attempt Rate', 'Failed Attempt Rate (%)',
            lambda refuse, msg_leak, glob_leak: max(0, 100 - refuse - msg_leak), 'fail_att')

print('\nDone. 4 figures × (pdf + png) = 8 files generated.')
