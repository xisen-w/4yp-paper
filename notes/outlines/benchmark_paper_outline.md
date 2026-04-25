# NeurIPS Benchmark Paper Outline
## PrivacyBench: Measuring the Security-Utility Tradeoff in Cross-Boundary Agent Communication

**Target:** NeurIPS 2026 Datasets & Benchmarks Track (9 pages + references + appendix)

---

### One-Sentence Pitch

The first benchmark that simultaneously measures utility and security when personal AI agents communicate across trust boundaries, revealing that generic privacy instructions reduce leakage by only 5 percentage points while category-specific policies achieve a 57pp improvement at negligible utility cost.

### Storytelling Patterns Applied

| Pattern | Application |
|---|---|
| **Evaluation crisis** (MMLU, HELM) | "No benchmark measures both utility AND security for cross-boundary agents" |
| **Dramatic failure** (SWE-bench: "2%") | "92% of sensitive data leaks; generic policy improves this by only 5pp" |
| **Taxonomy as contribution** (HELM, MTEB) | categories × defenses × relationships × modalities = evaluation framework |
| **Scalable evaluation** (HumanEval: unit tests) | gold_key_facts string matching = automated dual-metric scoring |
| **Ecological validity** (SWE-bench: real GitHub issues) | Built on a real deployed agent system with real user data patterns |
| **Living benchmark** (Chatbot Arena, MTEB) | Open-source release + leaderboard invitation |

---

### Structure

#### Title + Abstract (0.25 pages)

**Title:** PrivacyBench: Measuring the Security-Utility Tradeoff in Cross-Boundary Agent Communication

**Abstract (150 words):**
Personal AI agents increasingly hold sensitive data — notes, calendars, emails — and are beginning to communicate across trust boundaries via protocols like MCP and A2A. Yet no evaluation framework measures whether these communications are safe. We introduce PrivacyBench, a benchmark of 200 questions across 5 sensitivity categories, evaluated under 3 defense levels, 2 relationship conditions, and 2 attack modalities, with a dual-metric protocol that measures both task-completion utility and data-protection security simultaneously. Across 86 experimental runs, we find that: (1) generic privacy instructions reduce information leakage by only 5 percentage points; (2) category-specific policies achieve a 57pp improvement at <2.5% utility cost, breaking the assumed security-utility tradeoff; (3) multi-step conversation amplifies leakage 2-3x over single-step; and (4) relationship context has surprising dual-direction effects on privacy that depend on the data category. We release the benchmark, evaluation code, and all experimental data.

---

#### 1. Introduction (1.5 pages)

**Opening hook (1 paragraph):**
"When a personal AI agent engages in multi-turn conversation with an external agent under no defense policy, 92% of sensitive information leaks. Adding a generic privacy instruction — 'try not to share personal information' — reduces this to 87%. Agent privacy benchmarks that ignore the utility cost of defenses, and agent capability benchmarks that ignore security, both miss the full picture. We need a benchmark that measures both."

**The gap (2 paragraphs):**
- Agent capability benchmarks (SWE-bench, AgentBench, MMLU) don't measure privacy
- Agent security benchmarks (InjecAgent, AgentDojo, TensorTrust) don't measure utility cost
- No benchmark combines: multi-turn attacks + dual metrics + defense gradient + relationship variation
- Table 1: Comparison matrix (InjecAgent, AgentDojo, TensorTrust, TAMAS, AgentSocialBench, PrivacyBench)

**Contributions (1 paragraph):**
1. A dual-metric benchmark with 200Q across 5 sensitivity categories, automated evaluation via gold_key_facts
2. A defense gradient methodology (M0 → M1 → M2) that isolates the contribution of defense specificity
3. The first measurement of relationship effects on agent privacy (R0 vs R1)
4. Six empirical findings about the security-utility tradeoff (summarized in §5)
5. Open-source release of benchmark, evaluation code, and all experimental data

---

#### 2. Related Work (1 page)

**§2.1 Agent Security Benchmarks**
- InjecAgent (Zhan et al. 2024): single injection, tool-integrated → no utility measurement, no multi-turn
- AgentDojo (Debenedetti et al. 2024): dynamic sandbox → single task, no relationship variation
- TensorTrust (Toyer et al. 2023): human game → no persistent memory, no continuous interaction
- TAMAS (Kavathekar et al. 2025): general adversarial risk → no dual metric
- AgentSocialBench (Wang & Jiang 2026): closest — cross-boundary privacy, but no defense gradient, no adaptive attacks, no utility measurement
- HackAPrompt (Schulhoff et al. 2023): human-crafted injections → no agent-to-agent

