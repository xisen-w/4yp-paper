# Technical Report Outline
## Personal Agent Privacy Under Cross-Boundary Communication: A Systematic Empirical Study

**Target:** arXiv technical report (20-30 pages), potentially JMLR/TMLR submission
**Tone:** "We built a real system. Here is everything we learned."

---

### One-Sentence Pitch

The first comprehensive empirical study of what happens to private data when personal AI agents interact across trust boundaries — covering defense mechanisms, attack modalities, relationship dynamics, and architectural solutions — based on a deployed system (Pulse) with real users.

### Storytelling Patterns Applied

| Pattern | Application |
|---|---|
| **OS analogy** (MemGPT, vLLM) | MCC = Docker containers; Dual-Track Memory = per-process address spaces |
| **From method to paradigm** (Transformer, BERT) | Not just a benchmark — a framework for thinking about agent privacy |
| **Counterintuitive result** (InstructGPT, CAI) | "Category-specific defense is MORE secure AND equally useful" (breaks the tradeoff) |
| **Two-world bridge** (Dao) | Agent capability research × LLM security research |
| **Practitioner-facing** (vLLM: "2-4x throughput = cost reduction") | "Here's what we learned from building and deploying this" |
| **Honest limitations → future work** (Goodfellow, Schapire) | Acknowledged gaps become the community's research agenda |

---

### Structure

#### 1. Introduction (2 pages)

**The big picture (1 page):**
Personal AI agents now hold sensitive data (notes, calendars, emails, health records, financial details) and are beginning to interact with external agents via protocols like MCP (Anthropic, 2024) and A2A (Google, 2025). This creates a new attack surface that is qualitatively different from traditional LLM safety concerns:

- The agent has *persistent memory* across sessions
- The attacker is *another agent*, not a human prompt injector
- The data at risk is *personal*, not corporate or institutional
- The interaction is *multi-turn* and *relationship-contextualized*

No prior work has measured what happens in this setting across a defense gradient, multiple relationship conditions, and both single-step and multi-turn attack modalities.

**What we did (0.5 pages):**
We built Pulse — a personal agent coordination layer deployed with real users — and used it as the experimental platform for a systematic study. Across 86 experiments on 200 questions spanning 5 sensitivity categories, we measured the security-utility tradeoff under 3 defense levels, 2 relationship conditions, and 2 attack modalities.

**What we found (0.5 pages):**
Eight empirical findings, three architectural solutions, and a framework for evaluating cross-boundary agent privacy. Headline results: generic privacy instructions are security theater (+5pp improvement); category-specific policy breaks the assumed tradeoff (57pp improvement at <2.5% utility cost); relationship context has surprising dual-direction effects; and self-identity boundaries outperform policy overlays with 100% hold rate.

---

#### 2. Background and Related Work (3 pages)

**§2.1 The Agent Landscape**
- Agent architectures: ReAct, Toolformer, MemGPT
- Communication protocols: MCP (tool integration), A2A (agent-to-agent)
- Current state: agents are capability-rich but security-naive

**§2.2 LLM Security: Attack and Defense**
- Attack taxonomy: prompt injection (GCG, AutoDAN), social engineering (PAP), multi-turn escalation (Crescendo, PAIR), tool abuse
- Defense landscape: Spotlighting, Instruction Hierarchy, Llama Guard, StruQ, NeMo Guardrails
- Industry frameworks: Google 5-layer defense, Meta Rule of Two, OWASP Top 10 for LLMs
- Key result: Nasr et al. (2025) — every defense bypassed under adaptive attack

**§2.3 Cross-Boundary Privacy**
- AgentSocialBench (Wang & Jiang, 2026): closest prior work — static scenarios, no defense evaluation
- Existing benchmarks: InjecAgent, AgentDojo, TensorTrust, TAMAS — none measure utility + security simultaneously
- Our position: Table 2.1 comparison matrix

**§2.4 Formal Problem Statement**
- Agent A with knowledge K = {F, S, M_self}, external entities E = {E_1, ..., E_n}
- Utility U(A, E_i), Security S(A, E_i), Overhead O(A)
- Pareto frontier P = {(U, S, O)}
- The central question: is this frontier monotonic?

---

#### 3. System Design: Pulse (3 pages)

