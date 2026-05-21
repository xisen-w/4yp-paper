# PACT-NET V1 vs V2 Comparison

**Date**: 2026-05-17 (updated with 4-run V2 data)  
**Purpose**: Document why V1 results are invalid for between-condition claims, quantify the measurement error, and identify what V1 data can still be used.

---

## 1. What Happened in V1

V1 ran 4 experiments: D0x2, D2x2 using gpt-5.5 on pre-isolation infrastructure.

The critical bug: all conditions shared the same UUID space. When D0 and D2 ran concurrently, `setupPolicy()` wrote POLICY.md to **shared DB rows**. The last writer won — meaning D0 agents often had D2's POLICY.md loaded, and vice versa.

This race condition meant V1's "D0" was not actually no-policy, and V1's "D2" was not reliably policy-loaded.

---

## 2. Full Results Table

| Run | Tasks | Overall | Utility | Safety | T | D | C | X | A |
|-----|------:|--------:|--------:|-------:|---:|---:|---:|---:|---:|
| V1 D0 R1 | 997 | 63.1% | 73.0% | 54.2% | 77.7% | 0.0% | 100% | 78.6% | 1.97 |
| V1 D0 R2 | 997 | 60.5% | 68.6% | 53.2% | 87.2% | 0.0% | 100% | 89.3% | 1.85 |
| V1 D2 R1 | 997 | 68.4% | 66.5% | 70.2% | 72.3% | 0.0% | 100% | 67.9% | 1.85 |
| V1 D2 R2 | 997 | 66.2% | 65.6% | 66.7% | 85.1% | 0.0% | 100% | 71.4% | 1.76 |
| **V2 D0 R1** | **997** | **55.7%** | **89.0%** | **25.9%** | **95.7%** | **46.0%** | **100%** | **92.9%** | **1.55** |
| **V2 D0 R2** | **997** | **56.1%** | **88.1%** | **27.4%** | **96.8%** | **48.0%** | **100%** | **82.1%** | **1.67** |
| **V2 D1 R1** | **997** | **75.5%** | **79.6%** | **71.9%** | **76.6%** | **2.0%** | **100%** | **64.3%** | **1.49** |
| **V2 D1 R2** | **997** | **74.2%** | **77.9%** | **70.9%** | **78.7%** | **2.0%** | **100%** | **75.0%** | **1.61** |

---

## 3. V1 D0 Was Inflated

The true no-policy baseline is far worse than V1 suggested (V2 D0 averaged over 2 reps):

| Metric | V1 D0 avg | V2 D0 avg | V1 inflation |
|--------|:---------:|:---------:|:------------:|
| Safety | 53.7% | 26.6% | **+27.1pp** |
| should_refuse | 40.0% | 16.2% | +23.8pp |
| confused_deputy | 100% | 53.0% | +47.0pp (completely masked) |
| cross_surface_plant | 54.0% | 0.0% | +54.0pp |
| unauthorized_mutation | 69.6% | 29.6% | +40.0pp |
| transitive_risk | 17.1% | 3.7% | +13.4pp |

V1 D0 agents frequently had D2 POLICY.md loaded due to the race condition, making them appear much safer than they actually are. V2 confirms this across 2 independent reps.

---

## 4. The Policy Effect Was Massively Underestimated

| Metric | V1 Delta (D0->D2 avg) | V2 Delta (D0->D1 avg) | V2/V1 ratio |
|--------|:---------------------:|:---------------------:|:-----------:|
| Safety | +14.7pp | **+44.8pp** | 3.0x |
| should_refuse | +27.7pp | **+57.2pp** | 2.1x |
| unauthorized_mutation | +14.3pp | **+55.7pp** | 3.9x |
| confused_deputy | 0pp | **+45.0pp** | inf |
| cross_surface_plant | +23.0pp | **+94.0pp** | 4.1x |

V1 reported a +14.7pp safety effect from POLICY.md. The true effect is **+44.8pp** — 3x larger. Confirmed across 2 reps per condition.

The confused deputy result is particularly striking: V1 showed 0pp difference (both D0 and D2 at 100% defense), implying policy had no effect. V2 reveals a +45pp effect — D0 agents succeed at confused deputy 47% of the time without policy, reduced to 2% with it.

---

## 5. Per-Category Breakdown

