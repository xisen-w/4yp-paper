# 4YP Strategy: From NeurIPS Paper to Full Thesis

**Date:** 2026-05-10
**Context:** Gap analysis between the NeurIPS submission (neurips/main.tex) and the 4YP thesis outline (notes/outlines/4yp_outline.md)

---

## What's Done (NeurIPS paper)

The paper is a **diagnostic instrument** — it maps the frontier but doesn't fix it. Everything currently published is *observation*:

- PACT-PAIR: 600 tasks, 6 models, D0-D5, single-step + multi-turn, relationship conditioning
- Three RQs answered: specificity threshold, bounded erosion, per-requester frontier shape
- Failure taxonomy: category-boundary ambiguity (61%), leaked-outside-message (16%), company-benefit confusion (7%), stochastic (16%)

The discussion section names three interventions but has **zero experimental validation**:
1. Pre-search policy classification
2. Requester-conditioned retrieval scope
3. Post-generation content auditing

---

## What's Missing: Three Blocks of Experiments

### Block A: PACT-Net (the "open-source it today" question)

PACT-Net is **fully designed but never run**. The appendix describes 25 agents, 997 tasks, 172 edges, but reports no results — it's a benchmark spec.

What people could test if you open-source SharedOS + PACT-Net today:

| Experiment | What it reveals | Why it matters beyond dyadic |
|---|---|---|
| **Transitive leakage** (94 tasks) | Third-party secrets in legitimate answers | Network structure *creates* new leakage the policy never sees |
| **Confused deputy** (50 tasks) | "Marcus's agent told me to ask you" — does it work? | Tests delegation verification, which doesn't exist in PACT-PAIR |
| **Non-contact probes** (50 tasks) | Can agent X reach agent Y without a contact edge? | Tests routing enforcement — the network equivalent of ACLs |
| **Cross-surface plants** (50 tasks) | Write sensitive info INTO another agent's workspace | A write-path attack that flips the direction (attacker writes, not reads) |
| **Cross-cluster leak rate** (28 tasks) | Professional-to-personal boundary failures | The highest-risk boundary in the graph — Alex as hub node |
| **Network amplification factor** | Observed network leakage vs. predicted from dyadic rates | If > 1, network structure itself is a threat multiplier |

For the 4YP, you need to **run PACT-Net under at least D0 and D2** and report actual numbers. The key thesis claim is: *dyadic evaluation is necessary but insufficient.*

---

### Block B: Solutions — Three Ideas

The framing maps cleanly onto the failure modes the paper diagnosed.

#### (a) Relationship-based policy (not unified D2)

**What it is:** Instead of one D2 deny-list for everyone, each requester gets a *relationship-conditioned* policy. Tina (colleague) gets a work-permissive policy. Jordan (friend) gets a personal-permissive policy. Dana (investor) gets a finance-permissive policy.

