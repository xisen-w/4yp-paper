# Escalation Protocol Phase 2 Results

**Date:** 2026-05-19  
**Experiment:** Relationship-level precedent transfer ablation on PACT-NET  
**Run directory:** `research/runs/escalation/phase2_relationship/`

## What This Tests

Phase 2 tests the escalation gate as an isolated pre-tool classifier. Each item is converted into a synthetic `search_agent_memory` tool call and the sanitizer decides:

- `CONTINUE` for legitimate (`L`) items.
- `STOP` for private (`P`) items.

This is not a full agent pipeline test. It isolates whether precedent context helps the gate make better binary decisions before tool execution.

## Conditions

The experiment uses:

- PACT-NET only.
- L/P labels only.
- `B` and `BLOCKED` excluded.
- Question-group split.
- No auto-decide / no hash lookup.
- Two models: `gpt-5-mini`, `gpt-5.5`.

Core conditions:

| Condition | Meaning |
|---|---|
| `individual_10` | Same owner + same requester precedents from 10% train split |
| `individual_30` | Same owner + same requester precedents from 30% train split |
| `cluster_2nn_10` | Same-pair 10% precedents plus 2 same-owner similar requester relationships, using compressed anonymous cards |
| `rich_cluster_2nn_10` | Same retrieval as `cluster_2nn_10`, but shared precedents include relationship-aware rich cards |

## Important Design Detail

The `cluster_2nn_10` condition used a **compressed anonymous shared-card**:

```text
"<query_pattern>" — requester_cluster: <cluster>, category: <category> -> <ALLOW|DENY>
```

It did **not** include the similar requester's name, relationship note, policy row, sensitivity, or similarity rationale. This makes Phase 2 a conservative ablation of weak/anonymous relationship transfer, not the final production-faithful rich-card method.

## Headline Result

Cluster transfer improved utility over sparse same-pair supervision while preserving high security recall, but it did not match the utility of denser same-pair labeling. Rich cards improved the mini model on both metrics, but made GPT-5.5 more conservative than anonymous cluster cards.

| Model | Scope | Frac | PStop | Utility | AvgPrec | N | Err |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5-mini | individual | 10% | 90.8% | 69.8% | 2.4 | 1548 | 0 |
| gpt-5-mini | cluster_2nn | 10% | 88.5% | 76.7% | 7.5 | 1548 | 0 |
| gpt-5-mini | rich_cluster_2nn | 10% | 91.3% | 78.0% | 7.5 | 1548 | 0 |
| gpt-5-mini | individual | 30% | 87.7% | 91.0% | 7.4 | 1186 | 0 |
| gpt-5.5 | individual | 10% | 94.2% | 67.1% | 2.4 | 1548 | 0 |
| gpt-5.5 | cluster_2nn | 10% | 92.7% | 71.3% | 7.5 | 1547 | 1 |
| gpt-5.5 | rich_cluster_2nn | 10% | 94.4% | 68.1% | 7.5 | 1548 | 0 |
| gpt-5.5 | individual | 30% | 92.1% | 87.4% | 7.4 | 1186 | 0 |

## Bottom Line

Strict H2 is **not supported**:

> `cluster_2nn_10` did not match `individual_30` on both PStop and Utility.

But a weaker and useful claim is supported:

> Relationship-level shared precedents improve Utility under sparse same-pair supervision, with only a small drop in PStop.

Rich-card result:

> Better precedent representation helps, but not monotonically. It improves `gpt-5-mini` on both PStop and Utility, while making `gpt-5.5` safer but more conservative.

## Files

| File | Description |
|---|---|
| `all_conditions_eval.json` | Machine-readable eval for all 6 conditions |
| `per_condition/*_eval.json` | Per-condition scored result |
| `per_condition/*_config.json` | Per-condition run config |
| `per_condition/*_summary.json` | Per-condition runner summary |
| `per_condition/*_trace.jsonl` | Raw per-item gate traces for failure-case audit |
| `phase2_rich_chain.log` | Rich-card ablation launch/scoring log |
| `splits/net_10.json`, `splits/net_30.json` | Split files used by the run |
| `summary_table.md` | Thesis-ready result tables |
| `FAILURE_ANALYSIS.md` | Why cluster helped partially but failed to match 30% |
| `INSIGHTS.md` | Research takeaways and next ablation |
| `AUDIT_REPORT.md` | Data and implementation audit |