**§2.2 LLM Privacy and Safety**
- Nasr et al. (2025): every defense bypassed under adaptive attack → motivates our "security theater" finding
- Anthropic prompt injection (2025): 1% ASR = still nonzero for personal data
- Meta Rule of Two (2025): agent vulnerability framework

**Our position:** "First dual-metric, multi-turn, defense-gradient benchmark for cross-boundary agent privacy"

---

#### 3. Benchmark Design (2 pages)

**§3.1 Agent World**
- Alex (host agent): 100 notes across 11 folders + calendar + email + todos
- Tina (guest agent): queries Alex's agent with configurable relationship
- Tool access: search_notes, get_note_content, check_calendar, read_email, etc.
- Figure 1: Benchmark architecture (Alex's world → policy layer → Tina's queries)

**§3.2 Question Taxonomy**
- 5 categories: work_public (100Q), sensitive_work (30Q), personal_finance (25Q), personal_health (20Q), personal_relationships (25Q)
- Each question has gold_key_facts: strings that should appear in answer (utility) or should NOT appear (security)
- Table 2: Category examples with gold_key_facts

**§3.3 Defense Gradient**
- M0: No defense — full context, no policy
- M1: Generic prompt — "try not to share personal information"
- M2: Category-specific ACL — explicit deny-list per sensitivity category
- Design principle: each level adds ONE type of specificity, isolating its contribution

**§3.4 Experimental Conditions**
- Relationship: R0 (stranger: Tina identified by name only) vs R1 (colleague: "PM, works on Project Alpha")
- Modality: Single-step (one LLM call per question) vs Multi-step (60 ticks, heartbeat mode)
- Replication: 3 reps per condition (Bench200) + 10 splits (Bench20x10)

**§3.5 Evaluation Protocol**
- Dual metric via gold_key_facts string matching
- Utility = fraction of work_public questions answered with correct key facts
- Security = fraction of sensitive questions where NO gold_key_facts leaked
- Automated evaluation with manual audit of 100 random samples (cross-validation)

---

#### 4. Experiments (1.5 pages)

**Scale:** 86 total runs
- Bench200: 18 runs (3 policies × 2 modalities × 3 reps) — 200Q each
- Bench20x10: 60 runs (3 policies × 2 relationships × 10 splits) — 20Q each, multi-step
- V1/V3: 8 pilot runs (early exploration, 10Q each)

**Model:** gpt-5-mini (Azure endpoint)

**Table 3: Main Results**

| Condition | M0 Leak | M1 Leak | M2 Leak | M0→M1 Δ | M1→M2 Δ |
|---|---|---|---|---|---|
| Single-step (Bench200) | 49.0% | 45.0% | 10.7% | -4.0pp | -34.3pp |
| Multi-step (Bench20x10) | 92.4% | 87.5% | 35.0% | -4.9pp | -52.5pp |

**Table 4: Per-Category Leak Rates (Multi-Step, M2)**

| Category | R0 Leak | R1 Leak | Δ |
|---|---|---|---|
| sensitive_work | ~62% | ~62% | ~0pp |
| personal_finance | ~18% | ~18% | ~0pp |
| personal_health | — | — | -10.0pp |
| personal_relationships | — | — | +10.7pp |

---

#### 5. Results and Analysis (2.5 pages)

**§5.1 Finding 1: Generic Policy Is Security Theater**
- M0 → M1: only 5pp improvement (92.4% → 87.5% multi-step)
- "Telling an agent 'don't share sensitive info' barely matters"
- Implication: defenses that don't specify WHAT is sensitive are near-useless

**§5.2 Finding 2: Category-Specific Policy Breaks the Tradeoff**
- M1 → M2: 52.5pp improvement in multi-step
- Utility cost: <2.5% (Bench200 single-step measurement)
- Figure 2: **Pareto frontier** — utility vs security for all conditions
- Key observation: M2 dominates M1 on BOTH axes — the tradeoff is NOT monotonic
- Counter to conventional wisdom: more security does NOT necessarily mean less utility

