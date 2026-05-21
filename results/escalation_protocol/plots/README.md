# Escalation Protocol Plots — Chapter 6, §6.3 Figures

All figures use Nature-figure style (Arial, no top/right spines, editable SVG text).
No in-image captions. Data from Phase 2 experiment (question-group splits, no auto-decision).

---

## Figure Index

### 1. `esc_pstop_utility_frontier`
**Caption:** Security–utility frontier for the escalation gate across four scope conditions and two gate models. Each point represents one (scope, model) condition. GPT-5.5 (squares) consistently achieves higher PStop than GPT-5-mini (circles) at the cost of lower utility. The 30% same-pair condition (upper-right cluster) achieves the best balance for both models, while 10% conditions trade utility for security. The 90% PStop reference line marks the target security threshold.

---

### 2. `esc_scope_comparison`
**Caption:** PStop (a) and Utility (b) across four precedent scopes for both gate models. Key finding: with only 10% same-pair precedents, both models achieve PStop above 90% (GPT-5.5: 94.2%). The utility gap between 10% and 30% (67→87% for GPT-5.5, 70→91% for GPT-5-mini) quantifies the cost of sparse labelling. Cluster transfer and rich cards narrow this gap at 10% by 4–8pp utility without materially reducing PStop.

---

### 3. `esc_error_decomposition`
**Caption:** Error type decomposition by scope and model. False continue (security failure: private request incorrectly allowed) is consistently below 12% across all conditions, with GPT-5.5 achieving only 5.6–7.9%. False stop (utility failure: legitimate request incorrectly blocked) dominates the error budget, reaching 30–33% at 10% precedents but dropping to 9–13% at 30%. The asymmetry confirms that sparse-precedent escalation is conservative-by-default: it fails toward safety, not toward leakage.

---

### 4. `esc_per_category`
**Caption:** Per-category PStop (a) and Utility (b) for GPT-5.5 at 10% precedents across three scope conditions. Should-refuse achieves near-perfect PStop (96.5–97.9%) across all scopes. Transitive-risk PStop is also high (93.5–96.9%). The hardest category is should-answer (PStop only 68.9–75.6% because it has few P-label cases to learn from). Utility varies sharply: cross-cluster benefits most from cluster transfer (69.1%→86.8%), while should-refuse utility remains low (39–41%) due to conservative precedent interpretation.

---

### 5. `esc_transfer_delta`
**Caption:** Transfer effect on PStop and Utility when expanding from individual-10 to cluster or rich-cluster scope. Cluster transfer for GPT-5-mini trades 2.3pp PStop for +6.9pp utility — a favourable exchange. Rich-cluster transfer improves both metrics for GPT-5-mini (+0.4pp PStop, +8.2pp utility). GPT-5.5 benefits less from transfer (+0.2pp PStop, +0.9pp utility for rich), suggesting that larger models already extract relationship-boundary signal from individual precedents alone.

---

### 6. `esc_decision_change`
**Caption:** Decision change analysis showing the precision of transfer-induced changes. When moving from individual to cluster or rich-cluster scope, most changed decisions are corrections (green). GPT-5-mini individual→rich achieves 72% precision (149/208 changed to correct). GPT-5.5 shows lower absolute change counts (129 vs 208 for 5-mini) with 54% precision, consistent with it already making better individual decisions.

---

## Recommended Figures for Thesis

| Priority | Figure | Rationale |
|----------|--------|-----------|
| 1 | `esc_scope_comparison` | Core result: PStop vs Utility across all scopes (matches Table 6.5) |
| 2 | `esc_pstop_utility_frontier` | Compact scatter showing the trade-off space |
| 3 | `esc_per_category` | Shows where escalation works (should_refuse) vs struggles (should_answer) |
| 4 | `esc_transfer_delta` | Quantifies the value of cluster transfer |
| 5 | `esc_error_decomposition` | Confirms conservative-by-default property |

---

## Data Source

All plots generated from: `../phase2/summary_table.md` (Phase 2, Table 6.5 in thesis).

Script: `generate_escalation_plots.py`
