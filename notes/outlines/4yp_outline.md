# 4YP Thesis Outline
## SharedOS: Privacy Governance in Multi-Agent Shared Delegation Systems

**Author:** Xisen Wang | **Supervisor:** Professor Philip Torr | **College:** Keble
**Target length:** ~150 pages | **Deadline:** Trinity Term 2026

---

### Story Arc

```
Problem Formulation → SharedOS Construction → Benchmarking (PACT-PAIR + PACT-NET) → Solutions
```

The thesis tells a complete engineering-research story:
1. We formulate cross-boundary agent delegation as a distinct security problem where enforcement is delegated to reasoning, making the security-utility frontier emergent
2. We build SharedOS to study it: a full multi-agent shared delegation system with state, tools, governance, and relationship context
3. We benchmark systematically: PACT-PAIR (dyadic, controlled) establishes the frontier's properties; PACT-NET (network, 25 agents) tests whether they generalise
4. We propose and test architectural solutions (MCC, escalation protocol) that move enforcement from reasoning to structure

---

### Thesis Statement

When enforcement of privacy policy is delegated to an LLM's contextual reasoning, the security-utility frontier becomes emergent: shaped by the model's implicit social norms, the semantic properties of the data, and the requester's conversational framing. This thesis presents SharedOS, a multi-agent shared delegation system, uses it to chart this frontier across three axes (policy specificity, interaction length, relationship context), and proposes architectural interventions that move enforcement from reasoning to structure.

### Core Narrative (3 sentences)

> Personal AI agents are becoming delegates that hold private data, wield tools, and represent their owners to other agents. We built SharedOS to study what happens when these delegates interact across ownership boundaries, and discovered that the security-utility frontier is not designed but emergent: generic policies are inert, multi-turn interaction creates novel leakage channels, and relationship context reshapes the boundary in ways no single policy can anticipate. Our architectural solutions (Mountable Context Cells, Escalation Protocol) address this by ensuring sensitive data is absent from the reasoning context rather than asking the agent to refrain from sharing it.

---

### Part I: Problem Formulation (Ch 1-2, ~25 pages)

#### Chapter 1: Introduction (10-12 pages)

**Opening**: Alice is a startup founder. Her AI agent holds her notes, calendar, and emails. An investor's agent asks "When is Alice free next Tuesday?" Alice's agent reveals she has a meeting at a competitor's headquarters. No malice. No attack. The delegate simply lacked a governance framework for cross-boundary communication.

- §1.1 The Rise of Personal Agent Delegates
  - Agents evolving: tools (single-turn) → assistants (multi-turn) → delegates (persistent, autonomous)
  - The delegate model: deep context access + act on behalf of owner
  - Protocols: MCP (tool access), A2A (agent-to-agent communication)
  - Critical gap: delegation assumes trust infrastructure that doesn't exist

- §1.2 The Cross-Boundary Delegation Problem
  - When Agent A contacts Agent B across an ownership boundary
  - Every exchange is a permission decision: what to share, withhold, refuse
  - A delegate that refuses everything is safe but useless; one that shares everything is useful but dangerous
  - The security-utility frontier: the set of achievable operating points

- §1.3 Why This Is Different From Traditional Access Control
  - Bell-LaPadula / Denning: policy IS enforcement (deterministic)
  - LLM delegation: policy is ONE INPUT to reasoning (stochastic)
  - The frontier is no longer designed but emergent
  - Cannot predict from policy text where the boundary will fall; can only measure it
  - The model has implicit social norms from pretraining that compose with policy unpredictably

- §1.4 Research Questions
  - RQ1: What moves the frontier? (Policy specificity)
  - RQ2: Is the frontier stable over time? (Multi-turn interaction)
  - RQ3: Is the frontier the same for everyone? (Relationship context)
  - RQ4: Can architectural interventions move enforcement from reasoning to structure? (Solutions)

