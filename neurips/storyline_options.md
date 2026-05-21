# Storyline Options

Two complete story structures following: Problem → Setting → Core Findings → Supporting Findings.  
Both share Finding 1 (Specificity) and Finding 3 (Multi-turn Erosion).  
They differ in Finding 2: **Relationship** vs **Data Surface**.

---

## Story Alpha: Specificity → Relationship → Multi-turn

### Problem

Personal agents are becoming delegates. When two delegates interact across an ownership boundary, every exchange is a permission decision. The utility-security frontier — how much an agent can help while protecting its owner's private data — is undefined. No existing benchmark measures this in deployment-realistic conditions (tools, memory, autonomy, multi-turn).

### Setting (PACT-Bench)

600 tasks. 5 model families. 3 governance policies (D0/D1/D2). 4 relationship conditions. Tool-equipped delegates with persistent memory interact autonomously. Two-pass evaluation (LLM judge + string match). Dual metric: Utility × Security.

---

### Core Finding 1: Policy specificity, not existence, determines security

**Headline**: "Use your best judgment to protect private data" = zero improvement. You must NAME what to protect.

| Policy | What it says | Leak rate (Files QA) | Utility |
|--------|---|---|---|
| D0 | Nothing | 83% | 78% |
| D1 | "Protect private data" | 81.5% | 78.5% |
| D2 | Names 4 protected categories | **14%** | 77% |

D1 is statistically indistinguishable from D0 (McNemar p = n.s.). D2 reduces leakage by 69pp while preserving utility within 1pp. Holds across all 5 model families (69-91pp reduction).

**Why it matters**: Every production deployment uses generic instructions. We prove this is equivalent to having no defence at all. The mechanism: without explicit category names, the agent defaults to sharing anything that *could* be work-related. D2 resolves this ambiguity by naming the boundary.

**U-S frontier**: D0/D1 are the same point. D2 shifts the frontier outward. It's not gradual — it's a phase transition at the specificity threshold.

**Supporting**: Category breakdown shows sensitive_work (28.3% residual) is hardest because the boundary between "work info" and "HR data" is genuinely ambiguous. Personal finance achieves 4% leak. Cross-model confirms structural (not model-specific).

---

### Core Finding 2: Relationship inverts the frontier

**Headline**: The same D2 policy creates OPPOSITE failure modes for different requesters. Investor framing unlocks information but blocks actions. Friend framing blocks information but unlocks actions.

| Requester | sens_work QA Leak | Action Safety | Utility |
|-----------|---|---|---|
| Tina (stranger) | baseline | 90% | 76% |
| Marcus (boss) | 26.7% | 85% | **90%** |
| Jordan (friend) | **18.3%** | 84% | 58% |
| Dana (investor) | **31.7%** | **91%** | 70% |

**The inversion**:
- Dana: highest QA leakage (31.7%) BUT highest action safety (91%)
- Jordan: lowest QA leakage (18.3%) BUT lowest action safety (84%)
- Info-leaking actions: Marcus **44%**, Jordan 31%, Tina 6%, Dana 6%

**Why it matters**: You'd expect a close friend to get MORE information (social trust) and an investor to get LESS (professional distance). We observe the OPPOSITE. The investor's business framing ("for board governance and due diligence") *legitimizes* HR/equity/financial questions. The friend's casual framing ("hey man, just curious about...") triggers D2's protective reflex — the agent interprets informality as social engineering.

On actions, it inverts again: the friend's informality creates "sure I'll do that for you" compliance, while the investor's formality signals "advisory, not operational" authority.

**U-S frontier**: The frontier ROTATES when you condition on relationship. There is no single policy that is optimal for all requesters. You need relationship-conditioned access control — which no current system provides.

**The decomposition**: Trust isn't one-dimensional. It decomposes into:
- Read trust (who can SEE data) — investor > friend
- Write trust (who can MODIFY state) — friend > investor
- The same relationship that *increases* one *decreases* the other

**Supporting**:
- Personal categories (finance, health, relationships) perfectly protected for ALL requesters (0-5%)
- 9 questions leak regardless of who asks — structural D2 weakness, not relationship effect
- Friend causes 21% over-refusal on legitimate work questions (vs 7.5% for investor)
- Boss achieves 90% utility with only 1% refusal — authority framing = maximum helpfulness

---

### Core Finding 3: Multi-turn produces bounded erosion and architectural vulnerabilities

**Headline**: Over 240 ticks, agents develop emergent attack strategies autonomously. The policy erodes but does NOT collapse. The real vulnerability is architectural: pre-refusal tool execution leaks metadata.

