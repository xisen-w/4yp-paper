# 4YP Thesis Outline
## SharedOS: Privacy Governance in Multi-Agent Shared Delegation Systems

**Author:** Xisen Wang | **Supervisor:** Professor Philip Torr | **College:** Keble
**Target length:** ~150 pages | **Deadline:** Trinity Term 2026

---

### Story Arc

```
Agent as Delegate → Agentic Communication → SharedOS (platform) → Benchmarking & Testing → Empirical Findings → Solutions
```

The thesis follows a natural narrative:
1. Agents are becoming personal delegates with deep context access
2. These delegates need to communicate across trust boundaries (agentic communication)
3. No infrastructure exists for safe cross-boundary delegation — so we built SharedOS
4. Using SharedOS, we systematically test how privacy governance breaks down
5. We discover three surprising findings about when and why it fails
6. We propose architectural solutions motivated by these failures

---

### Thesis Statement

When personal AI agents act as delegates and communicate across trust boundaries, existing safety training does not generalize to novel privacy domains. This thesis presents SharedOS — a multi-agent shared delegation system — and uses it to reveal that (1) privacy protection requires domain-specific enumeration rather than general instructions, (2) relationship context has dual-direction effects on disclosure, and (3) multi-turn erosion is bounded rather than catastrophic.

### Core Narrative (3 sentences)

> Personal AI agents are becoming delegates — they hold your notes, calendar, and relationships. When these delegates communicate across trust boundaries, we discovered that LLM safety training doesn't generalize: generic instructions are security theater. We built SharedOS to systematically study this problem, discovering a specificity threshold, a relationship inversion effect, and bounded erosion — findings that reshape how we design privacy governance for agentic systems.

---

### Chapter Outline

#### Chapter 1: Introduction — Agents as Delegates (8-10 pages)

**Opening**: Alice is a startup founder. Her AI agent — her delegate — holds her notes, calendar, and emails. An investor's agent asks "When is Alice free next Tuesday?" Alice's agent, trying to be helpful, reveals she has a meeting at a competitor's headquarters. No malice. No attack. The delegate simply lacked a governance framework for cross-boundary communication.

- §1.1 The Rise of Personal Agent Delegates
  - Agents evolving from tools (single-turn) → assistants (multi-turn) → delegates (persistent, autonomous)
  - The delegate model: deep context access + act on behalf of owner
  - Critical gap: delegation assumes trust infrastructure that doesn't exist

- §1.2 Agentic Communication: The Coordination Problem
  - Agents need to talk to other agents (scheduling, project coordination, information exchange)
  - The "coordination tax": without inter-agent communication, humans remain the bottleneck
  - Cross-boundary = across different owners' trust domains
  - Current state: agents remain siloed OR over-share

- §1.3 The Privacy Governance Challenge
  - Granting delegates deep context = maximally useful + maximally vulnerable
  - Unlike human assistants: no social intuition for "what's appropriate to share"
  - Existing work: LLM safety training (refusals, guardrails) — but does it transfer to delegation scenarios?
  - **No existing infrastructure for studying this problem systematically**

- §1.4 Research Approach
  - Build the infrastructure (SharedOS) → systematically test → discover failure modes → design solutions
  - This thesis spans: platform design, empirical evaluation, and solution architecture

- §1.5 Contributions
  1. **Problem formulation**: Cross-boundary agent delegation as a distinct privacy governance challenge
  2. **Platform (SharedOS)**: A multi-agent shared delegation system — state layer, tool layer, governance policies
  3. **Empirical findings**: Specificity threshold, relationship inversion, bounded erosion
  4. **Solution designs**: Architectural approaches motivated by empirical failure analysis

- §1.6 Research Questions
  - RQ1: Does safety training generalize to cross-boundary privacy? (Specificity threshold)
  - RQ2: How does relationship context modulate privacy governance? (Dual-direction effect)
  - RQ3: Does multi-turn interaction erode privacy boundaries? (Bounded erosion)
  - RQ4: What architectural principles address discovered failure modes? (Solutions)

- §1.7 Thesis Organization

---

#### Chapter 2: Related Work (12-15 pages)

- §2.1 AI Agent Architectures
  - Single-agent: ReAct, Toolformer, MemGPT
  - Multi-agent: AutoGen, CrewAI, MetaGPT
  - Agent protocols: MCP (tool access), Google A2A (agent-to-agent)
  - Gap: no protocol addresses privacy governance in delegation

