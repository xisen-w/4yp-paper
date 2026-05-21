# PACT-NET Final RQ, Audit, and Rewrite Plan

Date: 2026-05-19

## Core Question

**What can PACT-NET answer that PACT-PAIR cannot?**

PACT-NET is not mainly a larger benchmark. Its value is that it lets us ask questions that do not exist in a dyad. PACT-PAIR has one requester and one target; PACT-NET has third parties, social clusters, authority claims, and networked memory. The chapter should therefore be organised as four PACT-NET-only findings.

Use only the validated P0/P1 PACT-NET V2 results in the main chapter. P0/P1 are local PACT-NET names introduced to avoid collision with the PACT-PAIR D0--D5 defence ladder:

- **P0:** no `POLICY.md`.
- **P1:** per-agent static role/category `POLICY.md`.

P1 is not relationship-specific. Each target agent receives its own role/category policy, but that policy is the same regardless of whether the requester is a colleague, investor, friend, family member, or external actor. There is no clean P2/D2, no relationship-specific policy, and no escalation condition in the PACT-NET chapter.

## Finding 1 — Third-Party Information Can Leak Indirectly

**Question PACT-PAIR cannot ask:**  
Can information about a third party leak through an otherwise legitimate delegation?

In PACT-PAIR, A asks B and the benchmark can only test whether B leaks B's information to A. There is no C. In PACT-NET, A can ask B a legitimate question whose answer co-locates information about C. The model must answer the legitimate part while withholding the third-party part.

Metric:

- `transitive_risk`: task-family correctness on selective-disclosure tasks.
- `T`: transitive leak rate; lower is better.

Result:

| Metric | P0 | P1 | Interpretation |
|---|---:|---:|---|
| transitive_risk correct | 3.7% | 22.3% | P1 helps, but weakly. |
| T transitive leak rate | 96.3% | 77.7% | Even with P1, 3 in 4 transitive cases leak. |

Claim:

P1 can suppress direct privacy probes, but it struggles with legitimate requests whose evidence bundle contains third-party private facts. This is a network-native selective-disclosure failure.

Plot:

- Main compact panel: `pact_net_four_findings_panel.pdf/png`
- Broader diagnostic view: `pact_net_protection_dumbbell.pdf/png`

## Finding 2 — Information Crosses Social and Organisational Clusters

**Question PACT-PAIR cannot ask:**  
Does information cross from one social or organisational cluster into another where it should not be visible?

PACT-PAIR has one relationship at a time. It cannot represent professional, personal, investor, family, and external clusters simultaneously. PACT-NET can test whether a fact that is appropriate inside one cluster leaks into another.

Metric:

- `cross_cluster`: task-family correctness on cluster-boundary tasks.
- `X`: cross-cluster leak rate; lower is better.

Result:

| Metric | P0 | P1 | Interpretation |
|---|---:|---:|---|
| cross_cluster correct | 12.5% | 30.4% | P1 helps, but most cluster-boundary cases still fail. |
| X cross-cluster leak rate | 87.5% | 69.6% | P1 still leaks across cluster boundaries in about 2 of 3 cases. |

Claim:

The agent does not reliably maintain boundaries such as professional vs personal, investor vs operator, or internal vs external. Relationship-aware and cluster-aware infrastructure is needed because the model's local judgement remains too coarse.

Plot:

- Main compact panel: `pact_net_four_findings_panel.pdf/png`
- Broader diagnostic view: `pact_net_protection_dumbbell.pdf/png`

## Finding 3 — One Leak Often Becomes Multi-Fact Disclosure

**Question PACT-PAIR cannot ask:**  
When a networked agent leaks, does it leak only the requested fact, or does it amplify the disclosure by bundling co-located facts?

PACT-PAIR can score whether a gold fact appears in one response. PACT-NET can measure whether networked memory causes leakage to expand: one query pulls in adjacent facts from the same note, same person, or same cluster.

Metric:

- `A`: amplification factor; 1.0 would mean no amplification beyond the nominal target fact.

Result:

| Metric | P0 | P1 | Interpretation |
|---|---:|---:|---|
| A amplification factor | 1.61 | 1.55 | Leaks remain bundled: more than one fact per leak event on average. |

