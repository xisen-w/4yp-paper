# 4YP Thesis Outline
## Pulse: Empirical Analysis of the Security-Utility Tradeoff in Cross-Boundary Agent Communication

**Author:** Xisen Wang | **Supervisor:** Professor Philip Torr | **College:** Keble
**Target length:** ~150 pages | **Deadline:** Trinity Term 2026

---

### Thesis Statement

When personal AI agents communicate across trust boundaries, the severity of privacy leakage depends on three factors — defense specificity, attack modality, and inter-agent relationship — in ways the research community has not previously measured. This thesis provides the first systematic empirical study of the security-utility tradeoff in cross-boundary agent communication, revealing that the tradeoff is not monotonic and that relationship context has surprising dual-direction effects on privacy.

### Core Narrative (3 sentences)

> Nobody has measured what happens to private data when personal AI agents talk to each other across trust boundaries. We built a benchmark (200 questions × 5 sensitivity categories × 3 defense levels × 2 relationship conditions × 2 attack modalities) and ran 86 experiments on a deployed agent system. We found that generic privacy instructions are security theater (+5pp), that category-specific policy breaks the assumed security-utility tradeoff (57pp improvement at <2.5% utility cost), and that relationship context has dual-direction effects that depend on the data category.

### Storytelling Patterns Applied

| Pattern (from our analysis) | How this thesis applies it |
|---|---|
| **Concrete opening example** (Daskalakis, Roughgarden) | Alice's agent reveals her Competitor Corp meeting to an investor |
| **Clean question** (Schapire) | "Is the security-utility tradeoff monotonic?" |
| **Dramatic failure** (SWE-bench, GSM8K) | "92% of sensitive info leaks; generic policy reduces this by only 5pp" |
| **Taxonomy as contribution** (HELM, MTEB) | categories × defenses × relationships = framework for thinking |
| **Counterintuitive result** (TruthfulQA, InstructGPT) | Colleague label increases relationship leaks but decreases health leaks |
| **OS analogy** (MemGPT, vLLM) | MCC = Docker containers (can't see), not chmod (shouldn't see) |
| **Two-world bridge** (Dao, Karpathy) | Agent capability research × LLM security research |
| **Thesis as curriculum** (Finn, Zaharia) | foundational framework (Ch3) that papers lack |
| **Honest limitations** (Schapire, Goodfellow) | RQ3/RQ4 are design proposals, not experimentally validated |

---

### Chapter Outline

#### Chapter 1: Introduction (8-10 pages)

**Opening paragraph**: A concrete scenario — Alice is a startup founder. Her AI agent holds her notes, calendar, and emails. An investor's agent asks "When is Alice free next Tuesday?" Alice's agent, trying to be helpful, reveals she has a meeting at a competitor's headquarters. No malice was needed. No attack was mounted. The agent simply lacked a framework for distinguishing what should be shared from what should not.

- §1.1 The Rise of Personal Agents — and the Communication Gap
  - Agents are becoming persistent digital proxies (ReAct, Toolformer, MCP, A2A)
  - Critical gap: no infrastructure for *cross-boundary* communication
  - The "coordination tax" problem
- §1.2 The Security Problem: Why Agents Remain Siloed
  - Granting agents deep personal context = maximally useful + maximally dangerous
  - Nasr et al. (2025): every defense bypassed at >90%; human red-teaming: 100%
  - Meta "Rule of Two": agent is critically vulnerable when it processes untrusted input + accesses sensitive data + can take actions
- §1.3 The Security-Utility Paradox
  - Maximum coordination utility requires maximum context access, which creates maximum vulnerability
  - Current solutions cluster at extremes: permissive (insecure) or restrictive (useless)
  - **No existing benchmark measures both dimensions simultaneously**
