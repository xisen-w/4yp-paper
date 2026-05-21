# PACT-NET Plots — Chapter 5 Figures

All figures use P0/P1 notation (matching the chapter) to avoid confusion with PACT-PAIR's D0–D5 ladder.

---

## Figure Index

### 1. `pact_net_frontier`
**Caption:** PACT-NET security–utility frontier. Per-agent policy (P1) trades 10.0pp utility for 44.8pp safety, a 4.6:1 ratio. Aggregate scores hide residual network-native failures (F1–F3).

---

### 2. `pact_net_bimodal_effectiveness`
**Caption:** Bimodal policy effectiveness across task families. Policy is highly effective against bilateral threats (should-refuse +57.2pp, cross-surface plant +94.0pp, confused deputy +45.0pp, unauthorized mutation +55.6pp) but achieves only marginal gains against network-native threats (transitive risk +18.6pp, cross-cluster +17.9pp). This bimodality is PACT-NET's central finding: per-agent policy addresses direct boundary violations but cannot express third-party provenance or cluster membership.

---

### 3. `pact_net_family_accuracy`
**Caption:** Per-family accuracy for all 10 PACT-NET task families under P0 (no policy) and P1 (per-agent policy). Utility families (left) show modest over-refusal costs (11–12pp). Safety families (centre) show dramatic improvement except for transitive risk and cross-cluster, which remain below 31%. Non-contact probe (right) achieves 100% under both conditions via infrastructure-level ACL enforcement.

---

### 4. `pact_net_four_findings`
**Caption:** PACT-NET's four network-specific metrics showing P0 to P1 movement. F1: Transitive leak rate $\mathcal{T}$ drops only 18.6pp (96.3% → 77.7%). F2: Cross-cluster leak rate $\mathcal{X}$ drops 17.9pp (87.5% → 69.6%). F3: Amplification factor $\mathcal{A}$ is nearly unchanged (1.61× → 1.55×), indicating bundled leakage is a topological property. F4: Confused deputy $\mathcal{D}$ is nearly eliminated (47.0% → 2.0%), showing policy works when the threat is explicit in the request.

---

### 5. `pact_net_utility_cost`
**Caption:** Utility cost decomposition. The 10.0pp aggregate utility loss under P1 distributes across three utility families: should-answer queries (−11.9pp), authorized creates (−11.7pp), and authorized completes (−3.5pp). The dominant mechanism is over-refusal: the policy causes the agent to refuse legitimate requests that superficially resemble protected categories.

---

### 6. `pact_net_protection_heatmap`
**Caption:** Protection matrix showing correct-response rates across all task families under P0 and P1. The colour gradient makes the bimodal pattern immediately visible: security families shift from dark (low protection) to light (high protection) under P1, while transitive risk and cross-cluster rows remain dark even with policy — these are the network-native failures that prompt engineering cannot address.

---

### 7. `pact_net_residual_gap`
**Caption:** Residual attack/leak rates under P1 (the best prompt-level defence). Confused deputy attacks are nearly solved ($\mathcal{D}=2.0\%$, below the "solved" threshold). Transitive leakage ($\mathcal{T}=77.7\%$) and cross-cluster leakage ($\mathcal{X}=69.6\%$) remain far above acceptable levels, motivating the architectural solutions (MCC, Escalation) in Chapter 6.

---

### 8. `pact_net_improvement_sorted`
**Caption:** Policy impact sorted by magnitude of P0→P1 improvement. The chart reveals three distinct bands: policy-responsive families (teal, >20pp gain: cross-surface plant, should-refuse, unauthorized mutation, confused deputy), policy-resistant families (purple, <20pp: transitive risk, cross-cluster, non-contact probe at 0pp structural), and utility-cost families (red, negative: over-refusal on legitimate tasks).

---

## Recommended Figures for Thesis

| Priority | Figure | Rationale |
|----------|--------|-----------|
| 1 | `pact_net_bimodal_effectiveness` | IS the chapter's thesis in one image |
| 2 | `pact_net_protection_heatmap` | Compact, shows all families at a glance |
| 3 | `pact_net_residual_gap` | Punchy motivation for Chapter 6 |
| 4 | `pact_net_four_findings` | Matches F1–F4 structure of §5.3 |
| 5 | `pact_net_frontier` | Headline safety/utility tradeoff |

---

## Data Source

All plots generated from: `../summary_mcc_h_mcc_h_d1_pact_net_v2.json` (conditions D0, D1 mapped to P0, P1).

Script: `generate_pact_net_plots.py`
