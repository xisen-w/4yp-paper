# Critique of research_story.md + Three Outlines

---

## Part 0: Critique of research_story.md

### What's Strong

**research_story.md is an exceptional internal research document.** It captures everything: core thesis (H1/H2/H3), existing data, research questions, experiment matrix, narrative arc, literature positioning, product alignment, feasibility, thesis audit, and reconciled story. As a "brain dump that a future reader can reconstruct the entire project from," it's 10/10.

Specific strengths:
1. **The H1/H2/H3 hypothesis structure** (§0.2) is clean and testable. The ASCII Pareto frontier diagram communicates the core thesis instantly.
2. **The data catalog** (§1.3, F1-F8) is excellent research practice — every finding has a source and thesis relevance.
3. **The experiment matrix** (§4) is rigorous — three orthogonal dimensions, each changing one variable.
4. **The thesis audit** (§9) is brutally honest — "Ch7 all `---`", "fundamental mismatch between thesis B2 and experiment M1."
5. **§12 "What Our Benchmark Actually Brings"** is the best section. Q1/Q2/Q3 are crystal clear and match the benchmark paper storytelling patterns we studied.
6. **§13 "Reconciled Story"** nails the reframing — from "claim we need to prove" to "study we report on."

### What Needs Work

**1. The document is a research journal, not a story.**

It reads chronologically — "here's what we knew, then what we learned, then what we realized." That's great for the researcher but wrong for the reader. The storytelling research shows that the best papers open with the *conclusion* ("the tradeoff is not monotonic") and then build evidence for it. research_story.md buries its best insights in §12-§13 after 750 lines of setup.

**Lesson from the storytelling analysis**: Transformer opens with "Attention is all you need" — the conclusion IS the title. TruthfulQA opens with the inverse scaling finding. Our story should open with: "Prompt-level privacy instructions are security theater" or "The security-utility tradeoff is not monotonic."

**2. Two narratives are tangled: the 4YP and the NeurIPS paper.**

§11 acknowledges this ("Big Story vs Small Story") but doesn't fully resolve it. The result is that the 4YP outline (§11.4) feels like a downscoped NeurIPS paper rather than a document with its own complete arc. The 4YP should have its own self-contained story that doesn't reference "what we'll do later for NeurIPS."

**3. The experimental picture has evolved beyond what §1 captures.**

research_story.md §1 describes V1 (10Q, 4 groups), V3 (20 ticks, attack mode), and Bench200 (single-step). But you've since run **Bench20x10** (60 runs, multi-step, R0/R1) with much richer results:
- M0 leak rate: 92.4% (not 49% — multi-step is much worse)
- M2 leak rate: 35.0% (not 10.7% — multi-step is harder to defend)
- R0 vs R1 shows a dual-direction effect: colleague label increases relationship leaks (+10.7pp) but decreases health leaks (-10.0pp)
- The strongest interaction is M1 × personal_relationships: R0=72% vs R1=92% (+20pp!)

These are more dramatic and nuanced findings than what §1 reports. The story should be built on the most complete data (Bench20x10), with Bench200 as a complementary single-step reference.

**4. The "dramatic failure result" is undersold.**

From the storytelling analysis: SWE-bench leads with "GPT-4 solves 2%." GSM8K leads with "can't do grade-school math." Our equivalent headlines:
- "92% of sensitive information leaks in multi-turn conversation" (M0, Bench20x10)
- "Generic privacy instructions reduce leakage by only 5 percentage points" (M1 vs M0)
- "Telling an agent someone is a 'trusted colleague' makes it leak MORE relationship data" (R1 effect)

These are genuinely dramatic findings. research_story.md presents them matter-of-factly in tables rather than as narrative hooks.

**5. Missing: a single Pareto frontier figure built from actual data.**

research_story.md mentions the Pareto frontier 20+ times but never contains one built from the latest data. The story_figures.py from the previous session used the Bench200 single-step numbers. We now have both single-step AND multi-step data, plus R0/R1 — enough for a proper multi-panel figure.

**6. The "relationship as security parameter" finding is stronger than research_story.md realizes.**