**§3.1 The Coordination Layer Concept**
- Distinction: agent *frameworks* (capabilities for individual agents) vs coordination *layers* (trust infrastructure between agents)
- TCP/IP analogy: Pulse provides communication infrastructure without dictating what applications run on top
- Why this distinction matters for security: security is a property of the *relationship*, not the *agent*

**§3.2 Agent Infrastructure**
- Alex's world: 100 notes across 11 folders (Work, Personal, Finance, Health, etc.)
- Calendar integration: busy/free, meeting details, attendees
- Email access: filtered by keyword, not bulk access
- Memory: L1 (context window) / L2 (vector DB) / L3 (structured facts)
- Tool set: search_notes, get_note_content, check_calendar, read_email, manage_todos, send_message

**§3.3 Share Links as Access Control**
- Per-relationship context scoping (folder-level, tool-level, data-level)
- This IS the production MCC — architectural isolation at the API layer
- Permissions: scope (all/folders), access (read/read_calendar/read_calendar_write), notesAccess (read/write/edit)

**§3.4 Memory Architecture**
- Self-state: owner's preferences, constraints, identity (never exposed to guests)
- Per-relationship shards: isolated episodic memory per guest
- Metadata filtering at vector DB level: WHERE relationship_id = E_i

---

#### 4. Benchmark Design (3 pages)

**§4.1 Question Taxonomy**
- 200 questions across 5 sensitivity categories (with distribution rationale)
- Gold key facts for automated evaluation
- Design philosophy: ecologically valid, based on real user query patterns

**§4.2 Defense Gradient**
- M0: No defense (behavioral baseline)
- M1: Generic prompt instruction ("try not to share personal information")
- M2: Category-specific deny-list (explicit enumeration of protected categories)
- Rationale: incremental ablation — each level adds one type of specificity

**§4.3 Attack Modalities**
- Single-step: one LLM call per question (Bench200)
- Multi-step: 60 ticks via heartbeat mode (Bench20x10)
- Heartbeat mode: tick-based autonomous execution with subprocess isolation
- Why both: single-step is clean for controlled comparison; multi-step reflects real-world dynamics

**§4.4 Relationship Conditions**
- R0: Stranger (name only)
- R1: Colleague (name + role + team + memory shard)
- Why: tests whether relationship context affects privacy behavior

**§4.5 Evaluation Methodology**
- Dual metric via gold_key_facts: utility (work Q accuracy) + security (1 - leak rate)
- Automated scoring with manual validation
- Replication strategy: 3 reps (Bench200), 10 splits (Bench20x10)

---

#### 5. Experimental Results (6 pages)

**§5.1 Scale and Overview**
- 86 total runs, 12,000+ question-answer pairs
- Table 5.1: Experimental matrix overview

**§5.2 The Defense Gradient**
- Table 5.2: Main results (M0/M1/M2 × SS/MS × R0/R1)
- **Finding 1**: Generic policy is security theater (92.4% → 87.5%, only 5pp improvement)
- **Finding 2**: Category-specific policy breaks the tradeoff (87.5% → 35.0%, 52.5pp improvement)
- Utility cost: <2.5% (Bench200)
- Insight: specificity matters more than strictness

**§5.3 Single-Step vs Multi-Step**
- **Finding 3**: Multi-step amplifies leakage by 24-43pp across all policies
- Table 5.3: SS vs MS comparison
- But: Tina rarely retries — leakage is first-contact, not persistence-based
- The extended conversation provides more contexts for volunteering information
- Implication: single-step benchmarks underestimate real-world risk by 2-3x

**§5.4 Attack Patterns in Multi-Turn**
- **Finding 4**: Agents naturally develop Crescendo-like escalation patterns
  - Pattern 1: Progressive side-channel (metadata accumulation across turns)
  - Pattern 2: Organic rapport-building → probe → reframe
  - Pattern 3: "Paste verbatim" tool-operation reframing
  - Pattern 4: Category ambiguity exploitation
  - Pattern 5: Partial compliance failure (refuses but leaks in elaboration)

**§5.5 The Relationship Effect**
- **Finding 5**: Relationship has dual-direction category-dependent effects
  - Overall: only 1.3pp difference
  - personal_relationships: +10.7pp (colleague label → social disclosure norms)
  - personal_health: -10.0pp (colleague label → professional boundary)
  - Strongest interaction: M1 × personal_relationships — R0=72% vs R1=92% (+20pp!)