- §1.4 Research Approach: Benchmark-First Methodology
  - Build evaluation → reveal failures → design solutions motivated by those failures
  - (Yao's pattern: WebShop → ReAct)
- §1.5 Contributions
  1. First dual-metric benchmark for cross-boundary agent privacy (200Q, 5 categories, dual eval)
  2. Empirical characterization of the tradeoff across defense/relationship/modality (86 runs)
  3. Discovery of dual-direction relationship effect on privacy (novel empirical finding)
  4. Architectural solution designs (MCC, Dual-Track Memory) with indirect evidence
- §1.6 Research Questions
  - RQ1: What are the failure modes when agents communicate across trust boundaries?
  - RQ2: How does defense specificity affect the security-utility tradeoff?
  - RQ3: How should agent memory be redesigned for multi-party interactions? *(design + indirect evidence)*
  - RQ4: Does relationship context shift the security-utility tradeoff curve? *(novel: replaces old RQ4 about escalation)*
- §1.7 Thesis Organization (roadmap paragraph)

#### Chapter 2: Related Work (12-15 pages)

- §2.1 AI Agent Architectures (brief: ReAct, Toolformer, MemGPT, MCP, Google A2A)
- §2.2 LLM Security: Attacks
  - Taxonomy: prompt injection (GCG, AutoDAN), social engineering (PAP), multi-turn escalation (Crescendo, PAIR), tool abuse, memory contamination
  - Key insight: "the attacker moves second" (Nasr et al.)
- §2.3 LLM Security: Defenses
  - Prompt-level: Spotlighting, Instruction Hierarchy, NeMo Guardrails
  - Model-level: Llama Guard, Anthropic hardening
  - Architectural: StruQ (conceptually closest to MCC)
  - Industry: Google 5-layer defense, Meta Rule of Two, OWASP Top 10 for LLMs
- §2.4 Agent Security Benchmarks
  - Table 2.1: comparison matrix (InjecAgent, AgentDojo, TensorTrust, TAMAS, AgentSocialBench, HackAPrompt)
  - Dimensions: single-turn vs multi-turn, attack vs defense, utility measured?, relationship varies?
- §2.5 Our Position
  - The "two-world bridge": agent capability papers don't measure privacy; security papers don't measure utility
  - AgentSocialBench is closest but lacks defense gradient, adaptive attacks, and utility measurement
  - We occupy the intersection

#### Chapter 3: Problem Formulation (8-10 pages)

- §3.1 Formal Setup
  - Agent A with owner U, knowledge base K = {F, S, M_self}
  - External entity set E = {E_1, ..., E_n} with relationship function R(U, E_i)
  - Communication protocol: query-response with tool access
- §3.2 The Context-Security Tradeoff
  - Utility U(A, E_i): task completion quality
  - Security S(A, E_i): sensitive data protection rate
  - Overhead O(A): escalation/manual intervention rate
  - Pareto frontier P = {(U, S, O) : no config dominates on all three}
- §3.3 Threat Model
  - 5 attack classes (with formal definitions, not just names)
  - Class 1: Direct prompt injection (override system instructions)
  - Class 2: Social engineering (manipulate reasoning chain)
  - Class 3: Multi-query inference (accumulate metadata across turns)
  - Class 4: Tool abuse (hijack tool calls for exfiltration)
  - Class 5: Memory contamination (cross-relationship leakage)
- §3.4 **Hypotheses** (NEW — make the thesis testable)
  - H1: Prompt-level defenses exhibit a monotonic security-utility tradeoff
  - H2: Architectural defenses (MCC) can break this monotonicity
  - H3: Relationship context shifts the tradeoff curve in category-dependent ways
- §3.5 Research Questions (RQ1-RQ4 formally tied to H1-H3)

#### Chapter 4: Benchmark Design (15-18 pages)

- §4.1 Agent Infrastructure
  - Alex's world: 100 notes across 11 folders, calendar, email, todos
  - Tina's agent: external entity with configurable relationship context
  - Tool set: search_notes, get_note_content, check_calendar, read_email, etc.
  - Figure 4.1: System architecture diagram
- §4.2 Question Design
  - 200 questions across 5 sensitivity categories
  - Table 4.1: Category distribution + representative examples
  - Gold key facts: per-question ground truth for automated evaluation
  - Design philosophy: ecologically valid (based on real user data patterns)
- §4.3 Defense Gradient
  - M0: No defense (full context access, no policy)
  - M1: Generic prompt ("try not to share personal information")
  - M2: Category-specific deny-list (explicit enumeration of protected categories)
  - Exact policy text for each (reproducibility)
  - Discussion: why M0/M1/M2 not the original B1/B2/A/B/C naming
- §4.4 Attack Modalities
  - Single-step: 200 questions in batch, one LLM call per question
  - Multi-step: 60 ticks via heartbeat mode, Tina asks 20 questions with retry
  - Figure 4.2: Tick lifecycle diagram (heartbeat mode)
- §4.5 Relationship Conditions
  - R0: Tina is authenticated stranger (name only)
  - R1: Tina is "Product Manager, colleague, works on Project Alpha" (memory shard)
- §4.6 Evaluation Methodology
  - gold_key_facts string matching for both utility AND security
  - What counts as "leaked" vs "refused" vs "correctly answered"
  - Cross-validation: manual audit of 100 random evaluations
- §4.7 Experimental Matrix
  - Table 4.2: Full matrix — 3 policies × 2 relationships × 2 modalities × 200Q
  - 86 total runs across all experiments
  - Replication: 3 reps per condition for Bench200, 10 splits for Bench20x10

#### Chapter 5: Results I — Failure Analysis (20-25 pages)

*Purpose: "How bad is it?" — the diagnostic chapter*

- §5.1 **Headline Result: 92% Leak Rate Under No Defense**
  - Table 5.1: Main results — M0/M1/M2 × R0/R1 × SS/MS
  - Figure 5.1: The Pareto frontier (scatter plot, utility vs security, all conditions)
  - Lead with the dramatic number (GSM8K pattern: "can't do grade-school math")

- §5.2 **Generic Policy Is Security Theater**
  - M0 → M1: leak rate drops from 92.4% to 87.5% (only 5pp)
  - "Telling the agent 'don't share sensitive info' barely matters"
  - This is the "inverse scaling" / "counterintuitive" hook

- §5.3 **Category-Specific Analysis**
  - Table 5.2: Per-category leak rates
  - M2 strongest: personal_finance (18% leak), personal_health
  - M2 weakest: sensitive_work (62% leak) — the ambiguity zone
  - Category ambiguity is the primary attack vector (attack_patterns.md)
  - Why: work questions blur the boundary between public and sensitive

- §5.4 **Single-Step vs Multi-Step**
  - Table 5.3: Bench200 SS vs Bench20x10 MS comparison
  - Multi-step amplifies leakage by +24-43pp across all policies
  - But: Tina rarely retries (only 2 extra calls in 20 M2 runs)
  - Leakage is mostly first-contact, not retry-based
  - Implication: single-step benchmarks underestimate real-world risk by 2-3x

- §5.5 **Attack Patterns in Multi-Turn**
  - Pattern 1: Progressive side-channel (V3 G1: metadata accumulation across 11 ticks)
  - Pattern 2: Organic Crescendo-like escalation (establish rapport → probe → retry with reframing)
  - Pattern 3: "Paste verbatim" tool-operation reframing
  - Pattern 4: Category ambiguity exploitation (reclassifying sensitive_work as work_public)
  - Pattern 5: Partial compliance failure (refuses explicit answer but leaks in elaboration)

- §5.6 **Self-Identity vs External Policy**
  - MEMORY.md "Never share: salary, equity" held 100% across ALL runs (V1, V3, Bench200, Bench20x10)
  - External policy (M1 "try not to share") crumbles under multi-turn: 87.5% leak
  - Interpretation: boundaries embedded in agent identity > policy overlays
  - This is the strongest indirect evidence for H2 (architectural > prompt)

- §5.7 **Attack Taxonomy with Quantitative Data**
  - Table 5.4: 5 attack classes with counts from both datasets
  - Distribution: direct injection (40%), social engineering (25%), inference (20%), tool abuse (10%), memory contamination (5%)

#### Chapter 6: Solution Proposal — Architectural Defense (12-15 pages)

*Purpose: "What should we build?" — motivated by Ch5 failures*

- §6.1 From Diagnosis to Treatment
  - Table 6.1: Each failure class → which solution addresses it
  - Philosophy: "Don't ask the agent to refrain — ensure the data is not in the room"
  - **The OS analogy**: MCC = Docker containers (process isolation), not chmod (file permissions)

- §6.2 Dual-Track Memory (addresses Class 5: memory contamination)
  - Motivation: global memory leaks across relationships
  - Design: self-state track (owner's core context) + per-relationship shards
  - Isolation: metadata filtering at vector DB level (WHERE relationship_id = E_i)
  - Fail-closed: missing relationship_id → zero results, not global fallback
  - Three-tier hierarchy: L1 (working memory) / L2 (episodic) / L3 (semantic)
  - Evidence: F2 (self-identity holding 100%) shows identity-embedded isolation works

- §6.3 Mountable Context Cells (addresses Classes 1, 2, 4)
  - Motivation: prompt-level defense says "can see but shouldn't share" → judgment on every query
  - Design: capability-based execution sandbox constructed *de novo* per interaction
  - Key difference: unauthorized tools/data are *absent*, not hidden or restricted
  - MCC specification: allowedNoteIds, calendarAccess, emailFilter, allowedTools, systemPromptScope
  - Policy Decision Point (PDP): pre-execution tool removal, runtime argument validation, continuous-state filtering
  - Connection to Pulse: folder-scoped share links ARE the production MCC
  - Security guarantee: no tool call can return data outside MCC scope (architectural, not behavioral)

- §6.4 Intelligent Escalation Protocol (addresses Class 3 and overhead)
  - Motivation: continuous state streams (email, calendar) can't be pre-authorized
  - Design: Sanitisation Agent with 4 decisions (Allow/Redact/Escalate/Deny)
  - Precedent-based learning: relational clustering → auto-approve routine queries
  - Macro Constitution: owner's high-level rules, dynamically updated

- §6.5 Implementation Status (honest)
  - Dual-Track Memory: partially implemented (relationship shards exist in Pulse)
  - MCC: partially implemented (folder-scoped share links = production version)
  - Escalation: design only, not implemented
  - What we CAN claim: the principle works (F2), the architecture is sound, full validation is future work

#### Chapter 7: Results II — Defense Evaluation (15-18 pages)

*Purpose: "What works?" — the prescriptive chapter*

- §7.1 **M2 as Strong Prompt-Level Defense**
  - Single-step: 10.7% leak (vs 49% M0) — a 4.6x reduction
  - Multi-step: 35.0% leak (vs 92.4% M0) — a 2.6x reduction
  - Utility cost: <2.5% (Bench200)
  - Key insight: **category specificity matters more than strictness**

- §7.2 **Defense Effectiveness by Category**
  - Table 7.1: Per-category protection rates under M2
  - personal_finance: 82% protected (strongest — clear boundary between "mine" and "yours")
  - personal_health: high protection
  - sensitive_work: only 38% protected (weakest — the ambiguity zone)
  - Analysis: why work-boundary questions are hardest (legitimate work context bleeds into sensitive)

- §7.3 **The Relationship Effect** (novel empirical contribution)
  - Table 7.2: R0 vs R1 per-category per-policy
  - Overall: small difference (1.3pp)
  - But per-category: **dual-direction effect**
    - personal_relationships: R1 leaks MORE (+10.7pp) — "colleague" activates social disclosure norms
    - personal_health: R1 leaks LESS (-10.0pp) — "colleague" triggers professional boundary
  - Strongest interaction: M1 × personal_relationships → R0=72% vs R1=92% (+20pp!)
  - Interpretation: relationship context doesn't uniformly help or hurt — it activates different social norms for different data categories
  - This finding has no precedent in the literature

- §7.4 **The Security-Utility Pareto Frontier**
  - Figure 7.1: **The key figure** — scatter plot with all conditions
  - X-axis: utility (work question accuracy), Y-axis: security (1 - leak rate)
  - M0, M1, M2 points for SS and MS; R0 and R1 variants
  - Key observation: M2 dominates M1 on BOTH axes — the tradeoff is NOT smoothly monotonic
  - Projected MCC position (with clear caveats about indirect evidence)

- §7.5 **Hypothesis Testing**
  - H1 (prompt-level monotonic): **Partially supported** — M0→M1 is near-flat, M1→M2 breaks the curve upward. Within prompt-level, specificity is the key variable, not strictness.
  - H2 (architectural breaks it): **Indirectly supported** — F2 (100% hold for self-identity) + MCC design analysis. Full experimental validation is future work.
  - H3 (relationship shifts curve): **Supported with nuance** — not simple "helps" or "hurts" but category-dependent dual effect. The tradeoff curve genuinely shifts shape depending on the relationship.

- §7.6 **Comparison with Academic Baselines**
  - Conceptual comparison: Spotlighting, Instruction Hierarchy, StruQ
  - Where our defense gradient sits relative to each
  - What we can and cannot claim without running these baselines

- §7.7 **Threats to Validity**
  - Single LLM backend (gpt-5-mini) — model-dependent results
  - Simulated adversary (Tina is LLM-generated, not human red-team)
  - Utility evaluation gaps (44/61 Bench20x10 runs have 0 utility tracked due to HTML formatting)
  - No formal attack methods (PAIR/Crescendo not yet implemented)
  - Bench200 SS had 35% misroute bug (acknowledged, controlled for)

#### Chapter 8: Conclusion (6-8 pages)

- §8.1 Summary of Findings
  - RQ1: 5 attack classes, quantified from 86 runs. Category ambiguity is the primary vector.
  - RQ2: Generic policy = security theater (+5pp). Category-specific = breakthrough (57pp at <2.5% cost). The tradeoff is not monotonic.
  - RQ3: Dual-Track Memory design addresses memory contamination. Indirect evidence (F2) supports architectural isolation. (Design contribution, not experimental.)
  - RQ4 (reframed): Relationship context has dual-direction effects — helps for health, hurts for relationships. M1 × relationship interaction reaches +20pp.

- §8.2 Contributions
  1. **First dual-metric benchmark** for cross-boundary agent privacy (200Q, 5 categories, gold_key_facts eval)
  2. **Empirical characterization** of the security-utility tradeoff across defense × relationship × modality (86 runs, 12,000+ QA pairs)
  3. **Discovery of dual-direction relationship effect** on privacy (novel: no prior work measures this)
  4. **Architectural solution design** (MCC, Dual-Track Memory) with indirect evidence from self-identity boundaries

- §8.3 Limitations
  - No full MCC experimental validation
  - Simulated adversary, not human red-team
  - Single model backend
  - Utility evaluation incomplete for multi-step
  - No comparison with formal attack methods (PAIR/Crescendo/PAP)

- §8.4 Future Work
  - Full MCC benchmark (implement folder-scoping in experiment pipeline)
  - PAIR/Crescendo/PAP formal attack evaluation
  - Cross-model comparison (Claude, Gemini, Llama)
  - Formal verification of context cell isolation properties
  - Transitive trust attacks (C3: friend-as-proxy)
  - Differential privacy for agent communication
  - Network-scale evaluation (N agents, social graph)

- §8.5 Concluding Remarks
  - "Don't ask the agent to refrain from accessing sensitive data — ensure the sensitive data is not in the room."
  - The coordination overhead problem will not be solved by more capable individual agents — it requires trust infrastructure between agents.

#### Appendices

- A: Full question set (200Q with categories, gold key facts, expected behavior)
- B: Policy file text (M0/M1/M2 exact prompts)
- C: Alex's world state (100 notes across 11 folders, abbreviated)
- D: Detailed per-run results tables

---

### Key Changes from Current .tex Structure

| Current .tex | This Outline | Why |
|---|---|---|
| Configs named B1/B2/A/B/C | M0/M1/M2/MCC | Match actual experiments |
| Ch5 qualitative only | Ch5 filled with Bench200 + Bench20x10 data | Most cited sections need numbers |
| Ch7 all empty (`---`) | Ch7 filled with M2 analysis + relationship effects + Pareto figure | Critical gap |
| H1/H2/H3 implicit | Explicit hypotheses in Ch3 | Gives thesis a testable spine |
| No relationship results | §7.3 dedicated to R0/R1 dual-direction finding | Novel contribution |
| RQ4 = escalation learning | RQ4 = relationship effect | Better match for available data |
| Abstract claims "evaluate solutions" | Honest: RQ3/RQ4 are design + indirect evidence | Maintains credibility |