§5 Act 4 hypothesizes that relationship-native policies will help. But r0_r1.md shows something more interesting: relationship context has **dual-direction effects** that depend on category. This is not just "relationship helps" — it's "relationship helps for some categories and hurts for others." This is a genuinely novel empirical finding that should be a headline result, not buried in future work.

### Summary Verdict

research_story.md is a 9/10 research planning document and a 5/10 paper outline. The information is all there, but it needs to be reorganized from "what we explored" to "what we found." The three outlines below do that reorganization for three different target formats.

---

## Part 1: 4YP Thesis Outline

### Title
**Pulse: Empirical Analysis of the Security-Utility Tradeoff in Cross-Boundary Agent Communication**

### Thesis Statement
When personal AI agents communicate across trust boundaries, the severity of privacy leakage depends on three factors — the specificity of the defense policy, the attack modality (single-step vs multi-turn), and the relationship between agents — in ways the research community has not previously measured.

### Structure (8 chapters, ~150 pages target)

**Chapter 1: Introduction (8-10 pages)**
- Open with concrete scenario: Alice's agent reveals her Competitor Corp meeting to an investor
- §1.1 The Rise of Personal Agents and the Communication Gap
- §1.2 The Security Problem: Why Agents Remain Siloed
- §1.3 The Security-Utility Paradox (keep existing — it's well-written)
- §1.4 Research Approach: benchmark-first methodology
- §1.5 Contributions (3 bullet points, honest about scope)
- §1.6 Research Questions (RQ1-RQ4, but reframe RQ3/RQ4 as "design proposals with indirect evidence" rather than "tested solutions")
- §1.7 Thesis Organization

**Chapter 2: Related Work (12-15 pages)**
- §2.1 AI Agent Architectures (ReAct, Toolformer, MCP — brief)
- §2.2 LLM Security: Attacks (PAIR, Crescendo, PAP, GCG — taxonomy)
- §2.3 LLM Security: Defenses (Spotlighting, Instruction Hierarchy, Llama Guard, StruQ)
- §2.4 Agent Benchmarks (InjecAgent, AgentDojo, TensorTrust, TAMAS, AgentSocialBench)
- §2.5 Our Position: the comparison table from research_story.md §12.3 becomes Table 2.1
- Key message: "No existing work measures the full picture — dual metrics, multi-turn, defense gradient, relationship variation"

**Chapter 3: Problem Formulation (8-10 pages)**
- Keep existing formal framework {F, S, M_self}, {U, S, O} — it's clean
- §3.1 The Context-Security Tradeoff (formalization)
- §3.2 Threat Model (5 attack classes)
- §3.3 Hypotheses — **NEW: explicitly state H1/H2/H3**
  - H1: Prompt-level defense exhibits a monotonic tradeoff (more security → less utility)
  - H2: Architectural defense can break this monotonicity
  - H3: Relationship context shifts the tradeoff curve in category-dependent ways
- §3.4 Research Questions (RQ1-RQ4, tied to hypotheses)

**Chapter 4: Benchmark Design (15-18 pages)**
- §4.1 Agent Infrastructure (Alex's world: 100 notes, 11 folders, calendar, email, todos)
- §4.2 Question Design: 200 questions across 5 sensitivity categories
  - Table 4.1: Category distribution with examples
  - Table 4.2: Gold key facts for evaluation
- §4.3 Defense Gradient: M0 → M1 → M2 (with exact policy text for each)
- §4.4 Attack Modalities: Single-Step vs Multi-Step (60 ticks)
- §4.5 Relationship Conditions: R0 (stranger) vs R1 (colleague with memory shard)
- §4.6 Evaluation Methodology
  - Dual metric: gold_key_facts matching for both utility and security
  - What counts as "leaked" vs "refused" vs "correctly answered"
- §4.7 Experimental Matrix: 3 policies × 2 relationships × 2 modalities × 200Q = controlled comparisons
- §4.8 Heartbeat Mode (the tick-based execution system)
  - Figure 4.X: Tick lifecycle diagram

**Chapter 5: Results I — Failure Cases and Baseline Analysis (20-25 pages)**
*This is the "How Bad Is It?" chapter — the diagnostic half*

- §5.1 Attack Taxonomy (5 classes, now with quantitative data)
  - Table 5.1: Attack class distribution with counts from Bench200 + Bench20x10
- §5.2 Headline Result: 92% Leak Rate Under No Defense
  - Table 5.2: Main results table (M0/M1/M2 × R0/R1, leak rates)
  - Figure 5.1: **THE Pareto frontier figure** — utility vs security for all conditions
  - Finding 1: "Generic policy barely helps" — M0 92.4% → M1 87.5% (only 5pp improvement)
- §5.3 Category-Specific Analysis
  - Table 5.3: Per-category leak rates (sensitive_work, finance, health, relationships)
  - Finding 2: M2 strongest on personal_finance (18%), weakest on sensitive_work (62%)
  - Finding 3: Category ambiguity is the primary attack vector
- §5.4 Single-Step vs Multi-Step
  - Table 5.4: Bench200 SS vs Bench20x10 MS comparison
  - Finding 4: Multi-step amplifies leakage by +24-43pp across all policies
  - Finding 5: Tina rarely retries (only 2 extra calls in 20 M2 runs) — leakage is first-contact
- §5.5 The Relationship Effect
  - Table 5.5: R0 vs R1 per-category
  - Finding 6: **Dual-direction effect** — colleague label increases relationship leaks (+10.7pp) but decreases health leaks (-10.0pp)
  - Finding 7: Strongest interaction is M1 × personal_relationships: R0=72% vs R1=92% (+20pp)
  - This section is a novel empirical contribution — no prior work has measured this
- §5.6 Attack Patterns in Multi-Turn
  - Progressive side-channel (V3 G1 metadata accumulation)
  - Organic Crescendo-like escalation
  - "Paste verbatim" tool-operation reframing
- §5.7 Self-Identity vs External Policy
  - MEMORY.md "Never share: salary, equity" held 100% across all runs
  - Finding 8: Boundaries embedded in agent identity outperform external policy overlays

**Chapter 6: Solution Proposal — Architectural Defense (12-15 pages)**
- §6.1 From Diagnosis to Treatment: What Each Failure Class Motivates
- §6.2 Dual-Track Memory (addresses Class 5: memory contamination)
  - Design: self-state track + per-relationship shards
  - Isolation mechanism: metadata filtering at DB level
  - Indirect evidence: F2 (self-identity > external policy)
- §6.3 Mountable Context Cells (addresses Classes 1, 2, 4)
  - Design: capability-based execution sandbox
  - The OS analogy: MCC = Docker containers, not file permissions
  - Connection to existing Pulse architecture (folder-scoped share links)
- §6.4 Intelligent Escalation Protocol (addresses Class 3 and overhead)
  - Design: sanitisation agent + precedent clustering
  - Macro Constitution
- §6.5 Implementation Status: What's Built vs What's Designed
  - Honest about: MCC is partially implemented as folder-scoping; Escalation is design-only
  - The key argument: F2 (self-identity boundaries holding 100%) is indirect evidence that architectural enforcement works

**Chapter 7: Results II — Defense Evaluation (15-18 pages)**
*This is the "What Works?" chapter — the prescriptive half*

- §7.1 M2 as Strong Prompt-Level Defense
  - Bench200 single-step: 10.7% leak (vs 49% M0)
  - Bench20x10 multi-step: 35.0% leak (vs 92.4% M0)
  - Utility cost: <2.5% (Bench200), ~same accuracy (Bench20x10)
  - Finding: **M2 breaks the "more security = less utility" assumption** — even prompt-level defense can be high-security/low-cost when categories are specific
- §7.2 Defense Effectiveness by Category
  - Table 7.1: Per-category protection rates under M2
  - personal_finance: 82% protected (strongest)
  - sensitive_work: 38% protected (weakest — the ambiguity zone)
  - Analysis: why work-boundary questions are hardest to defend
- §7.3 The Security-Utility Pareto Frontier
  - Figure 7.1: **The key figure** — scatter plot with M0/M1/M2 × SS/MS × R0/R1
  - Discussion: the frontier is NOT monotonic — M2 dominates M1 on both axes
  - Projected MCC position (with caveats)
- §7.4 Hypothesis Testing
  - H1 (prompt-level tradeoff is monotonic): **Partially supported** — M0→M1 is monotonic, but M1→M2 shows you can gain security without losing utility. The tradeoff is not smoothly monotonic even within prompt-level.
  - H2 (architectural breaks it): **Indirectly supported** — F2 (self-identity holding 100%) is the strongest evidence. Full MCC test is future work.
  - H3 (relationship shifts the curve): **Supported with nuance** — not a simple "helps or hurts" but a category-dependent dual effect. Novel finding.
- §7.5 Comparison with Academic Baselines
  - Discussion-level comparison with Spotlighting, Instruction Hierarchy (if not implemented, discuss conceptually)
- §7.6 Threats to Validity
  - Single LLM backend (gpt-5-mini)
  - Simulated adversary (Tina is LLM-generated)
  - Utility evaluation is incomplete (44/61 runs have 0 utility tracked due to HTML formatting)

**Chapter 8: Conclusion (6-8 pages)**
- §8.1 Summary of Findings (one paragraph per RQ)
- §8.2 Contributions
  1. First dual-metric benchmark for cross-boundary agent privacy
  2. Empirical characterization of the security-utility tradeoff across defense/relationship/modality
  3. Discovery of dual-direction relationship effect on privacy
  4. Architectural solution design (MCC, Dual-Track Memory) with indirect evidence
- §8.3 Limitations (honest: no MCC experiment, simulated adversary, single model, utility eval gaps)
- §8.4 Future Work
  - Full MCC benchmark
  - PAIR/Crescendo/PAP formal attack evaluation
  - Cross-model comparison
  - Formal verification of context cells
  - Differential privacy for agent communication
- §8.5 Concluding Remarks: "Don't ask the agent to refrain — ensure the data is not in the room"

**Appendices**
- A: Full question set (200Q with categories and gold key facts)
- B: Policy file text (M0/M1/M2 exact prompts)
- C: Alex's world state summary (100 notes across 11 folders)

### Key Differences from Current Thesis .tex

1. **Reframe configs**: Drop "Baseline 1/2, Solution A/B/C" naming. Use M0/M1/M2/MCC throughout — matches actual experiments.
2. **Fill Ch7**: The biggest gap. Two datasets exist (Bench200 + Bench20x10) — enough for 20+ pages of quantitative analysis.
3. **Split results into Ch5 (diagnostic) + Ch7 (prescriptive)**: Currently Ch5 is qualitative-only and Ch7 is empty. The new structure gives each chapter a clear purpose.
4. **Add H1/H2/H3 to Ch3**: Currently implicit — making them explicit gives the thesis a testable spine.
5. **Add relationship results**: The R0/R1 dual-direction finding is novel and doesn't appear in any current .tex chapter.
6. **Downscope RQ3/RQ4**: Be honest that these are design proposals, not experimentally validated. The thesis is strongest on RQ1/RQ2.

---

## Part 2: Benchmark Paper Outline (NeurIPS Datasets & Benchmarks Track)

### Title
**PrivacyBench: Measuring the Security-Utility Tradeoff in Cross-Boundary Agent Communication**

### One-Sentence Pitch
The first benchmark that simultaneously measures utility and security when personal AI agents communicate across trust boundaries, revealing that prompt-level privacy instructions reduce leakage by only 5 percentage points while category-specific policies achieve 57pp improvement at negligible utility cost.

### Target
NeurIPS 2026 Datasets & Benchmarks Track (9 pages + references)

### Structure

**1. Introduction (1.5 pages)**
- Hook: "92% of sensitive information leaks when a personal AI agent engages in multi-turn conversation with an external agent under no defense" [dramatic failure]
- Gap: Agent capability benchmarks ignore security; agent security benchmarks ignore utility cost. No benchmark measures both. (Table 1: comparison with InjecAgent, AgentDojo, TensorTrust, TAMAS, AgentSocialBench)
- Contribution: PrivacyBench — 200 questions, 5 sensitivity categories, 3 defense levels, 2 relationship conditions, 2 attack modalities, dual-metric evaluation

**2. Related Work (1 page)**
- Agent benchmarks (capability: SWE-bench, AgentBench; security: InjecAgent, TensorTrust)
- LLM privacy/safety (Nasr et al. 2025, Anthropic prompt injection, Meta Rule of Two)
- Our position: "first dual-metric, multi-turn, defense-gradient benchmark for cross-boundary agent privacy"

**3. Benchmark Design (2 pages)**
- §3.1 Agent World: 100 notes across 11 folders, calendar, email, todos — realistic personal context
- §3.2 Question Taxonomy: 5 categories (work_public, sensitive_work, personal_finance, personal_health, personal_relationships) with gold_key_facts
- §3.3 Defense Gradient: M0 (none) → M1 (generic prompt) → M2 (category-specific ACL)
- §3.4 Relationship Conditions: R0 (stranger) → R1 (colleague with memory shard)
- §3.5 Attack Modalities: Single-step (200Q batch) + Multi-step (60 ticks, heartbeat mode)
- §3.6 Evaluation: Dual metric via gold_key_facts string matching — simultaneously scores utility (work questions answered correctly) and security (sensitive data not leaked)
- Figure 1: Benchmark architecture diagram

**4. Experiments (1.5 pages)**
- 78 total runs: Bench200 (18 runs, single-step) + Bench20x10 (60 runs, multi-step)
- Table 2: Main results — leak rate × policy × relationship × modality
- Table 3: Per-category breakdown

**5. Results and Analysis (2 pages)**
- §5.1 Finding 1: Generic policy is security theater (5pp improvement)
- §5.2 Finding 2: Category-specific policy breaks the tradeoff (57pp improvement, negligible utility cost)
  - Figure 2: **Pareto frontier** — utility vs security for all conditions
- §5.3 Finding 3: Multi-step amplifies leakage by 24-43pp
- §5.4 Finding 4: Relationship has dual-direction category effects (+10.7pp relationships, -10.0pp health)
  - Figure 3: R0 vs R1 per-category heatmap
- §5.5 Finding 5: Self-identity boundaries hold 100% while external policy crumbles
- §5.6 Finding 6: Category ambiguity is the primary attack vector (sensitive_work is hardest)

**6. Discussion (0.5 pages)**
- Implications for defense design: specificity matters more than strictness
- Implications for evaluation: single-step benchmarks underestimate leakage by 2-3x
- Limitations: single model, simulated adversary, no formal attack methods (PAIR/Crescendo)

**7. Conclusion (0.5 pages)**
- Open-source benchmark release
- Call to action: "Agent privacy needs dual-metric evaluation as a standard"

**Appendix**
- Full question set
- Policy text
- Per-run results
- Datasheet for PrivacyBench (following Gebru et al. datasheets format)

### Key Differences from 4YP

1. **No solution proposal** — pure benchmark paper. MCC/Dual-Track Memory are out of scope.
2. **Tighter scope** — 9 pages forces ruthless prioritization. Only 6 findings.
3. **Open-source release** is a first-class contribution (benchmarks-as-infrastructure pattern from MTEB, Chatbot Arena).
4. **Leaderboard framing** — "we invite the community to evaluate their defenses on PrivacyBench."
5. **Uses both datasets** — Bench200 for single-step, Bench20x10 for multi-step. Shows both.

---

## Part 3: Technical Report Outline

### Title
**Personal Agent Privacy Under Cross-Boundary Communication: A Systematic Empirical Study**

### One-Sentence Pitch
The first comprehensive empirical study of what happens to private data when personal AI agents interact across trust boundaries, covering defense mechanisms, attack modalities, relationship dynamics, and architectural solutions — based on a deployed system (Pulse) with real users.

### Target
arXiv technical report (20-30 pages), potentially JMLR or TMLR submission

### Structure

**1. Introduction (2 pages)**
- The big picture: personal agents hold private data and are starting to interact externally
- What the field knows vs doesn't know (from research_story.md §11.2)
- "We built a real system. Here is everything we learned."

**2. Background and Related Work (3 pages)**
- Agent architectures and protocols (MCP, A2A)
- LLM security landscape (attacks, defenses)
- Cross-boundary privacy specifically (AgentSocialBench, our positioning)
- Formal problem statement ({U, S, O} Pareto frontier)

**3. System Design: Pulse (3 pages)**
- The coordination layer concept (TCP/IP analogy)
- Agent infrastructure: notes, calendar, email, tools
- Share links as MCCs (per-relationship context isolation)
- Memory architecture

**4. Benchmark Design (3 pages)**
- 200 questions, 5 categories, gold key facts
- Defense gradient: M0 → M1 → M2 → (future: Spotlighting, MCC)
- Attack modalities: single-step, multi-step (60 ticks), heartbeat
- Relationship conditions: R0 (stranger), R1 (colleague)
- Evaluation methodology

**5. Experimental Results (6 pages)**
- §5.1 Scale: 78 runs, 12,000+ question-answer pairs
- §5.2 Main Results Table
- §5.3 The Defense Gradient (M0 → M1 → M2)
  - Finding: generic policy is theater; category-specific policy works
- §5.4 Single-Step vs Multi-Step
  - Finding: multi-step amplifies 2-3x
  - Progressive side-channel patterns
- §5.5 The Relationship Effect
  - Finding: dual-direction category-dependent effect
  - Finding: M1 × relationship → 20pp interaction
- §5.6 Category Analysis
  - Finding: sensitive_work is the ambiguity zone
  - Finding: personal_health is most protectable
- §5.7 Self-Identity vs External Policy
  - Finding: embedded boundaries >> policy overlays
- §5.8 The Pareto Frontier
  - Figure: utility vs security across all conditions
  - The tradeoff is not monotonic

**6. Architectural Solutions (4 pages)**
- §6.1 Mountable Context Cells
  - Design, OS analogy, connection to share links
  - Why it should break the tradeoff (argument from F2)
- §6.2 Dual-Track Memory
  - Design, isolation mechanism
- §6.3 Escalation Protocol
  - Design, precedent clustering
- §6.4 Implementation Status (honest assessment)

**7. Discussion (2 pages)**
- Lessons for practitioners
- Lessons for the research community
- Comparison with industry approaches (Google 5-layer, Meta Rule of Two, Anthropic hardening)
- Limitations

**8. Conclusion (1 page)**
- Summary of 8 empirical findings
- "Don't instruct — isolate"
- Open-source benchmark release

**Appendices (5-10 pages)**
- A: Full question set
- B: Policy text
- C: Alex's world state
- D: Per-run results tables
- E: Attack pattern taxonomy with examples

### Key Differences from Other Two

1. **Includes the system description** — Pulse as a real deployed system, not just a benchmark
2. **Includes solutions** — MCC, Dual-Track Memory, Escalation (with honest implementation status)
3. **Longer** — 20-30 pages allows full treatment of everything
4. **Practitioner-facing** — "here's what we learned from building and deploying this"
5. **Less hypothesis-driven, more discovery-driven** — reports findings rather than tests hypotheses
6. **The benchmark lives inside the story** as measurement methodology, not headline contribution

---

## Appendix: Data Inventory for All Three

| Dataset | Runs | Questions | Modality | Policies | Relationships | Status |
|---------|------|-----------|----------|----------|---------------|--------|
| V1 | 4 | 10 | Multi-step (15 ticks) | M0, M1 | R0 | Complete |
| V3 | 4 | 10 | Multi-step (20 ticks, attack mode) | M0, M1 | R0 | Complete |
| Bench200 SS | 9 | 200 | Single-step | M0, M1, M2 | R0 | Complete |
| Bench200 MS | 9 | 200 | Multi-step (220 ticks) | M0, M1, M2 | R0 | Complete (35% misroute bug in SS) |
| Bench20x10 | 60 | 200 (10 splits x 20) | Multi-step (60 ticks) | M0, M1, M2 | R0, R1 | Complete |
| **Total** | **86** | | | | | |

Key numbers to cite:
- M0 multi-step leak rate: **92.4%** (Bench20x10)
- M1 multi-step leak rate: **87.5%** (Bench20x10) → only 5pp improvement
- M2 multi-step leak rate: **35.0%** (Bench20x10) → 57pp improvement
- M2 single-step leak rate: **10.7%** (Bench200) → shows modality effect
- M2 utility cost: **<2.5%** (Bench200)
- R1 relationship effect: **+10.7pp on personal_relationships, -10.0pp on personal_health**
- Self-identity boundary: **100% hold rate** across all runs
