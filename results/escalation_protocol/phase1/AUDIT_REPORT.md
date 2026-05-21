# Escalation Protocol — Data Audit Report

**Auditor:** Claude (automated)
**Date:** 2026-05-18

---

## 1. Completeness

This package contains both model families. It is not a gpt-5-mini-only result set.

| Condition | Expected Items | Completed | Errors | Status |
|-----------|---------------|-----------|--------|--------|
| gpt-5-mini / pair-rel / 10% | 619 | 619 | 0 | COMPLETE |
| gpt-5-mini / pair-rel / 30% | 481 | 481 | 0 | COMPLETE |
| gpt-5-mini / pair-rel / 50% | 343 | 343 | 0 | COMPLETE |
| gpt-5-mini / net / 10% | 1592 | 1592 | 0 | COMPLETE |
| gpt-5-mini / net / 30% | 1238 | 1238 | 0 | COMPLETE |
| gpt-5-mini / net / 50% | 884 | 884 | 0 | COMPLETE |
| gpt-5.5 / pair-rel / 10% | 619 | 619 | 0 | COMPLETE |
| gpt-5.5 / pair-rel / 30% | 481 | 481 | 0 | COMPLETE |
| gpt-5.5 / pair-rel / 50% | 343 | 343 | 0 | COMPLETE |
| gpt-5.5 / net / 10% | 1592 | 1592 | 0 | COMPLETE |
| gpt-5.5 / net / 30% | 1238 | 1238 | 0 | COMPLETE |
| gpt-5.5 / net / 50% | 884 | 884 | 0 | COMPLETE |

**Total gate decisions: 11,906 across 12 conditions. Zero API errors.**

Scope caveat: the completed grid covers `pair-relationship` and `net`. It does not include a PAIR-Layer0 run. Therefore this folder should be framed as the completed relationship/network escalation-gate grid, not as a full L0/L1/NET escalation grid.

---

## 2. Split Integrity

| Split | Track | Fraction | Precedents | Test | Train L/P | Test L/P/BLOCKED | Core P | Contact Probes |
|-------|-------|----------|-----------|------|-----------|------------------|-------:|---------------:|
| pair_relationship_10 | pair-rel | 10% | 69 | 619 | 15/54 | 82/537/0 | 537 | 0 |
| pair_relationship_30 | pair-rel | 30% | 207 | 481 | 30/177 | 67/414/0 | 414 | 0 |
| pair_relationship_50 | pair-rel | 50% | 345 | 343 | 55/290 | 42/301/0 | 301 | 0 |
| net_10 | net | 10% | 177 | 1592 | 117/60 | 1054/493/45 | 493 | 45 |
| net_30 | net | 30% | 531 | 1238 | 346/185 | 825/378/35 | 378 | 35 |
| net_50 | net | 50% | 885 | 884 | 582/303 | 589/270/25 | 270 | 25 |

**Observations:**
- All splits use seed=42 with stratified sampling by category
- PAIR precedent DB is heavily P-skewed (83–84% deny) — reflects the benchmark's design where most sensitive questions are P-labeled across most requesters
- NET precedent DB is more balanced (65–66% allow) — reflects the multi-agent benchmark where most queries are legitimate between contacts
- NET `BLOCKED` labels are non-contact probes. They are routing/contact-boundary probes, not ordinary escalation-policy decisions. They should be reported separately from P-labeled content-boundary cases.

---

## 2.1 Boundary-Layer Semantics

The completed NET splits contain three ground-truth labels:

| Label | Correct gate/routing behavior | Layer tested |
|-------|-------------------------------|--------------|
| `L` | CONTINUE | Legitimate tool access / utility |
| `P` | STOP | Content or relationship policy boundary |
| `BLOCKED` | STOP before target-agent execution | Contact graph / routing boundary |

This distinction matters. `P` means the requester can contact the target agent, but the requested content is out of bounds. `BLOCKED` means the requester should not be routed to the target agent at all. In the production OS, a `BLOCKED` case should normally be rejected upstream before the target agent's EscalationGate runs.

Therefore, the main escalation claim should use **PStop**: P-labeled items correctly stopped. `BLOCKED` should be framed as an auxiliary contact-enforcement check, not as evidence that the query sanitizer learned content privacy.

---

## 3. Label Distribution Issue (PAIR Track)

The PACT-PAIR benchmark has 688 scored cells with distribution: L=97 (14%), P=591 (86%).

This extreme imbalance causes a systematic failure in the auto-decide consensus heuristic:
- At 30%+ precedent, nearly all category×requester buckets contain ≥3 precedents
- Since 83-86% of precedents are "deny", consensus almost always votes STOP
- This is correct for P-items but wrong for the minority L-items
- Result: utility collapses from 65-71% at 10% to 24% at 50%

**This is NOT a bug** — it's a genuine finding about label-naive consensus mechanisms operating on skewed distributions. It should be reported as a limitation and motivation for balanced-consensus extensions.

---

## 4. Auto-Decide vs LLM-Decide Accuracy

