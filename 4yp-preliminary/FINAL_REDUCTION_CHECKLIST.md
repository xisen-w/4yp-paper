# 4YP Final Reduction Checklist

Use this as the freeze tracker for the main thesis source of truth:
`pulse_4yp_thesis.tex`.

Approximate word counts are rough source-level counts from the `.tex` files, used
only to guide reduction decisions.

## Chapter Checklist

| Ch. | Chapter | Source | Approx. words | Plots ready? | Word count ready? | Final read? | Notes |
|---:|---|---|---:|:---:|:---:|:---:|---|
| 1 | Introduction | `chap_introduction.tex` | 1,062 | [ ] | [ ] | [ ] | Check story promise matches final Chapter 6 claims. |
| 2 | Related Work | `chap_literature_review.tex` | 987 | [ ] | [ ] | [ ] | Keep only work needed for benchmark + infrastructure claims. |
| 3a | Problem Formulation & SharedOS | `chap_problem_setup.tex` | 983 | [ ] | [ ] | [ ] | Needs one clean security/utility case figure or example. |
| 3b | SharedOS Implementation | `engineering_implementation_sharedos.tex` | 1,611 | [ ] | [ ] | [ ] | Cut implementation details unless they support the formal setting. |
| 4 | PACT-PAIR: Dyadic Evaluation | `chap_architecture.tex` | 3,050 | [ ] | [ ] | [ ] | Tables tightened; final pass should check D0/D1/D2/D3/MCC naming. |
| 5 | PACT-NET: Network Evaluation | `chap_failure_cases.tex` | 1,266 | [ ] | [ ] | [ ] | Use P0/P1 framing; four findings: transitive, cross-cluster, amplification, confused deputy. |
| 6 | Architectural Solutions | `chap_solution_proposal.tex` | 2,400 | [ ] | [ ] | [ ] | Attribute results to relationship policy, MCC, escalation separately. |
| 7 | Conclusion & Discussion | `chap_experiments.tex` | 919 | [ ] | [ ] | [ ] | Make claims conservative and aligned with audited experiments. |

## Available Plots by Chapter

