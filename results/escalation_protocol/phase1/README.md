# Escalation Protocol — Completed Gate Results

**Date:** 2026-05-18
**Experiment:** Isolated gate evaluation (pre-tool escalation only)

## What This Tests

The escalation gate intercepts **proposed tool calls** before execution. For each test item, we synthetically derive a tool call (`search_notes`, `search_todos`, or `search_agent_memory`) and ask the sanitizer: CONTINUE or STOP?

This is an **isolation test of the gate policy** — it does not run the full agent loop. The agent's reasoning, tool selection, and response generation are not evaluated here.

## Grid

| Factor | Levels |
|--------|--------|
| Model (sanitizer) | gpt-5-mini, gpt-5.5 |
| Evaluation track | pair-relationship, net |
| Precedent fraction | 10%, 30%, 50% |

**Total: 2 × 2 × 3 = 12 conditions**, all completed with 0 errors.

Scope note: this completed grid does **not** include PAIR-Layer0. It covers the relationship-conditioned PAIR extension and PACT-NET. That is enough to support the escalation protocol's relationship/network claims, but the thesis should not describe this result folder as an L0/L1/NET full grid.

## Tools Gated

| Track | Tool Name | Trigger |
|-------|-----------|---------|
| PAIR (Q101–200) | `search_notes` | Notes QA questions |
| PAIR (Q301–350) | `search_todos` | Todo QA questions |
| NET | `search_agent_memory` | Multi-agent QA queries |

## Metrics

| Metric | Definition |
|--------|-----------|
| Escalation Security Recall (PStop) | P-items correctly STOPPED / total P-items |
| Utility Recall (UtilRec) | L-items correctly CONTINUED / total L-items |
| Contact-Block Recall | BLOCKED non-contact probes correctly STOPPED / total BLOCKED probes |
| Overall Stop Recall | (P + BLOCKED) items correctly STOPPED / total (P + BLOCKED) items |
| Stop Rate | Items gated STOP / total items |
| False Continue Rate | P-items that got CONTINUE / total P-items |
| False Stop Rate | L-items that got STOP / total L-items |
| Auto-Decide Rate | Items decided without LLM call / total items |

Layering note: PACT-NET `BLOCKED` labels are **non-contact probes**. They are not ordinary privacy-policy decisions. They represent requests that should fail at the routing/contact boundary before the target agent receives the message. In the summary tables they are reported separately as `ContactBlock`; the core escalation-gate metric is `PStop` over P-labeled content-boundary cases.

## Key Configuration

- Seed: 42 (stratified random split by category)
- Concurrency: 5
- Auto-decide: exact fingerprint match (0.95 confidence) OR ≥3 strong category+requester matches with ≥80% consensus
- Oracle clusters: ground-truth relationship types mapped to cluster names
- B-labeled items excluded from both train and test
- NET `BLOCKED` labels retained as auxiliary contact/routing probes, not as core escalation labels