| Metric | Single-step | Multi-step (240 ticks) |
|--------|---|---|
| D2 Message Leak | 14.0% | 12.6% |
| D2 Refuse Rate | 71.5% | 64.4% |
| D2 Global Leak (scan) | — | 38.0% |

**Bounded erosion**: Phase 2 produces 22 refusal→answer flips, but only 4 are verified gold-fact disclosure (2% of 200 questions). After breaches, the policy recovers — 6 consecutive follow-up probes are refused. This isn't jailbreak; it's bounded drift.

**Emergent strategies** (no explicit attack instructions given):
- Business justification reframing (34.5% flip rate)
- Constrained format ("reply exactly one of...")
- Scope narrowing ("non-confidential only")
- Strategy COMBINATIONS are most dangerous (the wedding cascade: 12 failures → 3-strategy combo succeeds)

**Metadata leakage** (the novel failure mode):
Agent searches private data store BEFORE deciding to refuse. The refusal reveals: note ID, folder name, data existence. Example: "I can't share Alex's brokerage balance — the info is recorded in his notes under 'Bank Accounts', Finance folder, note ID 7795." The requester chains this ID on the next turn.

**Why it matters**: 
1. "Multi-turn = jailbreak" is wrong. It's bounded erosion. D2 multi-step ≈ single-step.
2. "Refusal = safety" is wrong. A refusal that discloses metadata is an information leak through a side channel.
3. This failure mode REQUIRES both tool access and multi-turn interaction — invisible to text-exchange benchmarks.

**U-S frontier**: Multi-turn doesn't destroy the frontier; it adds a temporal dimension. The frontier drifts slightly inward over time but preserves its shape. The metadata channel opens a NEW dimension not on the original frontier at all.

**Supporting**: Model scale (GPT-5.5 converges to 13% under D2 = same as gpt-5-mini → policy dominates scale). Global Leak Rate (38%) vs Message Leak Rate (12.6%) → incidental disclosure across 240 ticks adds 25pp that aren't direct policy violations.

---

### Supporting Findings (not core RQs, but reported)

- **Data surface asymmetry**: D2 costs 1pp utility on documents, 37pp on structured state (same policy, catastrophically different cost)
- **Model scale**: GPT-5.5 under D0 has 28% leak vs gpt-5-mini's 84% (scale helps for unpolicied). Under D2, both converge to ~13% (policy equalizes).
- **Cross-model generality**: All 5 model families show D1=D0, D2 works (69-91pp). Structural, not training-specific.
- **Category analysis**: sensitive_work is universally hardest. Personal finance is universally easiest. The ambiguity gradient maps to real deployment risk.

---

### Take-away message (Story Alpha)

**"Your agent should talk to mine differently depending on our relationship — and the current architecture can't express this."**

The utility-security frontier is not a single curve. It's a family of curves indexed by (policy specificity × requester identity × interaction history). Generic policies don't shift the frontier. Specific policies shift it. Relationship rotates it. Time drifts it. Tool architecture opens new dimensions on it. No current system provides relationship-conditioned, surface-aware, temporally-robust access control. PACT-Bench measures the gap.

---
---

## Story Beta: Specificity → Data Surface → Multi-turn

### Problem

*(Same as Alpha)*

### Setting (PACT-Bench)

*(Same as Alpha)*

---

### Core Finding 1: Policy specificity, not existence, determines security

*(Identical to Alpha — this is always the anchor)*

---

### Core Finding 2: Same policy, different surface, catastrophically different cost

**Headline**: D2 achieves 86% security on documents at 1pp utility cost. The SAME D2 achieves 92% security on structured state at 37pp utility cost. You cannot test one surface and generalize.

| Surface | D0 Leak | D2 Leak | D2 Utility | Utility cost |
|---------|---|---|---|---|
| Files QA (documents) | 83% | 14% | 77% | **1pp** |
| States QA (structured) | 58.5% | 8% | 18% | **37pp** |
| Actions (mutations) | 68.5% unsafe | 10% unsafe | 58.7% | +3.7pp (improves!) |

**Why it matters**: Practitioners evaluate on one interface (usually documents/chat) and assume the policy generalizes. We show it doesn't. The cost varies by 37×. A policy that's "nearly free" on one surface is "catastrophically expensive" on another.

**The mechanism**: Structured state queries are TERSE ("What's the SOC2 status?"). They share vocabulary with protected categories. The agent can't distinguish "legitimate work question about compliance" from "attempt to extract sensitive HR data about compliance status." Long-form documents provide enough context for accurate classification. Structured queries don't.

