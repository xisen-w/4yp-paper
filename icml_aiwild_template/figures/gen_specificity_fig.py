"""Generate Figure 2: Policy specificity across three surfaces (3-panel wide figure).

Files QA panel averages gpt-5-mini + GPT-5.5 (both LLM judge).
States QA and Actions panels use gpt-5-mini only (sole model with LLM judge data).

Data sources (all verified 2026-05-07):
  - Files QA (gpt-5-mini): thesis/results/layer0_single_step/ss_eval_llm.json (g401-g406, 2 reps)
  - Files QA (GPT-5.5):    thesis/results/layer0_single_step/cross_model/gpt55_eval/ (g2040/2042/2044, 1 rep)
  - States QA:             thesis/results/layer0_single_step/ss_todo_eval_llm.json (gpt-5-mini, g401-g406)
  - Actions:               research/runs/v2/eval_output/eval_actions.json (gpt-5-mini, g401-g406)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# === DATA ===

# --- Files QA: average of gpt-5-mini (2 reps pooled) + GPT-5.5 (1 rep) ---
# gpt-5-mini LLM judge (g401+g404=D0, g402+g405=D1, g403+g406=D2)
# Categories: sensitive_work (30/rep→60), personal_finance (25→50), personal_health (20→40), personal_relationships (25→50)
mini_files_d0 = [(25+27)/60*100, (22+22)/50*100, (14+15)/40*100, (22+19)/50*100]  # 86.7, 88.0, 72.5, 82.0
mini_files_d1 = [(25+26)/60*100, (18+19)/50*100, (18+19)/40*100, (22+16)/50*100]  # 85.0, 74.0, 92.5, 76.0
mini_files_d2 = [(9+8)/60*100,   (0+2)/50*100,   (1+4)/40*100,   (1+3)/50*100]   # 28.3,  4.0, 12.5,  8.0

# GPT-5.5 LLM judge (g2040=D0, g2042=D1, g2044=D2)
# Categories: sensitive_work (60/45), personal_finance (49/37), personal_health (40/30), personal_relationships (51/38)
gpt55_files_d0 = [48/60*100, 38/49*100, 31/40*100, 36/51*100]  # 80.0, 77.6, 77.5, 70.6
gpt55_files_d1 = [42/60*100, 33/49*100, 25/40*100, 36/51*100]  # 70.0, 67.3, 62.5, 70.6
gpt55_files_d2 = [4/45*100,  2/37*100,  4/30*100,  0/38*100]   #  8.9,  5.4, 13.3,  0.0

# Averaged across both models
files_d0 = [(a + b) / 2 for a, b in zip(mini_files_d0, gpt55_files_d0)]
files_d1 = [(a + b) / 2 for a, b in zip(mini_files_d1, gpt55_files_d1)]
files_d2 = [(a + b) / 2 for a, b in zip(mini_files_d2, gpt55_files_d2)]

# --- States QA: gpt-5-mini only (LLM judge, pooled 2 reps) ---
# Source: ss_todo_eval_llm.json → g401+g404 (D0), g402+g405 (D1), g403+g406 (D2)
# Categories: sensitive_work (30/rep→60), personal_finance (24→48), personal_health (20→40), personal_relationships (26→52)
states_d0 = [(20+21)/60*100, (14+15)/48*100, (10+13)/40*100, (14+10)/52*100]
states_d1 = [(17+21)/60*100, (14+15)/48*100, (15+12)/40*100, (14+18)/52*100]
states_d2 = [(4+6)/60*100,   (0+1)/48*100,   (0+1)/40*100,   (1+3)/52*100]

# --- Actions: gpt-5-mini only (DB-diff ground truth, pooled 2 reps) ---
# Source: eval_actions.json
# edit_sensitive (20/rep→40), wipe (16→32), create_sensitive (16→32), overall unauthorized (100→200)
actions_d0 = [30/40*100, 19/32*100, 16/32*100, 114/200*100]
actions_d1 = [23/40*100, 19/32*100, 16/32*100, 114/200*100]
actions_d2 = [0/40*100,  0/32*100,  0/32*100,  13/200*100]

# Category labels
files_cats = ['Sensitive\nWork', 'Personal\nFinance', 'Personal\nHealth', 'Personal\nRelationships']
states_cats = files_cats
actions_cats = ['Edit\nSensitive', 'Wipe\nAll Data', 'Create\nSensitive', 'Overall\nUnauthorised']

# === PLOT ===
fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)

width = 0.24
colors = {'D0': '#d62728', 'D1': '#ff7f0e', 'D2': '#1f77b4'}

panels = [
    ('Files QA — Leak Rate', files_cats, files_d0, files_d1, files_d2),
    ('States QA — Leak Rate', states_cats, states_d0, states_d1, states_d2),
    ('Actions — Unsafe Rate', actions_cats, actions_d0, actions_d1, actions_d2),
]

for ax, (title, cats, d0, d1, d2) in zip(axes, panels):
    x = np.arange(len(cats))
    ax.bar(x - width, d0, width, color=colors['D0'], alpha=0.85)
    ax.bar(x,         d1, width, color=colors['D1'], alpha=0.85)
    ax.bar(x + width, d2, width, color=colors['D2'], alpha=0.85)

    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=9)
    ax.set_ylim(0, 109)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, alpha=0.3, linestyle='--')

    # Drop annotations from D0 to D2
    for i in range(len(cats)):
        drop = d0[i] - d2[i]
        if drop > 3:
            ax.annotate(f'−{drop:.0f}',
                        xy=(x[i] + width, d2[i] + 2),
                        fontsize=7.5, color='#1f77b4', fontweight='bold',
                        ha='center', va='bottom')

axes[0].set_ylabel('Rate (%)', fontsize=11)

# Shared legend
handles = [plt.Rectangle((0, 0), 1, 1, color=colors['D0'], alpha=0.85),
           plt.Rectangle((0, 0), 1, 1, color=colors['D1'], alpha=0.85),
           plt.Rectangle((0, 0), 1, 1, color=colors['D2'], alpha=0.85)]
fig.legend(handles, ['D0 (no policy)', 'D1 (generic)', 'D2 (deny list)'],
           loc='upper center', ncol=3, fontsize=10, framealpha=0.9,
           bbox_to_anchor=(0.5, 1.02))

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('/Users/wangxiang/Desktop/my_workspace/pulse/thesis/neurips/figures/fig_specificity.pdf',
            dpi=300, bbox_inches='tight')
plt.savefig('/Users/wangxiang/Desktop/my_workspace/pulse/thesis/neurips/figures/fig_specificity.png',
            dpi=200, bbox_inches='tight')
print("Saved fig_specificity.pdf and .png (3-panel)")
print()
print("Files QA (averaged gpt-5-mini + GPT-5.5):")
print(f"  D0: {[f'{v:.1f}%' for v in files_d0]}")
print(f"  D1: {[f'{v:.1f}%' for v in files_d1]}")
print(f"  D2: {[f'{v:.1f}%' for v in files_d2]}")
print(f"  Mean drop D0→D2: {sum(files_d0)/4 - sum(files_d2)/4:.1f}pp")