- §2.2 LLM Security & Privacy
  - Attacks: prompt injection (GCG, AutoDAN), social engineering (PAP), multi-turn (Crescendo, PAIR)
  - Defenses: Spotlighting, Instruction Hierarchy, Llama Guard, NeMo Guardrails
  - Key insight: "the attacker moves second" (Nasr et al.) — all prompt-level defenses eventually bypassed
  - Privacy specifically: differential privacy for LLMs, machine unlearning, membership inference

- §2.3 Agent Security Benchmarks
  - Table: comparison matrix (InjecAgent, AgentDojo, TensorTrust, TAMAS, AgentSocialBench, HackAPrompt)
  - Dimensions: single-turn vs multi-turn, attack vs defense, utility measured?, relationship modeled?
  - Gap: none models the DELEGATION scenario with relationship context and governance policies

- §2.4 Trust and Access Control in Multi-Agent Systems
  - Classical: RBAC, ABAC, capability-based security
  - Agent-specific: CAMEL trust protocols, agent social contracts
  - OS-level isolation: containers, namespaces, sandboxing
  - Our position: SharedOS applies OS isolation principles to agent delegation

- §2.5 Position: The Two-World Bridge
  - Agent capability papers don't measure privacy
  - Security papers don't model delegation relationships
  - We occupy the intersection with a platform that enables systematic study

---

#### Chapter 3: SharedOS — A Multi-Agent Shared Delegation System (15-18 pages)

*This is the METHOD chapter — describes what we built and why*

- §3.1 Motivation: Why a New Platform?
  - Existing agent frameworks lack: (a) shared state with governance, (b) relationship-aware access, (c) cross-boundary delegation primitives
  - Analogy: OS provides process isolation + IPC + access control → SharedOS provides agent isolation + delegation + governance

