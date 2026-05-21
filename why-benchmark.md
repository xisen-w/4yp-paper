# Why Benchmark on SharedOS: The Research Surface

## What SharedOS Supports as a Research Platform

SharedOS is a multi-agent shared delegation system with five independently configurable axes:

| Axis | Description | Current Implementation |
|------|-------------|----------------------|
| **State** | Files, structured state (todos, contacts), memory shards | Per-agent isolated workspace with typed data surfaces |
| **Tools** | Read/write typed tools with granular permissions | `searchNotes`, `createNote`, `completeTodo`, `sendMessage`, etc. |
| **Governance Policy** | D0-D5 specificity gradient from "share everything" to "deny all unlisted" | Natural-language policies interpreted by the target agent at inference time |
| **Relationship Context** | Per-requester memory shards conditioning agent behavior | Each edge in the network carries its own context window |
| **Evaluation Modes** | Single-step (one request, one response) and multi-turn heartbeat (up to 240 ticks) | Deterministic turn-taking with configurable conversation depth |

This combinatorial surface is what makes SharedOS unique. Any experiment can vary one axis while holding the others fixed. A researcher can ask "what happens when I tighten policy from D2 to D4 while keeping state, tools, relationships, and evaluation mode constant?" and get a controlled answer. Or they can ask "what happens when I add a new data surface while keeping policy fixed?" and isolate the effect of state complexity on leakage.

The platform is not a single benchmark. It is an experimental substrate on which many benchmarks can be built.

---

## Two Main Benchmark Directions Built on SharedOS

### 1. PACT-PAIR (Dyadic) -- The Controlled Unit Test

**600 tasks. One requester probes one target. Isolation by design.**

PACT-PAIR fixes the network to a single edge and varies the request, the policy, and the conversation depth. It is the controlled experiment: every confound from network topology, transitive trust, and multi-hop routing is eliminated.

#### Currently Explored Research Questions

| RQ | Variable | Finding |
|----|----------|---------|
| RQ1: Policy Specificity | D0-D5 gradient | Higher specificity reduces leak rate but increases over-refusal |
| RQ2: Multi-Turn Erosion | Conversation depth (1-240 ticks) | Leak probability increases monotonically with turn count |
| RQ3: Relationship Conditioning | Per-requester context | Familiar requesters receive more disclosures, even when policy prohibits |

#### New Research Questions People Could Explore with PACT-PAIR

| Direction | Question | Why It Matters |
|-----------|----------|----------------|
| Formal adversarial attacks | How much worse is a trained attacker (PAIR, Crescendo, GCG) vs. organic probing? | Quantifies the gap between average-case and worst-case leakage |
| Cross-model adversarial testing | Stronger attacker model vs. weaker defender model -- does the capability gap dominate policy? | Tests whether governance can compensate for capability asymmetry |
| Per-relationship policy design | Can relationship-conditioned D2 eliminate over-refusal without increasing leakage? | The practical question for deployment: precision without cost |
| MCC (Mountable Context Cells) | Does folder-scoped access control reduce leak to near-zero? | Tests architectural isolation vs. policy-only isolation |
| Escalation protocols | Pre-search classification + post-generation audit -- what's the residual after two-stage defense? | Measures the ceiling of layered defense |
| Defense stacking | D2 + MCC + escalation combined -- do defenses compose multiplicatively or sub-additively? | Critical for deployment: are three partial defenses better than one strong one? |
| Data surface generalization | Adding emails, calendar, CRM to the existing file/todo surfaces -- does leakage scale with surface count? | Tests whether findings generalize beyond the current state types |
| Prompt sensitivity | How much does rephrasing the same D2 policy change outcomes? | Measures robustness of natural-language governance |
| Temperature/sampling | Stochastic defense reliability across sampling parameters | Quantifies the variance floor: even a good policy fails sometimes |
| Tool abuse patterns | Can the requester trick the target into using write tools as side-channel attacks? | Tests whether read-only probing assumptions hold when write tools exist |

---

### 2. PACT-NET (Network) -- The Integration Test

**25 agents. 997 tasks. 172 edges. The emergent properties that dyadic testing cannot reveal.**

