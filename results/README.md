# PACT-Bench Results

Organized results for the NeurIPS 2026 submission.

## Eval Methodology Audit

### Three eval methods used in multi-step experiments

| Method | How it works | Coverage | Has Refuse? | False Positives |
|--------|-------------|----------|-------------|-----------------|
| **LLM Judge (V1 extraction)** | gpt-5-mini structured output judges each alexResponse extracted via progressBefore/After diffs. Fields: `verdict` (correct/incorrect/refused), `leaked`, `phase`, `phase2Flipped`. | gpt-5-mini: ~96%. GPT-5.5: **42-53% Notes, 0% Todo (broken)**. | Yes | Low (LLM verifies semantics) |
| **Gold Scan V2** (`eval_multistep_v2.ts`) | String-matches `gold_key_facts` against ALL 240 ticks' alexResponses. If any response anywhere contains the fact, it's marked leaked. | 100% for both models. | No | **High** — names in refusals, coincidental matches. gpt-5-mini M2: 38% vs LLM Judge's 12.6% (3× inflation). |
| **Tina self-report** (`msplit10_report.md`) | progressBefore/After diffs showing what Tina marked as "answered" in her own memory. Not verified against gold facts. | ~96% | No | **High** — counts Tina's belief, not actual leaks. M2: 33% vs LLM Judge's 12.6% (2.6× inflation). |

### Reliability verdict

- **LLM Judge**: Most accurate. Low false positive rate. Properly distinguishes refused/correct/incorrect. **Authoritative for gpt-5-mini multi-step.**
- **Gold Scan V2**: 100% coverage but high false positives (names appearing in refusal text, coincidental string matches). For gpt-5-mini M2: 55 of 76 "leaks" (72%) are false positives when cross-checked against LLM Judge.
- **Tina self-report**: **Not reliable for measuring actual information leakage.** The file itself states: *"This is NOT an LLM-judge eval."* Counts responses Tina *believes* are answers, not verified gold-fact disclosure.

### Paper table → eval method mapping

| Paper Table | Data | Eval Method | Coverage | Status |
|-------------|------|-------------|----------|--------|
| Table 2 (SS main) | gpt-5-mini | LLM Judge | ~100% | Authoritative |
| Table 3 (MS erosion by category) | gpt-5-mini | ~~Tina self-report~~ → **LLM Judge** | ~96% | Needs update (self-report numbers 19.5%→33% are inflated; LLM Judge gives 10.5%→12.6%) |
| Table 4 (SS cross-model) | 4 models | LLM Judge | ~100% | Authoritative |
| Table 5 (MS model scale) | gpt-5-mini + GPT-5.5 | Gold Scan V2 | 100% | Needs LLM Judge for both (gold scan inflates gpt-5-mini from 12.6% to 38%) |
| Table 6 (relationship) | gpt-5-mini | LLM Judge | ~100% | Authoritative |
| Appendix: MS headline (tab:ms_headline) | gpt-5-mini | LLM Judge | ~96% | Authoritative |
| Appendix: GPT-5.5 (tab:ms_gpt55) | GPT-5.5 | Gold Scan V2 | 100% | Being upgraded to Gold Scan + LLM Judge |

### Key discrepancy: Gold Scan V2 vs LLM Judge (gpt-5-mini M2)

| Metric | Gold Scan V2 | LLM Judge | Gap |
|--------|:------------:|:---------:|:---:|
| Leak rate | 38.0% (76/200) | 12.6% (24/191) | +25.4pp false positives |
| Refuse rate | N/A | 64.4% (123/191) | Gold Scan cannot detect refusals |
| Utility | 85.5% | 60.3% | Gold Scan counts any matched fact as "correct" even in unrelated responses |

Of the 76 Gold Scan "leaks", cross-check shows:
- 21 confirmed leaks (LLM Judge agrees)
- 55 false positives: names appearing in refusal text (e.g., "I can't share Maria Garcia's equity"), coincidental string matches from responses to unrelated questions, or partial token matches

### Phase 1 vs Final erosion (gpt-5-mini M2, LLM Judge)

| Metric | Value |
|--------|:-----:|
| Phase 1 leaked | 20/191 (10.5%) |
| Phase 2 eroded (new leaks from retries) | 4 |
| Final leaked | 24/191 (12.6%) |
| Erosion delta | +2.1pp |
| Phase 2 flipped (security, total) | 22 (but only 4 = verified leaks) |
| Refuse rate | 123/191 (64.4%) |

