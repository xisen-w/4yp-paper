# Architectural Solutions Plots — Chapter 6 Figures

All figures use Nature-figure style (Arial, no top/right spines, editable SVG text).
No in-image captions.

---

## Figure Index

### 1. `arch_frontier`
**Caption:** Security–utility frontier for the three PACT-PAIR L1 conditions. D3 (relationship-specific policy only) achieves the highest utility (70.9%) but leaks 15.5%. MCC_H (folder-scoped structure only) reduces leakage to 12.4% at a utility cost of 13.3pp. The combined MCC_H+D3 reaches the lowest leak rate (8.0%) with utility comparable to MCC_H alone (58.5%), demonstrating that structure and policy are complementary rather than substitutable.

---

### 2. `arch_per_requester`
**Caption:** Per-requester decomposition of utility (a) and leak rate (b) across three conditions. The complementarity pattern is visible: MCC_H dramatically reduces leakage for misaligned requesters (R3 friend: 38.7% → 22.0%; R4 investor: 16.9% → 1.6%) but increases it for aligned requesters (R1 colleague: 8.0% → 20.3%) because the agent freely shares everything in-scope. Adding D3 policy back (MCC_H+D3) restores within-scope discrimination, reducing R1 leakage to 6.3%.

---

### 3. `arch_escalation_gate`
**Caption:** Escalation gate Phase 2 results across four scope conditions and two models. PStop (private-request recall) remains above 88% in all conditions, with GPT-5.5 achieving 94.2–94.4% at 10% precedents. The utility gap between 10% and 30% same-pair labels (67–78% vs 87–91%) quantifies the cost of sparse precedents. Cluster transfer improves GPT-5-mini utility by 6.9–8.2pp without materially reducing PStop. The 90% reference line marks the target security threshold.

---

### 4. `arch_waterfall`
**Caption:** Private/boundary disclosure rate on PACT-PAIR L1 (Q1–400) across three architectural conditions. D3 relationship-specific policy alone: 15.5%. MCC_H folder-scoped structure alone: 12.4% (−3.1pp). Combined MCC_H+D3: 8.0% (−4.4pp). All three conditions use the same benchmark and metric, making the reductions directly comparable.

---

### 5. `arch_complementarity`
**Caption:** Decomposition of structure and policy effects on leak rate per requester. Teal bars show the D3→MCC_H transition (structure effect): positive values for R1 and R2 indicate that removing policy while adding structure increases leakage for aligned requesters. Navy bars show the MCC_H→MCC_H+D3 transition (policy effect): uniformly negative, confirming that policy provides within-scope discrimination that structure alone cannot. The asymmetry between R3/R4 (structure helps) and R1/R2 (policy helps) is the central complementarity finding.

---

### 6. `arch_escalation_transfer`
**Caption:** Decision change analysis for escalation gate transfer learning. Each pair shows how many decisions changed when expanding the precedent scope, split into correct vs wrong changes. Individual→cluster transfer for GPT-5-mini achieves 69% precision (116 correct / 169 changed), primarily improving legitimate-request utility (+113 L improved). Cluster→rich-card transfer shows diminishing returns for GPT-5.5 (36% precision), suggesting that richer representations benefit smaller models more than larger ones.

---

### 7. `arch_pact_net_mcc_validation`
**Caption:** PACT-NET MCC validation (Table 6.4). Panel (a): safety and utility scores across four conditions. MCC_H alone nearly matches P1 on safety (64.4% vs 71.5%) but collapses utility to 23.1% because the read-only scope blocks all authorised writes. Combined MCC_H+P1 achieves the highest safety (77.8%) with utility similarly constrained. Panel (b): network-specific metrics. Transitive leak drops only when both layers combine (96.3%→77.7%→67.0%). Confused deputy is eliminated under MCC_H+P1 (0.0%). The utility collapse motivates production MCCs with independent read and write capabilities.

---

## Recommended Figures for Thesis

| Priority | Figure | Rationale |
|----------|--------|-----------|
| 1 | `arch_per_requester` | Shows the complementarity thesis visually across all requesters |
| 2 | `arch_waterfall` | Progressive improvement narrative matching the chapter's layered argument |
| 3 | `arch_escalation_gate` | Quantifies the escalation protocol's security–utility trade-off |
| 4 | `arch_frontier` | Compact summary of the three-condition comparison |
| 5 | `arch_complementarity` | Deep dive supporting the "structure + policy" finding |

---

## Data Sources

- MCC/D3 data: `../summary_three_condition_combined.json`
- Escalation Phase 2 data: `../../escalation_protocol/phase2/summary_table.md`
- PACT-NET MCC validation: `../../pact_net/summary_mcc_h_mcc_h_d1_pact_net_v2.json`

Script: `generate_architectural_solutions_plots.py`