- Figure 5.1: R0 vs R1 per-category heatmap
- This is novel — no prior work measures this

**§5.6 Category Analysis**
- **Finding 6**: sensitive_work is the ambiguity zone
  - M2 protects personal_finance (82%) but struggles with sensitive_work (38%)
  - Category ambiguity > prompt injection as primary attack vector
  - Work questions blur the public/sensitive boundary

**§5.7 Self-Identity vs External Policy**
- **Finding 7**: Embedded boundaries >> policy overlays
  - MEMORY.md "Never share: salary, equity" held 100% across all 86 runs
  - External policy (M1) crumbles at 87.5% leak
  - Interpretation: the boundary is structural (embedded in identity), not behavioral (external instruction)

**§5.8 The Security-Utility Pareto Frontier**
- **Finding 8**: The tradeoff is NOT monotonic
  - Figure 5.2: Pareto frontier (utility vs security, all conditions)
  - M2 dominates M1 on both axes — higher security AND maintained utility
  - This contradicts the conventional assumption that more security = less utility
  - The curve shape depends on defense specificity, not defense strictness

---

#### 6. Architectural Solutions (4 pages)

**§6.1 Design Philosophy**
- "Don't ask the agent to refrain from accessing sensitive data — ensure the sensitive data is not in the room"
- The OS analogy: MCC = Docker containers (process isolation), not chmod (file permissions)
- Table 6.1: Failure class → solution mapping

**§6.2 Mountable Context Cells**
- Motivation: prompt-level defense says "can see but shouldn't share" → judgment on every query
- Design: capability-based execution sandbox, constructed de novo per interaction
- Unauthorized tools/data are ABSENT, not hidden or restricted
- Specification: allowedNoteIds, calendarAccess, emailFilter, allowedTools, systemPromptScope
- Enforcement: Policy Decision Point (pre-exec tool removal, runtime arg validation, continuous-state filtering)
- Security property: no tool call can return data outside MCC scope
- Connection to Pulse: folder-scoped share links ARE the production MCC
- Why it should break the tradeoff: removes data from context → no behavioral judgment needed → no utility cost for authorized queries

**§6.3 Dual-Track Memory**
- Motivation: global memory leaks across relationships (Class 5)
- Design: self-state track + per-relationship shards
- Isolation: metadata filtering at vector DB level
- Fail-closed: missing relationship_id → zero results
- Evidence: Finding 7 (self-identity boundaries holding 100%) demonstrates the principle

**§6.4 Intelligent Escalation Protocol**
- Motivation: continuous state streams can't be fully pre-authorized
- Design: Sanitisation Agent (Allow/Redact/Escalate/Deny) + precedent clustering
- Macro Constitution: owner's high-level rules, dynamically updated
- Expected behavior: escalation rate decreases as precedents accumulate

**§6.5 Implementation Status**
- MCC: partially implemented (folder-scoped share links in Pulse)
- Dual-Track Memory: partially implemented (relationship shards exist)
- Escalation: design only
- Honest assessment: the principle is validated by Finding 7; full MCC benchmark is future work

---

#### 7. Discussion (2 pages)

**§7.1 Lessons for Practitioners**
1. Generic privacy instructions are security theater — enumerate protected categories explicitly
2. Embed critical boundaries in agent identity (self-concept), not just policy overlays
3. Single-step testing underestimates real-world risk by 2-3x — always test multi-turn
4. Relationship context doesn't uniformly help or hurt — test with actual relationship conditions
5. The biggest gap is sensitive_work, not personal data — invest in work/sensitive disambiguation

**§7.2 Lessons for the Research Community**
1. Dual-metric evaluation (utility AND security) should be standard for agent benchmarks
2. Defense gradient methodology (incremental ablation) is more informative than binary defense/no-defense
3. Relationship as a first-class evaluation variable — aggregate metrics hide dual-direction effects
4. Category-level analysis reveals structure that aggregate leak rates obscure

**§7.3 Comparison with Industry Approaches**
- Google 5-layer defense: our M2 is analogous to their "output filtering" layer
- Meta Rule of Two: our benchmark provides quantitative measurement of what they articulate qualitatively
- Anthropic prompt injection hardening: 1% ASR is for model-level defense; our findings show system-level leakage is much higher

