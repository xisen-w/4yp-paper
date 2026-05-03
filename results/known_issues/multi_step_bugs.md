# Multi-Step Experiment Bugs (g403, 300 ticks, M0)

Run: `m0_g403-multi_2026-04-26T12-11-01`, 300 ticks, gpt-5-mini

## Summary

300 ticks executed, only 73 unique questions asked (all work_public Q1-Q100). Security questions (Q101-Q200) were never reached. Data is **unusable for security analysis**.

---

## Root Cause 1: parseProgress Format Mismatch

**Bug**: `parseProgress()` (experiment_v2.ts:145-172) only recognizes `N. ... [answered|refused]` format. Model writes `1) Topic — Answer` or free-text variants.

**Impact**: External monitoring always reads progress=0. Does not directly cause data loss but makes the run unobservable.

**Evidence**: run_summary.json shows `finalProgress.answered: 0` despite 73+ questions actually answered in chat_history.

---

## Root Cause 2: Promise.race Timeout (Late Write-Back Corruption)

**Bug**: `Promise.race` at line ~390 does not cancel the underlying `generateText()` call. When a tick times out, the model's pending tool calls (especially `edit_note`) may still complete *after* the next tick has already started.

**Impact**: Two concurrent writes to MEMORY.md → state corruption. Observed at tick 61: MEMORY.md dropped from 11,718 chars to 6,271 chars (a write-back from a timed-out tick overwrote the newer state).

**Evidence**: tick_state_snapshots.jsonl shows sudden size drops at timeout boundaries. Chat history shows contact_agent calls that were never reflected in subsequent MEMORY.md states.

---

## Root Cause 3: maxTokens=4000 Bottleneck (edit_note Failure)

**Bug**: With `maxTokens: 4000`, the model has ~4000 output tokens per tick. When MEMORY.md grows beyond ~13.5K chars (~3500 tokens), the model cannot produce the full `edit_note(content=<entire MEMORY.md>)` call within budget.

**Impact**: After tick ~70-80, MEMORY.md is too large to rewrite. Model stops calling edit_note → questions are asked but never tracked → same "pending" items reappear → model re-asks the same questions.

**Evidence**:
- tick 84: MEMORY.md reaches 13,697 chars — last tick where edit_note succeeds
- Subsequent ticks: contact_agent called but no edit_note follows
- 69/155 active ticks had contact_agent WITHOUT edit_note (44.5%)
- Correlation: this ratio increases monotonically with tick number

---

## Root Cause 4: Idle Ticks Due to Model Confusion

**Bug**: Once MEMORY.md tracking diverges from reality, model sees many "[pending]" items that it has already asked. Without accurate state, model sometimes outputs "nothing to do" or re-asks identical questions.

**Impact**: 59/300 ticks were completely idle (no tool calls). Additional ticks asked duplicate questions.

---

## Why Only work_public Questions Were Reached

The 200 questions are ordered Q1-Q100 (work_public), Q101-Q200 (sensitive). Model processes sequentially. Due to re-asking (Root Cause 3+4), the model cycled through Q1-Q73 repeatedly without advancing past Q100 into the security questions.

---

## Proposed Fixes (Not Yet Implemented)

1. **AbortController** — Replace Promise.race with AbortController to truly cancel timed-out operations
2. **maxTokens → 10000+** — Allow model to write back larger MEMORY.md
3. **parseProgress multi-format** — Recognize model's actual output formats
4. **Forced write-back** — Fail tick if contact_agent succeeds but edit_note doesn't follow

---

## Verdict

**Data is UNUSABLE.** Only 73/200 questions attempted, all from work_public. No security signal. The g403 run cannot contribute to the paper's security findings.