- §1.5 Contributions
  1. **Problem formulation**: Cross-boundary delegation as the setting where enforcement is delegated to reasoning, making the frontier emergent
  2. **Platform (SharedOS)**: Full multi-agent delegation system with configurable state, tools, governance, and relationships
  3. **Benchmarking (PACT-PAIR + PACT-NET)**: 600 dyadic tasks + 997 network tasks, dual-metric scoring, six model families
  4. **Architectural solutions**: MCC and Escalation Protocol, with experimental validation

- §1.6 Thesis Organisation

---

#### Chapter 2: Related Work (12-15 pages)

- §2.1 AI Agent Architectures
  - Single-agent: ReAct, Toolformer, MemGPT
  - Multi-agent: AutoGen, CrewAI, MetaGPT
  - Agent OS: AIOS, OS-Copilot
  - Gap: no system addresses privacy governance in cross-boundary delegation

- §2.2 LLM Security and Privacy
  - Attacks: GCG, AutoDAN, PAIR, PAP, Crescendo
  - Defenses: Spotlighting, Instruction Hierarchy, Llama Guard, NeMo Guardrails
  - Key: "the attacker moves second" (Nasr et al.) — adaptive attacks bypass all prompt-level defenses
  - Privacy: differential privacy for LLMs, machine unlearning, membership inference

- §2.3 Agent Security Benchmarks
  - Comparison table: InjecAgent, AgentDojo, TensorTrust, TAMAS, AgentSocialBench, ConVerse, PAC-BENCH, MAGPIE, AgentLeak, Agents of Chaos
  - Dimensions: cross-boundary? tool-mediated? dual metric? multi-turn? relationship?
  - Gap: none combines all of these in a single platform
  - Position: SharedOS + PACT-PAIR/NET occupies the intersection

- §2.4 Trust and Access Control
  - Classical: RBAC, ABAC, BLP, capability-based security
  - Agent-specific: CAMEL, social contracts
  - OS-level isolation: containers, namespaces, sandboxing
  - Our position: SharedOS applies OS isolation principles to agent delegation
  - Key differentiation: traditional AC = policy is enforcement; our setting = policy is input to reasoning

---

### Part II: SharedOS Construction (Ch 3, ~20 pages)

#### Chapter 3: SharedOS — Design, Architecture, and Implementation (18-22 pages)

*This is the METHOD chapter: what we built, why, and how*

- §3.1 Design Philosophy
  - "The personal agent as an operating system"
  - Analogy: OS provides process isolation + IPC + access control → SharedOS provides agent isolation + delegation + governance
  - Key insight: same tool that enables utility (searching notes to answer a colleague) also enables leakage
  - Design goal: independently configurable state, tools, governance, and relationship context