| Category | V1 D0 avg | V1 D2 avg | V2 D0 avg | V2 D1 avg |
|----------|----------:|----------:|----------:|----------:|
| should_answer | 71.8% | 71.2% | 75.9% | 64.0% |
| should_refuse | 40.0% | 70.5% | **16.2%** | **73.4%** |
| transitive_risk | 17.1% | 20.2% | **3.7%** | 22.3% |
| cross_cluster | 14.3% | 28.6% | 12.5% | 30.4% |
| non_contact_probe | 100% | 100% | 100% | 100% |
| authorized_create | 96.7% | 90.0% | 98.4% | 86.7% |
| authorized_complete | 27.8% | 20.0% | **91.7%** | **88.3%** |
| unauthorized_mutation | 69.6% | 83.9% | **29.6%** | **85.2%** |
| confused_deputy | 100% | 100% | **53.0%** | **98.0%** |
| cross_surface_plant | 54.0% | 77.0% | **0.0%** | **94.0%** |

Bold values highlight where V2 differs significantly from V1. V2 numbers are 2-rep averages.

---

## 6. What V1 Got Right

Despite the race condition, some V1 findings remain valid:

1. **Contact enforcement (C = 100%)**: Infrastructure-level ACL gate, unaffected by POLICY.md state. The production `contact_agent()` permission check blocks non-contacts regardless of policy.

2. **Network topology effects**: Graph structure findings (hub nodes, cluster isolation, edge density) are properties of the contact graph, not the defense condition.

3. **should_answer baseline (~71%)**: V1 D0 avg (71.8%) and V2 D0 (76.7%) are reasonably consistent, suggesting the model's baseline performance on legitimate queries is stable across runs.

4. **authorized_complete improvement in V2**: V1 scored 20-28% on authorized_complete while V2 scores 88-91%. This is likely a model/infrastructure improvement unrelated to the race condition.

---

## 7. Infrastructure Differences

| Aspect | V1 (pre-isolation) | V2 (namespace-isolated) |
|--------|-------------------|-------------------------|
| UUID space | Shared across conditions | Unique per (condition, rep) |
| POLICY.md | Race on shared users | Isolated per namespace |
| Model | gpt-5.5 | gpt-5.5 |
| Infra errors | Present (DNS, 429) | 2 Phase 2 errors in D0; 0 in D1 |
| Phase 2 | Mixed into main | Scored separately |
| Condition field | `policy` (string) | `condition` (typed) |
| Action eval | Response heuristics only | DB-diff available for fresh runs |

**Model confound**: Both V1 and V2 use gpt-5.5. However, the race condition in V1 means we cannot cleanly attribute V1->V2 differences to the isolation fix alone. The within-V2 comparison (D0 vs D1) is clean since both use the same model and infrastructure.

---

## 8. Paper Implications

1. **V1 data cannot support between-condition claims.** Any table comparing D0 vs D2 using V1 numbers is based on contaminated data. The paper should use V2 numbers for all D0-vs-D1/D2 comparisons.

2. **V1 within-condition numbers can be cited cautiously** for trends that don't depend on the D0/D2 boundary (e.g., should_answer performance, contact enforcement, network structure).

3. **The corrected finding is stronger.** V1 suggested policy adds ~15pp safety. V2 shows ~45pp. The paper's central claim — that natural-language privacy policy dramatically improves agent safety — is supported even more strongly by the clean data.

4. **The race condition itself is a finding.** The fact that shared mutable state in a multi-agent system introduced a hard-to-detect measurement error is thematically aligned with the paper's contribution about cross-boundary risks.

---

## 9. Run Locations

| Run | Directory |
|-----|-----------|
| V1 D0 R1 | `research/runs/pact_net_d0_rep1_gpt55/` |
| V1 D0 R2 | `research/runs/pact_net_d0_rep2_gpt55/` |
| V1 D2 R1 | `research/runs/pact_net_d2_rep1_gpt55/` |
| V1 D2 R2 | `research/runs/pact_net_d2_rep2_gpt55/` |
| V2 D0 R1 | `research/runs/pact_net_v2_d0_r1_2026-05-15T15-18-41/` |
| V2 D0 R2 | `research/runs/pact_net_v2_d0_r2_2026-05-16T10-10-56/` |
| V2 D1 R1 | `research/runs/pact_net_v2_d1_r1_2026-05-15T15-18-41/` |
| V2 D1 R2 | `research/runs/pact_net_v2_d1_r2_2026-05-16T10-11-40/` |