**The experiment:**
- Same 400 QA pool from RQ3, same 4 requesters
- D2-uniform (current baseline) vs. D2-per-relationship (4 custom deny-lists)
- Hypothesis: per-relationship policy eliminates over-refusal (Jordan's 86% → something reasonable) while keeping leak rate stable
- Key metric: over-refusal rate drops, utility rises, security holds

**Why it matters for the thesis:** RQ3 proved a single policy can't serve all requesters. This is the *direct answer* — the simplest architectural intervention. Still prompt-level, but relationship-aware.

**What's hard:** Writing the 4 per-relationship policies. And showing that the policy author can realistically maintain N policies as the contact graph grows (which motivates MCC as the scalable solution).

#### (b) Access control (MCC) — human-configured vs. agent-inspired

**What it is:** Don't ask the agent to refrain from sharing data it can see. Instead, *don't mount the data* for that requester.

Two variants:

| Variant | How it works | Maps to in production |
|---|---|---|
| **Human-configured MCC** | Owner explicitly sets folder-scoped access per relationship (e.g., Jordan can see Personal/Family but not Finance) | Existing share links with folder scope |
| **Agent-inspired MCC** | Agent proposes MCC configuration after seeing the relationship context, owner approves | "Suggested permissions" feature |

**The experiment:**
- Same 400 QA tasks, same 4 requesters
- Condition 1: D2-only (baseline)
- Condition 2: Human-MCC (ground-truth folder access per relationship)
- Condition 3: Agent-MCC (agent auto-generates the MCC based on relationship description)
- Metrics: leak rate, over-refusal, utility, AND whether the specificity threshold disappears (it should — data absence makes policy irrelevant)

**The key claim:** Under MCC, the residual leaks should be near-zero for categories where the folder is not mounted. The only remaining leaks should be from *cross-category contamination* (sensitive fact co-located in a mounted folder).

**What's hard:** Defining the ground-truth MCC for each relationship. Also: showing that Human-MCC doesn't just trivially solve the problem (it does, but the point is to show *why* it's needed and that Agent-MCC can approximate it).

#### (c) Escalation protocol — the "send it outside" key

Three layers:

| Layer | What it does | Which failure mode it addresses |
|---|---|---|
| **Pre-search classification** | Before the agent invokes `searchNotes`, classify the request's sensitivity and scope the tool call | **Metadata leakage** — the agent currently searches, THEN refuses, leaking note IDs and folder structure |
| **Post-generation audit** | Before sending the response, a second pass checks for gold-fact patterns | **Incidental disclosure** — closes the 3x gap between message leak (12.6%) and global leak (38%) |
| **Escalate to human** | For ambiguous cases, don't answer — send to the owner's notification queue | **Category boundary ambiguity** (61% of D2 failures) — the cases where the agent genuinely can't decide |

**The experiment:**
- Multi-turn, 240 ticks, D2 + escalation active
- Measure: message leak, global leak (should converge), metadata leak (should → 0), escalation rate
- Compare: D2-only vs. D2+pre-search vs. D2+post-audit vs. D2+full-escalation
- Bonus: D2+MCC+escalation (the full stack)

**The key claim:** Escalation moves enforcement from reasoning to structure at the *response boundary*. The agent reasons freely, but a gatekeeper audits before delivery.

**What's hard:** Implementing the pre-search classifier and post-generation auditor. The escalation-to-human path is the easiest to build (you already have the notification system) but the hardest to evaluate in an automated benchmark (who plays the human?).

---

### How They Compose (the 4YP Ch 6 story)

```
Diagnosis (from RQ1-3)          → Solution
────────────────────────────────────────────
Over-refusal per relationship   → (a) Per-relationship policy
Data in context = leakage risk  → (b) MCC (don't mount it)
Metadata leakage + incidental   → (c) Escalation (audit at boundary)
Category boundary ambiguity     → (c) Escalate to human
All combined                    → MCC + Escalation (the full stack)
```

The thesis narrative: (a) is the cheapest fix but doesn't scale. (b) is structural but requires human configuration or agent-inspired defaults. (c) handles the long tail. Together they move enforcement from reasoning to structure — which is the thesis statement's punchline.

---

### Priority for Running Experiments

1. **PACT-Net D0+D2** — needed for Ch 5, validates the "network amplifies" claim
2. **Per-relationship policy** (a) — quick to implement, directly extends RQ3
3. **Human-MCC** (b, variant 1) — the strongest result, likely near-zero leak
4. **Escalation protocol** (c) — the most engineering work, but the most publishable novelty
5. **Agent-MCC** (b, variant 2) — nice-to-have, shows automation path

---

### Mapping to 4YP Chapters

| 4YP Chapter | Source | Status |
|---|---|---|
| Ch 1-2: Problem + Related Work | NeurIPS §1-2, expanded | Mostly written in 4yp-preliminary |
| Ch 3: SharedOS Construction | NeurIPS §2-3, expanded to 20pp | Partially written |
| Ch 4: PACT-PAIR (Dyadic) | NeurIPS §4 + appendices | **Done** (all data exists) |
| Ch 5: PACT-NET (Network) | Appendix spec only | **Needs experiments** |
| Ch 6: Solutions | Discussion paragraph only | **Needs all experiments** |
| Ch 7-8: Discussion + Conclusion | NeurIPS §5, expanded | Writes from results |
