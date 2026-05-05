# Serious Review Truth

## Instructions

Keep this as a log. Each round mark a number. Log what got fixed, what to fix, and what version of the paper we are referring to. Use this to track progress across review rounds and ensure nothing falls through the cracks.

---

## Round 1: Google PAT Review (2026-05-05)

**Source**: OpenReview, LLM Feedback by Program Chairs  
**Paper version reviewed**: pre-v28 (reviewer saw old 33% numbers, XX placeholders)  
**Fixes applied in**: v29

### Already resolved in v28 (before this round)

- Multi-step D2 leak rate "33%" vs "12.6%" discrepancy — the 33% was Tina self-report, removed in v28
- "Table 4 shows 38.0% leak and 85.5% utility" — old Gold Scan numbers, replaced with LLM judge in v28
- Metric terminology inconsistency — unified to Refuse/Msg.Leak/Failed Att./Glob.Leak in v28

### Fixed in v29

1. **Checklist [TODO]** — filled all 16 items with proper answers and justifications
2. **Checklist instruction block** — deleted the "IMPORTANT, please: Delete this instruction block..." text
3. **D1 prompt wording inconsistency** — main text said "Try not to share..." but appendix said "Use your best judgment..." → unified to the actual prompt used in experiments
4. **"Chaos of Agents" → "Agents of Chaos"** in Table 7
5. **Bibliography capitalization** — added braces around LLM, AI, MemGPT, etc. in .bib
6. **Missing Action evaluation pipeline** — added paragraph in Appendix E explaining state-diff check
7. **Utility adjudication logic** — clarified utility = LLM judge verdict "correct"
8. **Eq. 1 formal definition** — reworded to match actual pipeline (LLM judge, not just string presence)
9. **Eq. 2 denominator typo** — fixed Q_pub → Q_prot
10. **Variable R undefined** — added definition in equation context
11. **Nasr et al. missing venue** — added arXiv identifier
12. **Tick budget contradiction** — clarified: 10 groups × 60 ticks each, run sequentially with shared memory state; "240 cumulative ticks" = total interaction ticks across groups sharing the same conversation
13. **"D0 blocks only 5% of sensitive edits"** — checked data, corrected claim
14. **"LLM judge misses no leaks" contradiction** — fixed text to acknowledge 7+10 string-only cases exist
15. **Math formalization (§2)** — added "illustrative, not formal" framing; fixed notation to avoid double-counting
16. **PAC-BENCH naming** — added footnote acknowledging similarity

### TODO (future rounds)

17. **XX placeholders in Table 5 (cross-model)** — gpt-5.5 full row, D1 for gpt-5.4-mini/gpt-5.4/Kimi/DeepSeek. DECISION: run experiments or remove rows?
18. **XX placeholders in Table 6 (relationship)** — Tina and Marcus QA runs. DECISION: run experiments or restructure table?
19. **OR-pooling claim vs arithmetic mean** — Line 453 claims OR-pooling but numbers are arithmetic means. True OR-pooling on Files QA D2 = 20% (not 14%). DECISION: which methodology to report?
20. **Network Amplification Factor** — undefined formula in Appendix F. DECISION: add formula or defer to "future work"?
21. **PACT-Bench vs PAC-BENCH naming collision** — consider if rename needed (low priority, just awareness)

---
