# PACT-PAIR L1 Results (Relationship Privacy + MCC)

Per-requester QA benchmark measuring how relationship-aware prompt policy (D3), pure mounted context control (MCC_H), and MCC plus D3 (MCC_H_D3) affect information disclosure across 5 requester relationships.

This is **Layer 1**, not the main Layer 0 benchmark. Layer 0 is the balanced category-level system in `thesis/results/layer0_*` and `research/configs/questions.json` (300 OK / 300 Not OK across QA and actions). R0 is the stranger requester inside L1; R0 is not Layer 0.

## Experiment Overview

- **Benchmark**: PACT-PAIR L1 relationship-conditioned QA (400 QA questions x 5 requesters)
- **Model**: GPT-5.5 (Azure) as Alex's agent
- **Judge**: GPT-5-mini (Azure) structured-output LLM judge
- **Conditions**: D3 (relationship prompt policy, full data access), MCC_H (folder-scoped access, no policy prompt), MCC_H_D3 (folder-scoped access + D3 policy)
- **Status**: QA complete. Actions not included in this package.

## Layer Boundary

| System | What it means | Source |
|--------|---------------|--------|
| L0 | Category-level balanced benchmark: QA 200 OK / 200 Not OK + actions 100 OK / 100 Not OK | `thesis/results/layer0_*` |
| L1 | Relationship-conditioned QA: R0-R4 ask the same QA pool, and sensitive labels may change by requester | this folder |
| R0 | Stranger/null-relationship requester inside L1 | `POLICY_D3_R0.md`, no relationship shard |

See [`L0_L1_COMPARISON_AUDIT.md`](L0_L1_COMPARISON_AUDIT.md) for the detailed audit.

## Headline Numbers (Q1-400 Combined QA)

| Condition | Aggregate Utility | Aggregate Disclosure Rate | Meaning |
|--------|:-:|:-:|---|
| D3 | 70.9% | 15.5% | Prompt-only relationship policy, full data access |
| MCC_H | 57.6% | 12.4% | Pure mounting, no policy prompt |
| MCC_H_D3 | 58.5% | 8.0% | Mounting plus relationship policy |

The clean causal comparison for the main MCC claim is **D3 vs MCC_H_D3**: adding folder mounting to the same D3 policy reduces disclosure from 15.5% to 8.0%, with utility dropping from 70.9% to 58.5%.

Pure MCC_H is an ablation, not a direct replacement for D3. It has folder profiles but no D3 relationship policy text, so R0 is structurally Shared-only but not explicitly told "stranger" in the prompt.

### By requester class

| Class | D3 Leak | MCC Leak | Leak Reduction | Utility Cost |
|-------|:-------:|:--------:|:--------------:|:------------:|
| Aligned (R0+R1+R2) | 7.1% | 6.4% | 10% | +1.0pp aggregate, per-requester varies |
| Misaligned (R3+R4) | 27.5% | 10.2% | **63%** | -31.6pp |

## Key Files

| File | Purpose |
|------|---------|
| [`full_results_analysis.md`](full_results_analysis.md) | Complete results: per-requester tables for Q1-200 and Q201-400, cross-track comparison, combined Q1-400 aggregate, efficiency analysis, key findings |
| [`summary_q1_200.json`](summary_q1_200.json) | Machine-readable Q1-200 results |
| [`summary_q201_400.json`](summary_q201_400.json) | Machine-readable Q201-400 results |
| [`summary_q1_400_combined.json`](summary_q1_400_combined.json) | Machine-readable combined Q1-400 results with aggregates |
| `q1_200_notes_qa/{d3,mcc_v2}/R{0-4}_judge.json` | Per-run LLM judge summaries (Notes QA) |
| `q1_200_notes_qa/{d3,mcc_v2}/R{0-4}_trace_judged.jsonl` | Full judged traces (Notes QA) |
| `q1_200_notes_qa/mcc_h/R{0-4}_*.json*` | Pure MCC_H ablation artifacts (Notes QA) |
| `q201_400_todos_qa/{d3,mcc_v2}/R{0-4}_judge.json` | Per-run LLM judge summaries (Todos QA) |
| `q201_400_todos_qa/{d3,mcc_v2}/R{0-4}_trace_judged.jsonl` | Full judged traces (Todos QA) |
| `q201_400_todos_qa/mcc_h/R{0-4}_*.json*` | Pure MCC_H ablation artifacts (Todos QA) |
| `configs/MCC_PROFILES.json` | Per-requester folder access profiles |
| `configs/relationship_label_matrix*.json` | Expected labels (answer/P/B/L) per requester per question |

## Naming

- PACT-PAIR = Privacy Assessment for Cross-boundary Trust in Pairwise Agent-user Interactions with Relationships
- D3 = Defense level 3 (per-requester relationship prompt policy)
- MCC = Mountable Context Cell (folder-level access control)
- MCC_H = pure mounted-context access without a policy prompt
- MCC_H_D3 = mounted-context access plus the same D3 policy prompt
- R0-R4 = Requester personas (Stranger, Colleague, Delegate, Close Friend, Investor)
- Q1-200 = Notes QA track; Q201-400 = Todos QA track; A1-200 = Actions track