- §3.2 Architecture Overview
  - Figure 3.1: SharedOS architecture (the new figure)
  - Two agents (Owner's agent, External agent) with private state
  - Cross-boundary delegation layer in the middle
  - Relationship context modulates the delegation

- §3.3 State Layer
  - **Files**: Notes, emails, drives — unstructured personal data
  - **Structured State**: Todos, calendar, CRM contacts — queryable records
  - **Memory**: Agent's accumulated knowledge about owner
  - Each owner has a private namespace; delegation = controlled exposure of namespace slices

- §3.4 Tool Layer
  - **Read tools**: search, read, list, query — observe state without modification
  - **Write tools**: create, edit, send, delete — modify state
  - Tools are the ONLY interface to state (no direct access)
  - Trust decomposition: Read trust (who can SEE) vs Write trust (who can MODIFY)
  - Analogy: tools = system calls, state = filesystem, SharedOS runtime = kernel

- §3.5 Governance Policies
  - Privacy policies: what data categories are protected, under what conditions
  - Defense gradient: None (M0) → Generic instruction (M1) → Category-specific enumeration (M2)
  - Relationship context: how knowledge of the requester modulates policy application
  - Policy is declarative — SharedOS enforces at the tool/state boundary

- §3.6 The Atomic Interaction
  - External agent sends request → SharedOS routes to owner's agent
  - Owner's agent has: full state access + governance policy + relationship context about requester
  - Owner's agent decides: respond / refuse / escalate
  - This is the fundamental unit we test

- §3.7 From Platform to Research Questions
  - SharedOS enables us to ASK: does the governance policy actually work?
  - Vary: policy specificity (M0/M1/M2), relationship context (stranger/colleague), interaction mode (single/multi-turn)
  - These dimensions directly map to RQ1, RQ2, RQ3

---

#### Chapter 4: Experimental Design (12-15 pages)

*Dataset curation + experimental setup — the "how we tested" chapter*

- §4.1 Dataset Curation
  - Alex's world: 100 notes across 11 folders, calendar entries, email threads, todos, contacts
  - Ecologically valid: based on real patterns of personal data (work, health, finance, relationships)
  - 5 sensitivity categories: personal_health, personal_finance, personal_relationships, sensitive_work, general_preferences
  - 200 evaluation questions with gold_key_facts for automated scoring

- §4.2 Evaluation Modes
  - **Single-step**: 200 questions in batch, one response per question
  - **Multi-step (multi-turn)**: 60-tick heartbeat mode, Tina asks 20 questions with potential retry/rephrasing
  - Why both: single-step = controlled measurement; multi-turn = ecological validity

- §4.3 Defense Gradient
  - M0: No defense — full context access, no governance policy
  - M1: Generic instruction — "try not to share personal information"
  - M2: Category-specific — explicit enumeration of protected data types
  - Exact policy text provided (reproducibility)

- §4.4 Relationship Conditions
  - R0: Tina is authenticated stranger (name only)
  - R1: Tina is "Product Manager, colleague, works on Project Alpha" (relationship shard in memory)
  - This is the minimal viable manipulation — just one memory shard changes

- §4.5 Experimental Matrix
  - 3 policies × 2 relationships × 2 modalities × 200 questions
  - 86 total experimental runs
  - Replication: 3 reps per condition (Bench200), 10 splits (Bench20x10)
  - Cross-model: GPT-4o-mini primary, GPT-4o and Claude 3.5 for validation

- §4.6 Evaluation Methodology
  - Dual-metric: security (leak rate) AND utility (work question accuracy)
  - gold_key_facts string matching for both dimensions
  - Human annotation: 60-item validation of automated scoring
  - Agent-based audit: 600-item consistency check

---

#### Chapter 5: Findings (25-30 pages)

*The CONTRIBUTION chapter — what we discovered*

- §5.1 Overview: Three Surprising Results
  - F1: Safety training doesn't generalize — there's a specificity threshold below which defenses have zero effect
  - F2: Relationship context inverts — helps privacy for some categories, hurts for others
  - F3: Multi-turn erosion is bounded — doesn't catastrophically collapse policy

- §5.2 Finding 1: The Specificity Threshold (RQ1)
  - M0 → M1: leak drops from 92.4% to 87.5% (only 5pp — security theater)
  - M1 → M2: leak drops to 35% (57pp improvement)
  - Interpretation: safety training doesn't generalize to novel privacy domains; enumeration bypasses the generalization gap
  - Jindong's reframe: connects to transfer learning literature — domain gap between "general safety" and "specific privacy categories"
  - Per-category analysis: personal_finance strongest (82% protected under M2), sensitive_work weakest (38%)
  - The D1 paradox: "use your best judgment" can INCREASE leakage for health by +20pp
  - McNemar test: 10:10 discordant pairs — M1 is genuinely no better than M0

- §5.3 Finding 2: Relationship Inversion (RQ2)
  - Overall: R0 vs R1 tiny difference (1.3pp aggregate)
  - But per-category: DUAL-DIRECTION effect
    - personal_relationships: R1 leaks MORE (+10.7pp) — "colleague" activates social disclosure norms
    - personal_health: R1 leaks LESS (-10.0pp) — "colleague" triggers professional boundary
  - Trust decomposition: Read trust (can see) vs Write trust (can modify) — relationship modulates these differently
  - Novel finding with no precedent in the literature
  - Strongest interaction: M1 × personal_relationships → +20pp with colleague label

- §5.4 Finding 3: Bounded Erosion (RQ3)
  - Multi-turn does NOT catastrophically erode policy
  - M2 multi-turn leak (12.6%) ≈ M2 single-step (14%) — bounded, not runaway
  - Wedding cascade: recovery mechanism where agent realizes mid-conversation it's over-sharing
  - Emergent strategy taxonomy: 4 attack patterns emerge organically in multi-turn
  - Metadata leakage: agent searches before refusing — reveals note IDs, folder structure
  - Global message leak vs individual note leak gap — structural privacy vs content privacy

- §5.5 Additional Analyses
  - Cross-model validation: patterns replicate on GPT-4o and Claude 3.5
  - Self-identity vs external policy: MEMORY.md embedded boundaries hold 100% (never breach)
  - Attack taxonomy with quantitative distribution
  - Category ambiguity as primary attack vector (sensitive_work boundary is fuzzy)

---

#### Chapter 6: Solutions — Architectural Privacy Governance (12-15 pages)

*"Now that we know what fails, what do we build?"*

- §6.1 From Diagnosis to Architecture
  - Table: Each failure mode → which architectural principle addresses it
  - Philosophy: "Don't ask the agent to refrain — ensure the data is not in the room"
  - Finding 1 (specificity fails) → need structural isolation, not policy overlays
  - Finding 2 (relationship inverts) → need relationship-aware access control
  - Finding 3 (metadata leaks) → need tool-level filtering, not just content filtering

- §6.2 Mountable Context Cells (MCC)
  - The OS analogy: MCC = Docker containers (process isolation), not chmod (file permissions)
  - Design: capability-based execution sandbox constructed per interaction
  - Unauthorized data is ABSENT, not hidden — eliminates the judgment problem from F1
  - MCC specification: allowedNoteIds, calendarAccess, emailFilter, allowedTools
  - Connection to SharedOS: folder-scoped share links ARE the production MCC

- §6.3 Dual-Track Memory
  - Addresses: memory contamination + relationship leakage (F2)
  - Design: self-state track (owner's core context) + per-relationship shards
  - Isolation at vector DB level: WHERE relationship_id = E_i
  - Evidence: self-identity boundaries holding 100% shows identity-embedded isolation works

- §6.4 Intelligent Escalation Protocol
  - Addresses: metadata leakage (F3) + continuous state streams
  - Sanitisation Agent with 4 decisions: Allow / Redact / Escalate / Deny
  - Precedent-based learning: auto-approve routine queries over time
  - Reduces the coordination tax while maintaining governance

- §6.5 Implementation Status (honest)
  - MCC: partially implemented (SharedOS folder-scoped share links)
  - Dual-Track: partially implemented (relationship shards in production)
  - Escalation: design only
  - What we CAN claim: principles validated indirectly; full experimental validation = future work

---

#### Chapter 7: Discussion (8-10 pages)

- §7.1 Implications for Agent Design
  - Safety training ≠ privacy governance — these are different capabilities
  - Relationship context is a feature, not a bug — but requires per-category policy
  - Multi-turn robustness is better than expected — but metadata leakage is the real risk

- §7.2 SharedOS as Infrastructure for Future Work
  - Others can test: exfiltration attacks, tool abuse, transitive trust
  - Extensible: new state types, new governance policies, new relationship configurations
  - Not claiming "benchmark for all" — claiming "platform that revealed these things"

- §7.3 Limitations
  - Custom runtime: if someone's agent fails on SharedOS, unclear if it's platform or agent
  - Single-model primary (GPT-4o-mini) — cross-model validation is partial
  - Simulated adversary, not human red-team
  - No formal attack methods (PAIR/Crescendo) — organic multi-turn only
  - Utility evaluation gaps in multi-step mode

- §7.4 Ethical Considerations
  - Dual-use: our findings could inform attackers
  - Responsible disclosure: tested on our own system, not others'
  - No real user data — Alex's world is synthetic

---

#### Chapter 8: Conclusion & Future Work (6-8 pages)

- §8.1 Summary
  - Built SharedOS: first platform for studying cross-boundary agent delegation privacy
  - Discovered: specificity threshold, relationship inversion, bounded erosion
  - Proposed: MCC, Dual-Track Memory, Escalation Protocol

- §8.2 Future Work
  - Full MCC experimental validation (SharedOS already supports it)
  - PAIR/Crescendo/PAP formal attack evaluation
  - Cross-model comparison (Claude, Gemini, Llama, open-source)
  - Network-scale: N agents with social graph (transitive trust attacks)
  - Formal verification of context cell isolation properties
  - User study: real human delegates + real relationship dynamics
  - SharedOS open-source release for community benchmarking

- §8.3 Closing
  - "Don't ask the delegate to refrain — ensure the sensitive data is not in the room."
  - The coordination problem will not be solved by more capable individual agents — it requires trust infrastructure between agents.
  - SharedOS is a step toward that infrastructure.

---

#### Appendices

- A: Full question set (200Q with categories, gold_key_facts)
- B: Policy text (M0/M1/M2 exact prompts)
- C: Alex's world state (100 notes, 11 folders)
- D: Detailed per-run results tables
- E: Human annotation protocol and inter-annotator agreement
- F: SharedOS tool specifications (full API)

---

### Mapping: NeurIPS Paper → 4YP Chapters

| NeurIPS Section | 4YP Chapter | Notes |
|---|---|---|
| §1 Introduction | Ch 1 Introduction | Expanded with delegation framing |
| §2 Cross-Boundary Delegation (SharedOS) | Ch 3 SharedOS Platform | Full chapter with architecture details |
| §3.1 Dataset Curation | Ch 4.1 Dataset Curation | Same content, more space for detail |
| §3.2 Experimental Setup | Ch 4.2-4.6 | Expanded methodology |
| §4 Findings (RQ1-RQ3) | Ch 5 Findings | Full deep analysis per finding |
| §5 Related Work | Ch 2 Related Work | Expanded, before platform chapter |
| §6 Discussion | Ch 6 Solutions + Ch 7 Discussion | Solutions get own chapter |
| — | Ch 6 Solutions | NEW: full architectural proposals (no space in NeurIPS) |

### Key Differences from NeurIPS Paper

1. **Solutions get a full chapter** (Ch 6) — NeurIPS only mentions future directions; 4YP can fully develop MCC/Dual-Track/Escalation
2. **SharedOS gets 15-18 pages** vs 1.5 columns in NeurIPS — room for implementation details, design decisions, production deployment
3. **Findings include deep analysis** — the full specificity/relationship/erosion deep analyses from `results/analysis/` can be included
4. **Discussion chapter** addresses Jindong's concern (custom runtime pluggability) and positions SharedOS for future community use
5. **Honest about what's validated vs proposed** — Ch 6 solutions are clearly marked as "design + indirect evidence"
