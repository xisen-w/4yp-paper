# PACT-Bench Results

Organized results for the NeurIPS 2026 submission.

## Directory Structure

```
results/
  benchmark_experiment_plan_final.md   — Experiment plan (PART-Bench naming, pre-PACT rename)
  
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
    10split/                           — 10-split × 6 conditions (M0/M1/M2 × R0/R1)
      README.md                        — 10-split experiment README
      msplit10_report.md               — Main report
      msplit10_deep_analysis.md        — Deep analysis
      msplit10_eval_llm.md             — LLM judge eval results
      msplit10_eval_llm.json           — LLM judge eval raw data
      msplit10_eval_strmatch.md        — String-match eval results
      msplit10_eval_strmatch.json      — String-match eval raw data
      msplit10_raw_extraction.json     — Raw extraction data

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
| Paper headline numbers | `layer0_single_step/partbench_v1_full_eval_report.md` |
| Cross-model comparison (Layer 0) | `layer0_single_step/cross_model/analysis.md` |
| Multi-step vs single-step | `layer0_multi_step/10split/msplit10_report.md` |
| Attack examples for figures | `layer0_single_step/notes_qa_attack_examples.md` |
| Data validity evidence | `validity/` |

## Naming

Results files use legacy naming (PART-Bench, M0/M1/M2). Paper uses PACT-Bench, D0/D1/D2.
Mapping: M0=D0, M1=D1, M2=D2.