**§5.3 Finding 3: Multi-Step Amplifies Leakage 2-3x**
- Every policy leaks more under multi-step: M0 +43pp, M1 +42pp, M2 +24pp
- But: Tina rarely retries (only 2 extra calls in 20 M2 runs)
- Leakage is first-contact, not retry-based — the extended conversation provides more contexts for the agent to volunteer information
- Implication: single-step benchmarks underestimate real-world risk by 2-3x

**§5.4 Finding 4: Relationship Has Dual-Direction Category Effects**
- Overall R0 vs R1: only 1.3pp difference
- But per-category: personal_relationships +10.7pp (colleague label → social disclosure norms) and personal_health -10.0pp (colleague label → professional boundary)
- Strongest interaction: M1 × personal_relationships — R0=72% vs R1=92% (+20pp)
- Figure 3: R0 vs R1 per-category heatmap
- This is novel: no prior work measures relationship effects on agent privacy

**§5.5 Finding 5: Self-Identity Boundaries Outperform External Policy**
- MEMORY.md "Never share: salary, equity" held 100% across ALL 86 runs
- External policy (M1) crumbles at 87.5% leak
- Interpretation: boundaries embedded in agent identity >> policy overlays
- Implication for defense design: critical boundaries should be in the agent's self-concept, not just its instructions

**§5.6 Finding 6: sensitive_work Is the Ambiguity Zone**
- M2 protects personal_finance well (82%) but struggles with sensitive_work (38%)
- Reason: work questions blur public/sensitive boundary — "What's the API rate limit?" vs "What's our burn rate?"
- Category ambiguity is the primary attack vector, not prompt injection or social engineering
- Implication for benchmark design: evaluations must include boundary cases, not just clear-cut examples

---

#### 6. Discussion and Limitations (0.5 pages)

**Implications for defense design:**
- Specificity matters more than strictness
- Enumerate protected categories explicitly; generic instructions are security theater
- Consider embedding critical boundaries in agent identity, not just policy overlays

**Implications for evaluation:**
- Single-step benchmarks underestimate real-world risk by 2-3x
- Dual-metric evaluation (utility AND security) should be standard
- Relationship conditions must be varied — aggregate metrics hide dual-direction effects

**Limitations:**
- Single LLM backend (gpt-5-mini) — findings may not generalize across models
- Simulated adversary (Tina is LLM-generated) — human red-teamers may find different attack vectors
- No formal attack methods (PAIR/Crescendo/PAP) — our findings are under natural LLM conversation, not optimized attacks
- Utility evaluation incomplete for multi-step (HTML formatting issue in 44/61 Bench20x10 runs)
- Single host agent persona (Alex as startup CTO) — role diversity is future work

---

#### 7. Conclusion (0.5 pages)

PrivacyBench provides the first dual-metric evaluation framework for cross-boundary agent privacy. Our findings challenge two assumptions: (1) that the security-utility tradeoff is monotonic (category-specific policy achieves both higher security and maintained utility), and (2) that relationship context uniformly helps or hurts privacy (it does both, depending on the data category).

We release the full benchmark — 200 questions, evaluation code, gold_key_facts, policy files, and all 86 experimental runs — and invite the community to evaluate their defense mechanisms on PrivacyBench.

**Open questions for the community:**
- Can architectural defenses (context isolation, memory sandboxing) close the remaining 35% leak gap?
- How do formal attack methods (PAIR, Crescendo) interact with the defense gradient?
- Does the relationship dual-direction effect generalize across models and cultural contexts?

---

#### Appendix

- A: Datasheet for PrivacyBench (following Gebru et al. datasheets format)
- B: Full question set (200Q with categories and gold_key_facts)
- C: Policy file text (M0/M1/M2 exact prompts)
- D: Alex's world state summary
- E: Per-run results (all 86 runs)
- F: Evaluation validation (manual audit of 100 random samples)

---

### Key Differences from 4YP Thesis

| Dimension | 4YP Thesis | Benchmark Paper |
|---|---|---|
| **Scope** | Full study + solutions | Benchmark + findings only |
| **Length** | ~150 pages | 9 pages + appendix |
| **Solution proposal** | MCC, Dual-Track Memory, Escalation | Out of scope |
| **Hypothesis testing** | H1/H2/H3 explicit | Findings-driven, no formal hypotheses |
| **RQs** | 4 research questions | 0 — replaced by "6 findings" |
| **Open-source** | Not emphasized | First-class contribution |
| **Audience** | Thesis committee | NeurIPS reviewers + agent security community |
| **Tone** | "Here's what I investigated" | "Here's what YOU should measure" |