Compare with Tina self-report (Table 3 current): 19.5% → 33.0% (+13.5pp). The self-report over-counts because Tina marks responses as "answered" even when they don't contain gold facts.

### GPT-5.5 eval status

- **V1 LLM Judge** (`msplit10_eval_llm.json`): **LEGACY/BROKEN**. Coverage: 42-53% Notes QA, 0% Todo QA. The V1 progressBefore/After extraction method failed for GPT-5.5 because it processed messages faster, causing diffs to miss most questions. **Do not use these numbers.**
- **Gold Scan V2** (`eval_v2_gold_scan.json`): 100% coverage. String-match only. Same false positive issues as gpt-5-mini but formerly the only full-coverage eval.
- **Gold Scan V2 + LLM Judge** (`eval_v2_gold_scan_with_llm.json`): **COMPLETE**. Takes Gold Scan bestResponses and adds LLM judge verdicts. Authoritative for GPT-5.5.

### GPT-5.5 LLM Judge Results (authoritative)

| Defence | Leak | Refuse | Utility |
|---------|:----:|:------:|:-------:|
| D0 | 28.0% (56/200) | 63.5% (127/200) | 68.5% (137/200) |
| D1 | 25.0% (50/200) | 68.5% (137/200) | 56.0% (112/200) |
| D2 | **13.0% (26/200)** | **80.5% (161/200)** | 51.5% (103/200) |

### Critical caveat: attacker weakness vs defender strength

The high "refuse" rates for GPT-5.5 (63.5% at D0!) are NOT Alex refusing — they're questions that **Tina never managed to ask** within 240 ticks. Among questions actually asked:
- M0: 56/73 leaked (76.7%), 0 refusals
- M2: 26/39 leaked (66.7%), 0 refusals

GPT-5.5-as-attacker is weaker (fewer questions asked in 240 ticks), not GPT-5.5-as-defender being more resistant. The /200 denominator is correct for the paper (it measures total info exposure), but the narrative should reflect that model scale primarily weakens the attacker, not strengthens the defender.

### Model scaling comparison (LLM Judge, apples-to-apples)

| Defence | gpt-5-mini Leak | gpt-5-mini Util | GPT-5.5 Leak | GPT-5.5 Util | Leak Δ |
|---------|:--------------:|:---------------:|:------------:|:------------:|:------:|
| D0 | 84.2% | 82.9% | 28.0% | 68.5% | **-56.2pp** |
| D1 | 72.9% | 77.5% | 25.0% | 56.0% | **-47.9pp** |
| D2 | 12.6% | 60.3% | 13.0% | 51.5% | +0.4pp |

Key insight: Under D2, both models converge to ~13% leak rate. The explicit deny-list policy is the great equalizer — model scale adds nothing when strong policy exists. Model scale matters most when there's no policy (D0: 84% → 28%).

---

## Directory Structure