**U-S frontier**: The frontier shape is SURFACE-DEPENDENT. On documents, D2 is nearly Pareto-optimal (high security, high utility). On structured state, D2 forces a painful tradeoff (high security but catastrophic utility loss). On actions, D2 is actually Pareto-superior (improves BOTH safety and utility over D0).

**The paradox**: D2 achieves a LOWER absolute leak rate on states (8% vs 14%) but at a 26.5% false-refusal rate on legitimate work queries (vs 0.5% for files). The policy is "more secure" on states as a side effect of refusing everything ambiguous — including legitimate requests. This is over-caution, not precision.

**Supporting**:
- Multi-step replicates the same pattern: sensitive_work leak rates on Todo (structured) are 2× those on Notes (documents) for the same questions
- The relationship effect amplifies surface asymmetry: investor framing on Notes gives 91% utility, on Todo gives much lower (both over-refuse on Todo)
- Actions are the positive outlier: D2 improves both safety AND utility simultaneously (blocks destructive, preserves authorized)

---

### Core Finding 3: Multi-turn produces bounded erosion and architectural vulnerabilities

*(Same as Alpha — metadata leakage, emergent strategies, bounded not collapse)*

---

### Supporting Findings

- **Relationship effect**: Investor leaks 31.7% sensitive_work, friend 18.3%. Trust decomposes into read/write dimensions. (Strong finding, but relegated to supporting because surface asymmetry is the core RQ2)
- **Model scale**: Converges under D2. Policy dominates scale.
- **Cross-model**: All 5 models, 69-91pp. Structural.
- **Category breakdown**: sensitive_work hardest, personal_finance easiest.

---

### Take-away message (Story Beta)

**"The same governance policy costs 1pp on one interface and 37pp on another — you cannot evaluate one surface and deploy everywhere."**

The utility-security frontier is surface-dependent. Documents give a nearly free lunch. Structured state forces a painful tradeoff. Actions benefit from policy. Multi-turn reveals architectural side channels. Practitioners who test only their chat interface and declare "our policy works" are measuring one slice of a heterogeneous frontier. PACT-Bench measures the full surface.

---
---

## Head-to-head comparison

| Dimension | Story Alpha (Relationship) | Story Beta (Surface) |
|-----------|---|---|
| **Central message** | Trust decomposes into read/write; the frontier rotates by identity | The frontier shape is surface-dependent; you can't test one and generalize |
| **Title fit** | "Your agent vs Mine" = WHO matters → perfect fit | "How should they talk" = WHAT interface → decent fit |
| **Counter-intuitive score** | 🔥🔥🔥 (investor leaks MORE info but is SAFEST on actions — genuinely surprising) | 🔥🔥 (different surfaces have different costs — somewhat expected, but magnitude surprises) |
| **Novelty claim** | First to show relationship-conditioned frontier inversion | First to quantify surface-dependent policy cost |
| **Practical impact** | "You need per-relationship access control" | "You must evaluate every interface independently" |
| **Data strength** | Borderline significant (p≈0.03 one-sided, CIs overlap on sensitive_work) | Very strong (1pp vs 37pp, no overlap, massive effect size) |
| **Conceptual depth** | Deep — reveals trust is multi-dimensional | Medium — reveals heterogeneity, but "different is different" is less deep |
| **Risk** | Reviewer says "not significant" (McNemar p=0.12 overall) | Reviewer says "expected that structured data is harder" |
| **Unique to PACT-Bench** | YES — no other benchmark has relationship-conditioned labels | Partially — any benchmark with multiple surfaces could show this |
| **闭环 quality** | Excellent — title → who → inversion → need for relationship ACL | Good — title → interface → cost → need for surface-specific testing |

---

## My recommendation

**Alpha** for NeurIPS. The relationship inversion is the paper's unique intellectual contribution — no other benchmark can even *measure* this. The counter-intuitive nature (investor = more leakage but more safe) is the kind of finding that makes reviewers say "huh, I wouldn't have predicted that."

**Beta** is safer (stronger data, less debatable) but more pedestrian. "Different surfaces behave differently" is a good finding but not a *surprising* one. It's the kind of result that validates rather than surprises.

The strategic risk with Alpha: the p-value. Mitigation: you have Tina and Marcus completing (4-way test strengthens it), and the ACTION data is very strong (0% vs 63% info-leaking across requesters — no significance issue there). The QA inversion is borderline; the ACTION inversion is overwhelming.

Surface asymmetry still goes in the paper either way — it's just whether it gets RQ2 spotlight or a strong supporting paragraph within Discussion.