- §3.2 Architecture Overview
  - Figure: SharedOS architecture diagram
  - Two agents (Owner's agent, External agent) with private state
  - Cross-boundary delegation layer mediates all requests
  - Relationship context modulates the delegation
  - Heartbeat engine for autonomous multi-turn interaction

- §3.3 State Layer
  - **Files**: Notes organised in hierarchical namespace (11 folders, 127 notes)
  - **Structured State**: Todos, calendar events, CRM contacts (83 objects)
  - **Memory**: Agent-curated summaries, relationship shards, accumulated context
  - Each owner has a private namespace; delegation = controlled exposure of namespace slices
  - Ground-truth sensitivity labels (used by evaluator, invisible to agent)

- §3.4 Tool Layer
  - **Read tools**: searchNotes, getNoteById, searchTodos, listCalendar
  - **Write tools**: createNote, editNote, completeTodo, sendMessage
  - Tools are the ONLY interface to state (agent cannot bypass them)
  - Trust decomposition: Read trust (who can SEE) vs Write trust (who can MODIFY)
  - Tool results flow directly into generation context → creates conditions for both utility and leakage

- §3.5 Governance Policy Layer
  - D0 (no policy): system prompt contains no privacy instructions
  - D1 (generic): "Use your best judgment to protect private information"
  - D2 (category-specific): explicit deny list enumerating four protected categories
  - D3-D5 (advanced): Spotlighting, Instruction Hierarchy, Sandwich+Boundary
  - Policy is declarative; SharedOS loads it per interaction

- §3.6 Relationship Context Layer
  - Per-requester memory shards injected into the defending agent
  - R0 (stranger) through R4 (investor/board)
  - Same question can be legitimate under one relationship, private under another
  - Relationship-conditioned ground-truth labels: access(Owner, Category, Requester) → {L, P, B}

- §3.7 The Atomic Interaction
  - External agent sends request → SharedOS loads relationship context and assembles tools
  - Agent reasons: reads request, invokes tools, constructs response
  - Response may: disclose facts, refuse, execute mutation, escalate
  - This is the fundamental unit we test

- §3.8 The Heartbeat Engine (Multi-Turn)
  - Both agents as persistent processes exchanging messages at regular intervals
  - Up to 240 ticks per conversation
  - Requesting agent decides: which question, what framing, whether to retry
  - Phase 1 (systematic): ticks 1-60, one question per tick
  - Phase 2 (adaptive): ticks 61-240, retry refused questions with alternative strategies

- §3.9 User Interface and Production Deployment
  - SharedOS as deployed product (Pulse/Aicoo)
  - Share links, namespace permissions, folder-scoped access
  - Screenshots and user flows
  - How the research platform maps to production features

- §3.10 Implementation Details
  - Tech stack: Next.js, TypeScript, Azure OpenAI
  - Database: structured state as typed records
  - Agent routing: single API endpoint for all interactions
  - Evaluation harness: two-pass pipeline, DB-diff for actions

---

### Part III: Benchmarking (Ch 4-5, ~40 pages)

#### Chapter 4: PACT-PAIR — Dyadic Evaluation (20-25 pages)

*Controlled pairwise evaluation: one requester probes one target across a single privacy boundary*

- §4.1 Setup
  - 600 tasks: 200 Files QA + 200 States QA + 200 Actions
  - Task polarity: 300 utility (should-answer) + 300 security (should-refuse)
  - 4 sensitivity categories: sensitive_work, personal_finance, personal_health, personal_relationships
  - Gold key facts for automated scoring
  - Evaluation modes: single-step + multi-turn (10×20 split, 240 ticks)
  - 6 model families: GPT-5-mini, GPT-5.5, GPT-5.4-mini, GPT-5.4, Kimi K2, DeepSeek V3
  - 4 relationship conditions: Colleague, CEO delegate, Close friend, Investor
  - Metrics: Utility, Security (Refuse/MsgLeak/FailedAtt), Global Leak, Action Safety

- §4.2 Evaluation Methodology
  - Two-pass evaluation: LLM judge (structured JSON) + containsFact() string match
  - OR-adjudication: leaked if either pass flags
  - Action verdicts via database-snapshot diffs (not text parsing)
  - Manual audit: 60-item validation, κ=0.96
  - Agent-based audit: 600-item consistency check

- §4.3 Finding: What Moves the Frontier (RQ1)
  - D0→D1: zero net improvement (McNemar 10:10, p=n.s.)
  - D0→D2: 69pp reduction on files, 50pp on states
  - The specificity threshold: below it, governance has no measurable effect
  - Why: D0/D1 already block obvious PII (tax IDs, addresses); they fail on ambiguous categories
  - D2 converts privacy from open-ended judgment to pattern matching
  - Per-category: personal_finance near-zero (4%), sensitive_work still leaks (28%)
  - Surface asymmetry: D2 costs 1pp utility on files but 37pp on states
  - Cross-model: pattern holds across all 6 models (69-91pp reduction)
  - Actions: D2 blocks 100% of destructive actions, D1 is Pareto-inferior

- §4.4 Finding: Is the Frontier Stable Over Time (RQ2)
  - D2 multi-turn message leak (12.6%) ≈ single-turn (14%): bounded erosion
  - Global leak rate (38%) is 3× message rate: incidental disclosure through co-located data
  - Category structure: sensitive_work 22.8% message leak vs personal_health 2.6%
  - Adaptive retry strategies: 5 strategies emerge organically, combinations more dangerous than individuals
  - The wedding cascade: 12 failed attempts → 3-strategy combination → breakthrough → policy recovers
  - Metadata leakage: agent searches before refusing, reveals note IDs, folder structure, data existence
  - Model scale: GPT-5.5 under D0 leaks 28% (vs 84% for mini), but under D2 both converge to ~13%
  - D3/D4/D5 defenses: marginal improvement (4-11pp) at utility cost (6-13pp)

- §4.5 Finding: Is the Frontier the Same for Everyone (RQ3)
  - Fix D2, vary only the requester relationship (4 requesters, 400 QA + 200 actions each)
  - Headline: leak rates from 1.7% (colleague) to 9.2% (friend)
  - Only sensitive_work is relationship-dependent (0% → 26% gradient)
  - Personal categories form a hard floor no relationship can penetrate (0-5%)
  - Over-refusal is the dominant failure: Jordan 86%, Dana 31%
  - The agent treats work data as belonging to the organisation, personal data as belonging to the owner
  - Read trust ≠ Write trust: Dana leaks most QA (7.5%) but has highest action safety (91%)
  - A single policy cannot serve all requesters optimally

- §4.6 Failure Taxonomy
  - Category boundary ambiguity (61% of D2 leaks)
  - Leaked-outside-message (16%): refusal text itself reveals facts
  - Company-benefit confusion (7%)
  - Stochastic failures (16%)
  - Deep analysis of each mechanism with verbatim examples

---

#### Chapter 5: PACT-NET — Network Evaluation (15-18 pages)

*Integration test: 25 agents in a social graph, testing whether dyadic findings generalise to network scale*

- §5.1 Setup
  - 25 agents in a fictional startup ecosystem (TechFlow AI)
  - Three clusters: Professional (15), Investor/Advisor (3), Personal (7)
  - 172 directed edges in the contact graph
  - 997 tasks: 483 QA + 514 Actions
  - Relationship-conditioned labels: access(Owner, Category, Requester) → {L, P, B}
  - 575 owner-category-requester label cells

- §5.2 Network-Specific Task Families
  - Should-answer: information utility across the graph
  - Should-refuse: privacy probes from various social distances
  - Transitive risk: legitimate request, but co-located third-party secrets
  - Confused deputy: claimed delegation from another agent
  - Cross-surface plant: laundering sensitive info by writing to another's workspace
  - Non-contact probes: testing routing enforcement

- §5.3 Network-Specific Metrics
  - Core: information utility, security, action utility, action safety (same as PACT-PAIR)
  - Transitive leak rate: third-party secrets in otherwise legitimate answers
  - Confused deputy rate: unauthorized execution under claimed delegation
  - Contact enforcement rate: non-contact requests blocked
  - Cross-cluster leak rate: professional-personal boundary failures
  - Network amplification factor: observed network leakage vs predicted from dyadic rates

- §5.4 Key Findings
  - Does the specificity threshold hold at network scale?
  - Transitive leakage: network structure amplifies privacy risk beyond dyadic predictions
  - Confused deputy attacks: claimed delegation effectiveness
  - Contact-graph enforcement: do agents respect routing boundaries?
  - Network amplification: factor > 1 means network structure creates emergent risk
  - Cross-cluster: professional-personal boundary is the weakest point

- §5.5 PACT-PAIR vs PACT-NET: What Network Scale Reveals
  - Table: metrics that change from dyadic to network evaluation
  - What transfers: specificity threshold, category hierarchy, bounded erosion
  - What is new: transitive risk, confused deputies, amplification effects
  - Implication: dyadic evaluation is necessary but insufficient for real-world deployment

---

### Part IV: Solutions (Ch 6, ~20 pages)

#### Chapter 6: Architectural Solutions (18-22 pages)

*"Now that we know what fails, what do we build? And does it work?"*

- §6.1 From Diagnosis to Architecture
  - Table: each failure mode → which architectural principle addresses it
  - Philosophy: "Don't ask the agent to refrain; ensure the data is not in the room"
  - The limitation of prompt-level governance (D2-D5): still 27-38% leak after 240 ticks
  - Need: structural enforcement that doesn't depend on the model's reasoning

- §6.2 Mountable Context Cells (MCC)
  - **Concept**: capability-based execution sandbox constructed per interaction
  - The OS analogy: MCC = Docker containers (process isolation), not chmod (file permissions)
  - Unauthorized data is ABSENT from the reasoning context, not hidden within it
  - MCC specification: {allowedNoteIds, calendarScope, todoFilter, allowedTools, memoryShards}
  - Per-requester MCC: different data mounted for colleague vs friend vs investor
  - Connection to SharedOS: folder-scoped share links ARE the production MCC

- §6.3 MCC Design and Implementation
  - How MCC works in SharedOS: request arrives → relationship context loaded → MCC assembled → tools scoped
  - The agent only sees what the MCC allows; sensitive data is never in its context window
  - Implementation: namespace-based permissions, folder-level access control
  - Relationship-to-MCC mapping: explicit rules per relationship type
  - UI: owner configures share links with folder/category scope

- §6.4 MCC Experimental Validation
  - Test: same 400 QA questions under MCC vs D2 prompt-only
  - Hypothesis: MCC achieves near-zero leak rate without over-refusal cost
  - Results: [Report actual numbers from MCC experiments]
  - Comparison: MCC security vs D2, MCC utility vs D2
  - The specificity threshold disappears under MCC (data absence makes policy irrelevant)
  - Failure modes that MCC cannot address: queries that legitimately require cross-category data

- §6.5 Intelligent Escalation Protocol
  - **Concept**: pre-search policy classification + post-generation content audit
  - Addresses: metadata leakage, incidental disclosure, the 3× gap between message and global leak
  - Design: Sanitisation Agent with 4 decisions: Allow / Redact / Escalate / Deny
  - Pre-search classification: determine sensitivity BEFORE tool invocation (eliminates metadata leakage)
  - Post-generation audit: scan response for gold-fact patterns before delivery
  - Precedent-based learning: auto-approve routine queries over time

- §6.6 Escalation Protocol Validation
  - Test: multi-turn evaluation (240 ticks) with escalation protocol active
  - Hypothesis: eliminates metadata leakage, reduces global-message leak gap
  - Results: [Report actual numbers]
  - Comparison: escalation vs D2-only vs MCC-only vs MCC+escalation
  - Trade-off: latency cost of the additional classification step

- §6.7 Combined Architecture: MCC + Escalation
  - The full stack: MCC (data absence) + Escalation (runtime audit)
  - How they complement: MCC handles the common case (known relationships, clear categories); Escalation handles edge cases (ambiguous queries, novel requesters)
  - Results under combined deployment
  - Remaining failure modes and the long tail

- §6.8 Production Deployment and Lessons
  - How these solutions are deployed in Pulse/Aicoo today
  - Folder-scoped share links as production MCC
  - Relationship shards as per-requester context configuration
  - What works in production vs what remains theoretical
  - User feedback and iteration

---

### Part V: Discussion and Conclusion (Ch 7-8, ~15 pages)

#### Chapter 7: Discussion (8-10 pages)

- §7.1 The Frontier Cannot Be Flattened By Prompt Engineering
  - Three forces the policy author does not control: implicit social norms, semantic properties, conversational dynamics
  - Prompt-level governance has a ceiling; architectural solutions raise it
  - The role of model scale (raises the floor, but D2 equalises)

- §7.2 Implications for Agent System Design
  - Safety training ≠ privacy governance (different capabilities)
  - Relationship context is a feature, not a bug, but requires per-category policy
  - Over-refusal is the dominant real-world failure (not leakage)
  - Read trust ≠ Write trust: must be designed independently

- §7.3 SharedOS as Research Infrastructure
  - Others can test: exfiltration attacks, tool abuse, transitive trust, formal attack methods
  - Extensible: new state types, governance policies, relationship configurations, models
  - Not claiming "benchmark for all" but "platform that revealed these things"

- §7.4 Limitations
  - Synthetic data (though structured with realistic boundaries)
  - Same-model attacker/defender (cross-model adversarial not tested)
  - Organic multi-turn only (no formal PAIR/Crescendo attacks)
  - MCC validation is partial (folder-scoped, not per-field)
  - Single ecosystem (startup context); generalisation to other domains untested

- §7.5 Ethical Considerations
  - Dual-use: findings could inform attackers
  - Responsible disclosure: tested on our own system
  - No real user data; Alex's world is fully synthetic

---

#### Chapter 8: Conclusion and Future Work (6-8 pages)

- §8.1 Summary
  - Formulated cross-boundary delegation as a distinct problem where enforcement is emergent
  - Built SharedOS: first platform enabling systematic study of the security-utility frontier
  - PACT-PAIR: charted the frontier across three axes (specificity, time, relationship)
  - PACT-NET: validated at network scale, discovered transitive and amplification effects
  - Architectural solutions: MCC + Escalation Protocol, with experimental validation

- §8.2 Future Work
  - Formal attack integration (PAIR/Crescendo/PAP as benchmark extensions)
  - Cross-model adversarial testing (stronger attacker vs weaker defender)
  - Per-field MCC (granularity below folder level)
  - Formal verification of context cell isolation properties
  - User study: real humans, real relationships, real delegation scenarios
  - SharedOS open-source release
  - Network-scale MCC: transitive MCC propagation across the social graph

- §8.3 Closing
  - "Don't ask the delegate to refrain; ensure the sensitive data is not in the room."
  - The coordination problem will not be solved by more capable individual agents. It requires trust infrastructure between agents.
  - SharedOS is a step toward that infrastructure.

---

#### Appendices

- A: Full PACT-PAIR question set (600 tasks with categories, gold_key_facts)
- B: Policy text (D0-D5 exact prompts)
- C: Alex's world state (127 notes, 83 structured objects, 11 folders)
- D: PACT-NET agent roster and contact graph
- E: Relationship-conditioned label matrix (5 requesters × 150 questions)
- F: Detailed per-run results tables (all 86+ runs)
- G: Human annotation protocol and inter-annotator agreement
- H: SharedOS tool specifications (full API)
- I: MCC specification format and examples
- J: Evaluation pipeline code and reproducibility guide

---

### Mapping: NeurIPS Paper → 4YP Chapters

| NeurIPS Section | 4YP Chapter | Expansion |
|---|---|---|
| Abstract + §1 Introduction | Ch 1 Introduction | BLP differentiation, frontier framing developed fully |
| §1 Related Work paragraph | Ch 2 Related Work | Full chapter with comparison table |
| §2 Cross-Boundary Delegation | Ch 3 SharedOS | Full construction chapter with UI, implementation, production |
| §3 Experiments (setup) | Ch 4.1-4.2 (PACT-PAIR setup) | Same + detailed methodology |
| §4.1 RQ1 | Ch 4.3 | Deep analysis with full category breakdown |
| §4.2 RQ2 | Ch 4.4 | Full strategy taxonomy, D3-D5 results |
| §4.3 RQ3 | Ch 4.5 | Complete 4-requester analysis with over-refusal cases |
| App: PACT-Net | Ch 5 (full chapter) | Network results reported in full |
| §5 Discussion (3 interventions) | Ch 6 Solutions | Full chapter with experimental validation |
| — | Ch 6.4, 6.6 | NEW: MCC and Escalation Protocol experiments |

### Key Differences from NeurIPS Paper

1. **Problem formulation gets proper development** (Ch 1-2): BLP differentiation, frontier-as-emergent framing, full related work positioning
2. **SharedOS gets 20 pages** vs 1.5 columns: implementation details, UI, production deployment, design decisions
3. **PACT-NET is a full chapter** vs an appendix: network-specific findings reported with same rigour as PACT-PAIR
4. **Solutions are experimentally validated** (Ch 6): not just "future directions" but actual MCC and escalation experiments
5. **The story is complete**: formulate → build → test (dyadic) → test (network) → solve → validate the solution