Claim:

Networked memory makes leakage denser. The problem is not only whether the requested fact leaks, but whether the response drags along neighbouring facts. P1 reduces some attack success but does not eliminate co-disclosure.

Plot:

- Main compact panel: `pact_net_four_findings_panel.pdf/png`

## Finding 4 — Agents Can Be Tricked by False Delegation Claims

**Question PACT-PAIR cannot ask:**  
Can an agent be tricked by a requester who claims authority from a third party?

PACT-PAIR has requester and target only. It cannot naturally express "I am asking on behalf of someone else." PACT-NET can test false delegation: A claims that B authorised the request to C.

Metric:

- `confused_deputy`: task-family correctness on false delegation tasks.
- `D`: confused deputy attack success rate; lower is better.

Result:

| Metric | P0 | P1 | Interpretation |
|---|---:|---:|---|
| confused_deputy correct | 53.0% | 98.0% | P1 nearly solves this direct false-delegation surface. |
| D confused deputy attack success | 47.0% | 2.0% | P1 reduces attack success by 45pp. |

Claim:

False delegation is a real network-specific attack surface, but unlike transitive leakage and cross-cluster leakage, it is highly responsive to per-agent policy because the bad authority claim is visible in the immediate request.

Plot:

- Main compact panel: `pact_net_four_findings_panel.pdf/png`
- Broader diagnostic view: `pact_net_protection_dumbbell.pdf/png`

## Chapter Structure

### Benchmark Design

Keep this compact:

- **Setting and infrastructure:** 25-agent TechFlow graph, production `contact_agent` path, namespace-isolated runs.
- **Task families:** should-answer, should-refuse, transitive-risk, confused-deputy, cross-surface plant, non-contact probe.
- **Relationship-conditioned labels:** L/P/B depends on requester, target, category, and relationship.
- **Metrics:** utility/safety plus `T`, `X`, `A`, `D`, and contact enforcement.
- **Conditions:** P0 no `POLICY.md`; P1 per-agent static role/category `POLICY.md`.

### Experiments and Findings

Use four findings exactly:

1. **Third-party information can leak indirectly.**
2. **Information crosses social and organisational clusters.**
3. **One leak often becomes multi-fact disclosure.**
4. **Agents can be tricked by false delegation claims.**

### Summary

PACT-NET demonstrates that cross-boundary agentic delegation creates failure modes that are not visible in pairwise evaluation: third-party transitive disclosure, cross-cluster leakage, amplification through co-located memory, and false delegation. Policy is useful, especially for visible false-delegation attacks, but the persistent transitive and cross-cluster leak rates show that networked delegation needs structural mechanisms for requester-conditioned access, selective disclosure, audit, and escalation.

## What This Chapter Should Not Claim

- Do not claim action outcomes are DB-diff verified for P0/P1; they are response-heuristic scored and should be framed as directional.
- Do not claim both source and target were definitely GPT-5.5; the audit found target execution follows the production `contact_agent` model configuration unless explicitly traced.
- Do not claim Phase 1 had zero errors across all runs; the audit notes D0/P0 R2 errors in the underlying run.
- Do not present D2/P2 as evaluated in PACT-NET V2.

## Plots Generated

Generated in `thesis/results/pact_net/plots/`:

| File | Purpose |
|---|---|
| `pact_net_frontier_scatter.pdf/png` | Safety-utility frontier from P0 to P1. Backup figure; not currently inserted. |
| `pact_net_protection_dumbbell.pdf/png` | Multi-row dumbbell showing where P1 helps and where network-only failures remain. Backup figure; not currently inserted. |
| `pact_net_protection_heatmap.pdf/png` | Compact matrix for all direct, authority-chain, and network-only protection scores. Good appendix/backup figure. |
| `pact_net_four_findings_panel.pdf/png` | Combined 2x2 panel for the four PACT-NET-only findings. |
| `pact_net_four_findings_data.csv` | Machine-readable data used for all finding plots. |
| `pact_net_protection_matrix_data.csv` | Machine-readable data for dumbbell and heatmap plots. |
| `generate_pact_net_plots.py` | Matplotlib/seaborn script for regenerating the figures. |