```
results/
  benchmark_experiment_plan_final.md   — Experiment plan (PART-Bench naming, pre-PACT rename)

  pact_net/                            — Layer 2 network privacy (25-agent SharedOS, D0 vs D1)
    README.md                          — Index + headline numbers
    v2_results_analysis.md             — Full R1 results with audit caveats
    v2_methodology_audit.md            — Architecture, eval methodology, reproducibility
    v1_vs_v2_comparison.md             — Why V1 was corrupted, corrected findings

  layer0_single_step/                  — Layer 0 single-step experiments (gpt-5-mini g401-g406)
    partbench_v1_full_eval_report.md   — Master report: Notes QA + Actions + Todo QA + cross-validation
    notes_qa_paper_stats.md            — Paper-ready numbers for Notes QA (claims, stats, quotes)
    notes_qa_failure_analysis.md       — Detailed failure case analysis
    notes_qa_failure_summary_tables.md — Summary tables for failure categories
    notes_qa_attack_examples.md        — Attack examples for figures
    actions_preliminary_analysis.md    — Actions track full analysis (A1-200)
    actions_stats_summary.txt          — Actions statistical summary
    actions_visualization_notes.md     — Notes for figure generation
    todo_qa_failure_analysis.md        — Todo QA failure analysis
    failure_analysis_raw.json          — Raw failure data (v1)
    failure_analysis_v2.json           — Raw failure data (v2, enhanced leak detection)
    README_notes_qa_analysis.md        — Notes QA analysis README
    README_actions_analysis.md         — Actions analysis README
    cross_model/                       — Layer 0 cross-model sentinel (4 models × 3 defenses)
      analysis.md                      — Cross-model analysis (gpt-5-mini, gpt-5.4-mini, gpt-5.4, kimi-k2)
      eval_batch2_raw.json             — Raw eval output
      results_summary.json             — Structured summary

  layer0_multi_step/                   — Layer 0 multi-step experiments (10-split heartbeat)
    10split/                           — gpt-5-mini: 10-split × 3 M-levels = 30 runs
      README.md                        — 10-split experiment README
      msplit10_report.md               — Tina self-report (UNRELIABLE for leak rates)
      msplit10_phase2_erosion.md       — Phase 2 attack strategy documentation
      msplit10_eval_llm.md             — LLM judge eval (AUTHORITATIVE for gpt-5-mini)
      msplit10_eval_llm.json           — LLM judge eval raw data (96% coverage, has refuse/phase)
      eval_v2_gold_scan_gpt5mini.md    — Gold Scan V2 (100% coverage but high false positives)
      eval_v2_gold_scan_gpt5mini.json  — Gold Scan V2 raw data
      msplit10_eval_strmatch.md        — String-match eval results
      msplit10_eval_strmatch.json      — String-match eval raw data
      msplit10_raw_extraction.json     — Raw extraction data
    gpt55_10split/                     — GPT-5.5: 10-split × 3 M-levels = 30 runs
      README.md                        — GPT-5.5 experiment README
      eval_v2_gold_scan.md             — Gold Scan V2 (CURRENT authoritative, 100% coverage)
      eval_v2_gold_scan.json           — Gold Scan V2 raw data
      eval_v2_gold_scan_with_llm.json  — Gold Scan V2 + LLM Judge (COMPLETE, authoritative for paper)
      msplit10_eval_llm.md             — V1 LLM judge (LEGACY — only 42-53% coverage, BROKEN)
      msplit10_eval_llm.json           — V1 LLM judge raw data (DO NOT USE)
      msplit10_eval_strmatch.md        — V1 string match (LEGACY)
      msplit10_eval_strmatch.json      — V1 string match raw data

  layer1_relationship/                 — Layer 1 relationship experiments

  pact_pair_d3_mcc/                    — L1 relationship-conditioned QA with D3, pure MCC_H, and MCC_H_D3
    README.md                          — Index + L0/L1 boundary warning
    L0_L1_COMPARISON_AUDIT.md          — Clarifies Layer 0 vs R0/R1-R4 semantics
    AUDIT_REPORT.md                    — Implementation/data audit for D3/MCC package
    full_results_analysis.md           — QA tables and three-condition comparison
    summary_three_condition_combined.json — D3 vs MCC_H vs MCC_H_D3 combined QA summary

  validity/                            — Data validity reports
    single_step_baseline_validity.md   — Single-step baseline validity check
    10split_multi_step_validity.md     — 10-split multi-step validity check
    notes_qa_g401-406_validity.md      — Notes QA replication validity (g401-g406)
    todo_qa_g401-406_validity.md       — Todo QA validity (g401-g406)
    todo_qa_g401-406_summary.csv       — Todo QA summary data

  known_issues/                        — Known bugs and data quality issues
    multi_step_bugs.md                 — Multi-step experiment bugs (g403, 300-tick run)

  archive/                             — Old directory structure (pre-cleanup)
```

## Key Results Files

| What you need | File |
|--------------|------|
| Paper headline numbers (SS) | `layer0_single_step/partbench_v1_full_eval_report.md` |
| Cross-model comparison (SS) | `layer0_single_step/cross_model/analysis.md` |
| Multi-step gpt-5-mini (authoritative) | `layer0_multi_step/10split/msplit10_eval_llm.json` |
| Multi-step GPT-5.5 (current best) | `layer0_multi_step/gpt55_10split/eval_v2_gold_scan.json` |
| Multi-step GPT-5.5 (with LLM judge) | `layer0_multi_step/gpt55_10split/eval_v2_gold_scan_with_llm.json` |
| Phase 2 erosion case studies | `layer0_multi_step/10split/msplit10_phase2_erosion.md` |
| Attack examples for figures | `layer0_single_step/notes_qa_attack_examples.md` |
| Data validity evidence | `validity/` |

## Naming

Results files use legacy naming (PART-Bench, M0/M1/M2). Paper uses PACT-Bench, D0/D1/D2.
Mapping: M0=D0, M1=D1, M2=D2.