All plots use Nature-figure style (Arial, no top/right spines, 7pt base, editable SVG text, 600 DPI).
Unified palette: gold (#E28E2C), teal (#42949E), navy (#0F4D92), red (#B64342), green (#2E9E44). No purple.

---

### Chapter 3: Problem Formulation & SharedOS

Already in `4yp-preliminary/figures/`:
- `shared_os_overview.png` — system architecture diagram (currently referenced)

No additional Nature-style plots generated. Consider adding a conceptual security–utility frontier sketch if space allows.

---

### Chapter 4: PACT-PAIR Dyadic Evaluation

Already in `4yp-preliminary/figures/` (currently referenced in .tex):
- `fig_specificity.pdf` — D0/D1/D2 comparison across surfaces
- `erosion-case-study-final.png` — multi-turn erosion case study (wedding cascade)
- `fig_frontier_msg_security.pdf` — three-panel frontier (specificity, cumulative leak, relationship)

No new Nature-style plots needed — Ch4 is fully figured.

---

### Chapter 5: PACT-NET Network Evaluation

**Primary plots** (`results/pact_net/plots/`):

| # | File | Description | Recommended? |
|---|------|-------------|:---:|
| 1 | `pact_net_frontier.pdf` | P0→P1 security–utility frontier (2-point scatter with arrow) | |
| 2 | `pact_net_bimodal_effectiveness.pdf` | Dumbbell chart: bilateral (policy-responsive) vs network-native (policy-resistant) | **★★★** |
| 3 | `pact_net_family_accuracy.pdf` | Grouped bar: all 10 task families P0 vs P1 | |
| 4 | `pact_net_four_findings.pdf` | 2×2 panel: F1 transitive, F2 cross-cluster, F3 amplification, F4 confused deputy | **★★** |
| 5 | `pact_net_utility_cost.pdf` | Utility cost decomposition (over-refusal on 3 legitimate families) | |
| 6 | `pact_net_protection_heatmap.pdf` | 10×2 heatmap, all families P0 vs P1 correct rate | |
| 7 | `pact_net_residual_gap.pdf` | Residual leak under P1: transitive 77.7%, cross-cluster 69.6%, deputy 2.0% | **★★** |
| 8 | `pact_net_improvement_sorted.pdf` | Horizontal bar: sorted P0→P1 delta per family | |

**Legacy/older versions** (`results/pact_net/plots/nature/`):
- `nature_pact_net_frontier.pdf`
- `nature_pact_net_four_findings.pdf`
- `nature_pact_net_policy_effect_scatter.pdf`
- `nature_pact_net_task_family_matrix.pdf`

Use the primary plots (updated palette, unified style). Legacy plots are superseded.

---

### Chapter 6: Architectural Solutions

**§6.1–6.2 MCC + D3 plots** (`results/pact_pair_d3_mcc/plots/`):

| # | File | Description | Recommended? |
|---|------|-------------|:---:|
| 1 | `arch_frontier.pdf` | 3-point scatter: D3, MCC_H, MCC_H+D3 on security–utility plane | |
| 2 | `arch_per_requester.pdf` | 2-panel grouped bar: utility (a) and leak rate (b) per requester × 3 conditions | **★★★** |
| 3 | `arch_waterfall.pdf` | Progressive leak reduction: 15.5% → 12.4% → 8.0% | **★★★** |
| 4 | `arch_complementarity.pdf` | Delta decomposition: structure effect vs policy effect per requester | **★★** |
| 5 | `arch_pact_net_mcc_validation.pdf` | 2-panel: safety/utility + transitive/deputy for P0/P1/MCC_H/MCC_H+P1 | **★★** |
| 6 | `arch_escalation_gate.pdf` | PStop + Utility across 4 scope conditions × 2 models | |
| 7 | `arch_escalation_transfer.pdf` | Decision change analysis (correct vs wrong) | |

**§6.3 Escalation Protocol plots** (`results/escalation_protocol/plots/`):

| # | File | Description | Recommended? |
|---|------|-------------|:---:|
| 1 | `esc_pstop_utility_frontier.pdf` | Scatter: PStop vs Utility for all 8 (scope, model) conditions | **★★** |
| 2 | `esc_scope_comparison.pdf` | 2-panel grouped bar: PStop (a) and Utility (b) by scope | **★★★** |
| 3 | `esc_error_decomposition.pdf` | False-continue vs false-stop by scope and model | **★★** |
| 4 | `esc_per_category.pdf` | 2-panel: per-category PStop (a) and Utility (b) for GPT-5.5 | |
| 5 | `esc_transfer_delta.pdf` | Δ PStop and Δ Utility from scope expansion | |
| 6 | `esc_decision_change.pdf` | Correct vs wrong decisions changed (transfer quality) | |

**Legacy/older** (`results/pact_pair_d3_mcc/plots/` — non-arch prefix):
- `pact_net_defence_ladder.pdf`
- `pact_net_network_radar.pdf`
- `pact_net_safety_utility_tradeoff.pdf`
- `pact_net_task_family_bar.pdf`
- `pact_net_transitive_progression.pdf`

These are superseded by the `arch_*` and `esc_*` plots above.

---

### Summary: Recommended Minimum Figure Set

| Chapter | Recommended plots (pick 2–3) | Rationale |
|---------|------------------------------|-----------|
| Ch 5 | `pact_net_bimodal_effectiveness` + `pact_net_four_findings` or `pact_net_residual_gap` | Bimodal is the chapter's thesis; four_findings or residual_gap quantifies |
| Ch 6 §6.1–2 | `arch_per_requester` + `arch_waterfall` + `arch_pact_net_mcc_validation` | Complementarity + progressive reduction + network validation |
| Ch 6 §6.3 | `esc_scope_comparison` + `esc_pstop_utility_frontier` | Core table visualization + trade-off space |

Total new figures to add: **5–7** (currently Ch5 and Ch6 have zero figures)

## Final Freeze Checks

| Check | Status | Notes |
|---|:---:|---|
| All result claims trace to audited result folders | [ ] | No Phase 1 escalation stats in main thesis unless explicitly framed as superseded. |
| No obsolete D2/D3 terminology in PACT-NET chapter | [ ] | Use P0/P1 for PACT-NET main benchmark. |
| Relationship-specific policy results clearly separated from PACT-NET P1 | [ ] | P1 is per-agent static policy; relationship-specific policy belongs to PACT-PAIR / solution chapter. |
| MCC claims specify whether pure MCC or MCC + policy | [ ] | Avoid saying pure MCC when condition is combined. |
| Escalation claims specify gate-only evaluation, not full pipeline | [ ] | Mention tool-gate abstraction and current query-to-tool simplification. |
| All figures have white background and readable text at thesis scale | [ ] | Prefer PDF insertion for vector text where possible. |
| Final PDF rendered and page count accepted | [ ] | Latest known render: `pulse_4yp_thesis_v27.pdf`. |