| Condition | Auto-Decide Rate | Auto Accuracy | LLM Accuracy |
|-----------|-----------------|---------------|--------------|
| pair-rel 10% (either model) | 78.0% | 85.7% | 90.4% (mini) / 88.2% (5.5) |
| pair-rel 30% (either model) | 97.5% | 78.0% | 66.7% |
| pair-rel 50% (either model) | 99.4% | 77.3% | — (too few) |
| net 10% (either model) | 47.1% | 95.3% | 67.9% (mini) / 64.1% (5.5) |
| net 30% (either model) | 90.9% | 93.8% | 64.5% (avg) |
| net 50% (either model) | 95.2% | 94.4% | 60.7% (avg) |

**Key finding:** Auto-decide accuracy is model-independent (deterministic heuristic). Results at 30%+ are nearly identical across gpt-5-mini and gpt-5.5 because auto-decide handles 91-99% of items.

---

## 5. Cross-Condition Consistency Checks

### 5.1 Monotonicity (NET track — expected)
- PStop: 93.1% → 89.4% → 91.1% (mini), 95.1% → 90.7% → 91.1% (5.5)
  - Slight dip at 30% is expected: more auto-decide with balanced consensus means fewer forced-STOP decisions
- Utility: 78.6% → 91.8% → 93.5% (mini), 74.6% → 91.3% → 93.2% (5.5)
  - Monotonically increasing — more precedent helps utility as expected
- ContactBlock remains high across NET fractions: 97.8% → 97.1% → 96.0% for both models. This is an auxiliary routing-boundary result, not the core escalation result.

### 5.2 Model Equivalence at High Auto-Decide
- At 30% and 50% for both tracks: results are identical across models (within 1pp)
- This confirms the auto-decide heuristic dominates and the LLM is rarely consulted

### 5.3 Pair-Rel Degradation (expected given label imbalance)
- Utility degrades monotonically: 65→37→24% (mini), 71→37→24% (5.5)
- Security also degrades slightly: 90→84→83% (both models)
- Both explained by P-biased consensus over-denying everything

---

## 6. Comparison to Existing Results

### PACT-NET (same benchmark family, but gate-only methodology)

| Defense | should_answer (Utility) | should_refuse (Security) | transitive_risk |
|---------|------------------------|--------------------------|-----------------|
| D0 (no defense) | 76.8% | 15.5% | 4.2% |
| D1 (policy only) | 64.5% | 72.7% | 23.4% |
| D2 (rel. policy) | 71.5% | 66.2% | 13.8% |
| **Escalation 10%** | **88.4%** | **96.3%** | **100%** |
| **Escalation 30%** | **97.6%** | **93.8%** | **84%** |
| **Escalation 50%** | **97.6%** | **93.4%** | **93%** |

**Verdict:** On NET content-boundary cases, Escalation dominates the gate-level Pareto frontier: high PStop with substantially higher utility than prompt-only defenses. This is a gate-only comparison, not a full final-answer leakage comparison.

### PACT-PAIR (approximate comparison — different eval methodology)

| Defense | Utility | Security | Notes |
|---------|---------|----------|-------|
| D3 (avg R1-R4) | ~71% | ~78% | Full pipeline, single-turn |
| MCC+D3 (avg R1-R4) | ~56% | ~87% | Full pipeline, single-turn |
| **Escalation 10%** | **70.7%** | **90.1%** | Gate-only, relationship-conditioned |

**Verdict:** Competitive with D3/MCC+D3 average at 10% precedent. Not directly comparable due to different eval methodology (gate decision vs answer correctness).

---

## 7. Limitations and Caveats

1. **Isolation test only:** Does not run the full agent loop. Tests "given a tool call is proposed, does the gate make the right decision?" — not "does the agent ultimately leak?"
2. **Synthetic tool calls:** Every query is assumed to trigger a tool call. In production, some queries would never reach the gate.
3. **BLOCKED belongs to routing/contact enforcement:** NET `BLOCKED` cases are useful for system-level boundary analysis, but they should not be used as the core evidence for the EscalationGate's content-policy learning.
4. **No replication:** Single run per condition (budget constraint). Variance estimated via per-category/per-requester breakdowns.
5. **Label imbalance:** PAIR results at 30%+ are dominated by the auto-decide pathology, not the escalation protocol's true capability.
6. **Oracle clusters:** Uses ground-truth relationship types, not production clustering.
7. **Single model family:** Azure OpenAI (gpt-5-mini / gpt-5.5) only. Different model families may behave differently.
8. **No PAIR-Layer0 in this completed package:** The result set covers L1 relationship and NET. Do not claim a completed L0 escalation run from this folder.

---

## 8. Files in This Directory

| File | Description |
|------|-------------|
| `README.md` | Experiment overview and configuration |
| `AUDIT_REPORT.md` | This document |
| `all_conditions_eval.json` | Combined eval results for all 12 conditions |
| `splits_metadata.json` | Metadata for all 6 train/test splits |
| `summary_table.md` | Final results table for thesis |
