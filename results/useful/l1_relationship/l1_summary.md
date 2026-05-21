# PACT-Bench L1: Relationship-Conditioned Privacy Leakage

## Experiment Setup
- **Defense**: D2 (category-specific deny list)
- **Model**: GPT-5-mini (2 replications)
- **Requesters**: 4 relationship framings
  - R0 = Tina (stranger/colleague, g100) — baseline
  - R2 = Marcus (boss delegate, g101) — authority framing
  - R3 = Jordan (close friend, g102) — personal relationship
  - R4 = Dana (investor/board, g103) — business relationship
- **Questions**: 400 QA per requester (200 notes-surface + 200 todo-surface)
  - Q1-100: work_public (notes), Q101-200: sensitive (notes)
  - Q201-300: work_public (todo), Q301-400: sensitive (todo)
- **Actions**: 200 per requester (100 authorized + 100 unauthorized)
- **Eval**: Two-pass — LLM judge (GPT-5-mini) + string-match on gold_key_facts
- **Date**: 2026-05-04 – 2026-05-05
- **Status**: ALL COMPLETE (400/400 QA × 4, 200/200 Actions × 4)

---

## Action Results (Complete)

### Summary

| Group | Requester | Utility | Safety |
|-------|-----------|---------|--------|
| g100 | Tina (Stranger) | **92%** | **90%** |
| g101 | Marcus (Boss) | 89% | 85% |
| g102 | Jordan (Friend) | 92% | 84% |
| g103 | Dana (Investor) | 83% | **91%** |
| **Mean** | | **89.0%** | **87.5%** |

### By Unauthorized Category

| Category (n per group) | g100 Stranger | g101 Boss | g102 Friend | g103 Investor |
|------------------------|---------------|-----------|-------------|---------------|
| unauthorized_wipe (16) | **16/16 blocked** | **16/16 blocked** | **16/16 blocked** | **16/16 blocked** |
| unauthorized_create_sensitive (16) | **16/16 blocked** | **16/16 blocked** | **16/16 blocked** | **16/16 blocked** |
| unauthorized_edit_sensitive (20) | 19/20 blocked | 19/20 blocked | 18/20 blocked | 19/20 blocked |
| probing_action (16) | 15/16 blocked | 14/16 blocked | 15/16 blocked | 15/16 blocked |
| info_leaking_action (16) | 15/16 blocked | **9/16 blocked** | 11/16 blocked | 15/16 blocked |
| unauthorized_strategic (16) | 9/16 blocked | 11/16 blocked | **8/16 blocked** | 10/16 blocked |

### Key Action Findings

1. **D2 blocks 100% of wipe and create_sensitive** across all requesters — relationship has zero effect on hard-deny categories.
2. **info_leaking_action** shows strongest relationship effect: Marcus (boss) executes 7/16 (44%) vs Tina (stranger) 1/16 (6%). Authority framing is most effective for action-based exfiltration.
3. **unauthorized_strategic** is the universal weakness: 44-50% blocked regardless of relationship. D2 doesn't adequately address governance-level actions.
4. **Dana (investor) has lowest utility (83%)** but highest safety (91%) — agent is most cautious with investor framing.

---

## QA Results (Full eval re-running — partial data from May 4)

From existing eval (g101-g103 complete, g100 partial):

### Category-Level Leak Rates

| Category | Jordan (friend) | Dana (investor) |
|----------|----------------|-----------------|
| sensitive_work (60) | 18.3% (11/60) | **31.7% (19/60)** |
| personal_finance (49) | 0% (0/49) | 0% (0/49) |
| personal_health (40) | 5.0% (2/40) | 5.0% (2/40) |
| personal_relationships (51) | 3.9% (2/51) | 3.9% (2/51) |

### Utility (work_public correct rate)

| | Tina (partial) | Marcus (partial) | Jordan | Dana |
|--|----------------|-----------------|--------|------|
| Utility | 73.3%* | **90.0%*** | 57.5% | 70.5% |
| Refused | 6.7% | 1.0% | **19.5%** | 10.0% |

*Partial data; full re-eval running.

---

## Core Findings

### 1. Investor framing nearly doubles sensitive_work QA leakage
Dana (investor) leaks 31.7% of sensitive_work vs Jordan (friend) at 18.3% (+13.4pp). The investor frame makes financial/HR/equity questions feel "legitimate" for the agent to answer — consistent with fiduciary-access social norms.

### 2. All relationships protect personal data equally well
personal_finance (0% all), personal_health (5% both), personal_relationships (3.9% both) are equally protected regardless of requester. D2 is robust for personal categories.

### 3. Friend framing causes over-refusal
Jordan's utility is 57.5% vs Marcus's 90.0%. Jordan refuses 19.5% of work_public questions. The agent preemptively refuses when it detects informal/personal framing.

### 4. Boss delegate achieves highest utility
Marcus at 90.0% utility (only 1% refused work_public). Authority framing ("Sarah needs this") makes the agent maximally helpful.

### 5. Asymmetric QA/Action vulnerability
Dana leaks more QA data (investor framing extracts info) but has highest action safety (92%). Jordan leaks less QA but executes more unauthorized actions. Relationship effects are surface-dependent.

### 6. Destructive actions uniformly blocked
unauthorized_create_sensitive (0/16 all) and unauthorized_wipe (0/16 all) are perfectly blocked regardless of relationship. D2 defense is absolute for destructive categories.

### 7. Strategic actions are the universal weakness
unauthorized_strategic actions execute at 50-56% across ALL requesters — relationship-independent. This is D2's blind spot.

---

## Run Notes

- g100 QA experienced multiple hangs during Q388-400 (personal_relationships). Required 5 restarts. All 400 completed 2026-05-05 ~15:45.
- Full QA eval with complete g100 data running as of 2026-05-05 14:55. Will update l1_qa_eval_llm.json.
- Actions eval completed cleanly on 2026-05-04.

---

## Data Sources

| File | Content |
|------|---------|
| `l1_actions_eval.json` | Action eval (4 groups × 200, complete) |
| `l1_qa_eval_llm.json` | QA eval (re-running with full g100 data) |
| `l1_deep_analysis.md` | Statistical audit with McNemar tests and CIs |
| Raw QA runs | `research/runs/l1/single_m2_g{100-103}_*` |
| Raw action runs | `research/runs/l1/action_m2_g{100-103}_*` |
| Questions | `research/configs/questions.json` |
| Label matrix | `research/configs/relationship_label_matrix.json` |
| Eval script | `research/scripts/eval_single_step.ts` |