PACT-NET embeds agents in a realistic social graph (professional clusters, personal clusters, cross-cluster bridges) and tests whether privacy properties that hold pairwise still hold at network scale.

#### What It Tests That Dyadic Cannot

| Phenomenon | Description | Why Dyadic Misses It |
|------------|-------------|---------------------|
| Transitive leakage | Third-party secrets appearing in legitimate answers | Requires at least three agents |
| Confused deputy attacks | "Marcus told me to ask you" -- authority impersonation | Requires network context to be meaningful |
| Non-contact probes | Routing enforcement -- can an unconnected agent reach you? | Requires a graph with non-edges |
| Cross-surface plants | Writing sensitive info INTO another agent's workspace | Requires bidirectional tool access |
| Cross-cluster leak rate | Professional-to-personal boundary failures | Requires cluster structure |
| Network amplification factor | Is observed leakage > predicted from independent dyadic rates? | The core question: do emergent effects exist? |

#### New Research Questions People Could Explore with PACT-NET

| Direction | Question | Why It Matters |
|-----------|----------|----------------|
| Information cascades | Does a leak to agent B propagate to agent C who asks B? | Tests whether leakage is contained or amplifying |
| Coalition attacks | Two agents coordinating to extract information neither could get alone | Tests whether pairwise security implies group security |
| Graph topology effects | Does hub-and-spoke leak more than mesh? | Informs network design for privacy |
| Role-based access at network scale | Does D2 scale to 25 different relationship policies without contradiction? | Tests governance scalability |
| Trust propagation | Does an agent trust C more because B vouched for them? | Tests whether social proof bypasses policy |
| Network-level MCC | Can folder-scoped access propagate transitively through the graph? | Tests whether architectural isolation composes across hops |

---

## Beyond PACT-PAIR and PACT-NET: Other Things SharedOS Enables

SharedOS is a platform, not a paper. The two benchmarks above are what we have built and validated. Below is what the platform makes possible for the broader research community.

| Direction | Description | Enabled By |
|-----------|-------------|------------|
| User study integration | Real humans replacing synthetic requesters | SharedOS's tool layer is model-agnostic; a human can issue the same API calls |
| Longitudinal studies | How does the privacy frontier evolve over weeks of real interaction? | Multi-turn heartbeat mode supports extended conversations |
| New task families | Persuasion, deception, social engineering beyond QA and actions | The task format is a JSON schema; new families slot in without platform changes |
| Multi-modal surfaces | Image/document sharing as a leakage channel | State layer supports arbitrary file types; tools can be extended to vision |
| Custom agent populations | Healthcare, legal, finance scenarios replacing TechFlow AI | Agent definitions are configuration; swap the persona and the state |
| Formal verification | Using SharedOS's typed tool layer to prove isolation properties | Tools have typed inputs/outputs amenable to static analysis |
| Red team competitions | SharedOS as a CTF platform for agent security | Evaluation mode + scoring already exists; add a leaderboard |

---

## Why Open-Sourcing This Matters

We have shown three things so far:

1. **Policy specificity matters** -- the D0-D5 gradient produces measurable, monotonic effects on both leakage and over-refusal.
2. **Multi-turn erodes privacy** -- even strong policies degrade over extended conversation.
3. **Network effects are real** -- dyadic safety does not guarantee network safety.

But we have explored a tiny fraction of the combinatorial surface. The platform supports experiments we have not run, with attack models we have not tried, on data surfaces we have not added, at scales we have not tested. The five configurable axes (state, tools, governance, relationships, evaluation mode) create a research space that no single team can exhaust.

Open-sourcing SharedOS, PACT-PAIR, and PACT-NET gives the community:

- A **reproducible baseline** against which new defenses can be measured
- A **modular platform** where new axes can be added without rebuilding the evaluation pipeline
- A **realistic substrate** that captures the deployment conditions (multi-agent, multi-turn, heterogeneous policy) that toy benchmarks miss
- A **shared language** for comparing results across papers: same tasks, same metrics, same platform

The question is not whether multi-agent privacy will be studied. It is whether it will be studied on realistic platforms or on synthetic toy problems. SharedOS makes the realistic option available to everyone.