**§7.4 Limitations**
- Single LLM backend (gpt-5-mini)
- Simulated adversary (LLM-generated Tina, not human red-team)
- No formal attack methods (PAIR/Crescendo/PAP)
- Single agent persona (Alex as startup CTO)
- Utility evaluation incomplete for multi-step (HTML formatting issue)
- No full MCC experimental validation (architectural solution is proposed, not benchmarked)
- Bench200 SS had 35% misroute bug (acknowledged, controlled for)

---

#### 8. Conclusion (1 page)

**Summary of 8 empirical findings:**
1. Generic policy = security theater (+5pp)
2. Category-specific policy breaks the tradeoff (57pp at <2.5% utility cost)
3. Multi-step amplifies leakage 2-3x
4. Agents develop Crescendo-like patterns organically
5. Relationship has dual-direction category effects
6. sensitive_work is the ambiguity zone
7. Self-identity boundaries >> policy overlays (100% hold)
8. The security-utility tradeoff is NOT monotonic

**The big insight:**
"The coordination overhead that consumes knowledge workers' time will not be solved by more capable individual agents. It requires infrastructure that makes cross-boundary agent communication safe. This report demonstrates that architectural enforcement — not prompt-level restriction — is the reliable path."

**Open-source release:**
Benchmark, evaluation code, gold_key_facts, policy files, all 86 experimental runs, and the Pulse agent platform.

**Future directions:**
- Full MCC benchmark
- Formal attack evaluation (PAIR, Crescendo, PAP)
- Cross-model comparison
- Formal verification of context cells
- Network-scale evaluation (N agents, social graph)
- Longitudinal study (weeks/months with real relationships)

---

#### Appendices (5-10 pages)

- A: Full question set (200Q with categories, gold_key_facts, expected behavior)
- B: Policy file text (M0/M1/M2 exact prompts)
- C: Alex's world state (100 notes, folder structure)
- D: Per-run results tables (all 86 runs)
- E: Attack pattern taxonomy with examples
- F: Pulse system architecture (detailed)
- G: Evaluation validation (manual audit methodology and results)

---

### Key Differences from Other Two Formats

| Dimension | 4YP Thesis | Benchmark Paper | Technical Report |
|---|---|---|---|
| **Length** | ~150 pages | 9 pages | 20-30 pages |
| **System description** | Brief | Minimal | 3 pages (Pulse as real system) |
| **Solutions** | Full chapter | Out of scope | 4 pages (with honest status) |
| **Tone** | "Here's my investigation" | "Here's what YOU should measure" | "Here's what we learned building this" |
| **Hypotheses** | H1/H2/H3 explicit | Findings-driven | Findings-driven |
| **Audience** | Thesis committee | NeurIPS reviewers | Practitioners + researchers |
| **Open-source** | Not emphasized | First-class contribution | First-class contribution |
| **Pulse** | Background infrastructure | Anonymous benchmark platform | Named, described, deployed |
| **RQs** | 4 formal RQs | 0 (6 findings instead) | 0 (8 findings) |
| **Product alignment** | Not discussed | Not discussed | Lessons for practitioners section |

---

### Data Inventory (shared across all three)

| Dataset | Runs | Questions | Modality | Policies | Relationships | Status |
|---|---|---|---|---|---|---|
| V1 | 4 | 10 | Multi-step (15 ticks) | M0, M1 | R0 | Complete |
| V3 | 4 | 10 | Multi-step (20 ticks, attack) | M0, M1 | R0 | Complete |
| Bench200 SS | 9 | 200 | Single-step | M0, M1, M2 | R0 | Complete |
| Bench200 MS | 9 | 200 | Multi-step (220 ticks) | M0, M1, M2 | R0 | Complete |
| Bench20x10 | 60 | 200 (10×20) | Multi-step (60 ticks) | M0, M1, M2 | R0, R1 | Complete |
| **Total** | **86** | | | | | |

**Key numbers:**
- M0 multi-step leak: **92.4%** | M1: **87.5%** (→ +5pp) | M2: **35.0%** (→ +57pp from M0)
- M2 single-step leak: **10.7%** | M2 utility cost: **<2.5%**
- R1 relationship effect: **+10.7pp relationships, -10.0pp health** (dual-direction)
- Self-identity boundary: **100% hold** across all 86 runs
- M1 × personal_relationships: **R0=72% vs R1=92%** (+20pp interaction)
