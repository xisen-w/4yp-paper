# PACT-PAIR L0/L1 Comparison Audit

Date: 2026-05-18

This note fixes the main interpretation issue in this result package: Layer 0 and Relationship are two different evaluation systems. R0 is a requester inside the L1 relationship system, not a synonym for Layer 0.

## Bottom Line

The `pact_pair_d3_mcc` folder is an L1 relationship-conditioned QA experiment. It should not be described as the main Layer 0 benchmark.

The valid story is:

- L0 evaluates clean category-level privacy: 300 OK vs 300 Not OK across QA and actions.
- L1 evaluates relationship-conditioned privacy: the same QA item can be legitimate for one requester and private for another.
- R0-R4 are requesters inside L1. R0 is the stranger/null-relationship requester, not "Layer 0".
- D3 vs MCC_H_D3 measures the incremental value of folder mounting on top of a relationship prompt policy.
- MCC_H measures pure folder mounting without policy, but it is not semantically identical to D3 because D3 injects requester policy language and MCC_H does not.

## Checklist

| Question | Answer | Status |
|---|---|---:|
| Is R0 the same as Layer 0? | No. R0 is the L1 stranger requester. | FIXED |
| Does R0 have a stranger policy under D3? | Yes. `POLICY_D3_R0.md` explicitly says stranger/no relationship. | PASS |
| Does pure MCC_H R0 say "stranger" in the prompt? | No. It has no policy prompt; it only has Shared-only structural access. | CAVEAT |
| Does L1 include work-public utility questions? | Yes. All requesters get 200 `answer` QA items from work_public. | PASS |
| Is L1 balanced per requester? | Mostly but not exactly. R0 is 200 utility / 200 security; R1-R4 differ because some sensitive items become L or B. | CAVEAT |
| Is L0 balanced? | Yes. Main L0 is 300 OK / 300 Not OK across 400 QA + 200 actions. | PASS |
| Can D3 be directly compared to MCC_H_D3? | Yes, as "add folder mounting on top of the same D3 prompt policy". | PASS |
| Can D3 be directly compared to MCC_H as "prompt vs MCC"? | Only as an operational contrast. It changes both policy language and access layer. | CAVEAT |
| Can MCC_H be interpreted as pure MCC? | Yes for folder/tool access; no for relationship semantic awareness beyond the chosen profile. | CAVEAT |
| Are actions validated in this folder? | No. This package currently contains QA results only. | FAIL for action claims |

## L0 Source Of Truth

Layer 0 lives outside this folder, primarily in:

- `thesis/results/layer0_single_step/`
- `thesis/results/layer0_multi_step/`
- `research/configs/questions.json`

Layer 0 label structure:

| Surface | OK | Not OK |
|---|---:|---:|
| QA, Q1-400 | 200 | 200 |
| Actions, A1-200 | 100 | 100 |
| Total | 300 | 300 |

This is the clean, balanced system. It is relationship-agnostic at the label level.

## L1 Source Of Truth

This folder uses the relationship-conditioned L1 setup:

- Work-public QA items remain `answer` for everyone.
- Sensitive QA items with relationship matrices use `L`, `P`, or `B` per requester.
- Sensitive QA items without a relationship matrix default to `P`.
- Actions are not included in the current L1 D3/MCC result package.

Expected QA labels before judge errors:

| Requester | Relationship | answer | L | P | B | Utility N | Security N |
|---|---|---:|---:|---:|---:|---:|---:|
| R0 | Stranger/null relationship | 200 | 0 | 200 | 0 | 200 | 200 |
| R1 | Colleague | 200 | 10 | 175 | 15 | 210 | 190 |
| R2 | CEO delegate | 200 | 49 | 150 | 1 | 249 | 151 |
| R3 | Close friend | 200 | 22 | 142 | 36 | 222 | 178 |
| R4 | Investor | 200 | 16 | 174 | 10 | 216 | 184 |

So the R0 row in L1 superficially resembles L0 QA (200 answer / 200 private), but it is still not the full L0 benchmark because it has no action tasks and uses the L1 requester-condition machinery.

## Condition Semantics

| Condition | Policy prompt | Relationship context | Access layer | What it tests |
|---|---|---|---|---|
| D3 | Per-requester `POLICY_D3_R*.md` | R1-R4 relationship shard, R0 none | Full notes + todos | Can a relationship prompt policy govern full-context access? |
| MCC_H | None | R1-R4 relationship shard, R0 none | Folder-scoped notes, coarse todo gate | What does folder mounting do without a policy prompt? |
| MCC_H_D3 | Same D3 policy as D3 | R1-R4 relationship shard, R0 none | Folder-scoped notes, coarse todo gate | Does mounting improve over prompt policy? |

Important nuance: pure MCC_H has relationship-specific folder profiles, but the model is not told "this requester is a stranger/colleague/investor" by a policy prompt. For R0, the only "stranger" signal is the Shared-only profile and lack of relationship memory.

## Valid Comparisons

| Comparison | Valid claim | Invalid claim |
|---|---|---|
| D3 vs MCC_H_D3 | Folder mounting improves a D3 prompt-policy system. | "Pure MCC beats prompt-only." |
| MCC_H vs MCC_H_D3 | Adding relationship policy on top of mounting reduces within-scope leakage. | "MCC needs D3 to work at all." |
| D3 vs MCC_H | Operational contrast between policy-only full access and no-policy mounted access. | Clean causal isolation of policy vs architecture. |
| L0 vs L1 R0 | R0 is a stranger/null-relationship stress row inside L1. | R0 is Layer 0. |
| R0-R4 inside L1 | Relationship changes the utility/security frontier. | R0-R4 are different versions of the L0 benchmark. |

## Three-Condition QA Summary

Combined Q1-400 QA:

| Condition | Utility | Disclosure rate | Interpretation |
|---|---:|---:|---|
| D3 | 70.9% | 15.5% | Prompt-only relationship policy with full access. |
| MCC_H | 57.6% | 12.4% | Pure mounting lowers exposure but leaks within mounted folders. |
| MCC_H_D3 | 58.5% | 8.0% | Mounting plus policy is strongest on security in this package. |

This supports a layered conclusion: access control removes out-of-scope data, while policy still matters for deciding what to say from in-scope data.

## Required Paper Framing

Use this wording:

> We distinguish Layer 0 from Layer 1. Layer 0 is the balanced category-level benchmark (300 OK / 300 Not OK). Layer 1 is a relationship-conditioned QA extension in which the same sensitive item may be legitimate for one requester and private for another. R0 is the stranger requester within Layer 1, not the Layer 0 benchmark.

And for MCC:

> The D3-to-MCC_H_D3 comparison measures the effect of adding mounted context control to an existing relationship prompt policy. The pure MCC_H condition is reported separately as an ablation, but it does not receive the same relationship policy text and should not be treated as a one-line replacement for D3.

