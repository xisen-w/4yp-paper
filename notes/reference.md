# Reference Analysis: Shunyu Yao's "Language Agents" Dissertation

> **Source**: Shunyu Yao, *Language Agents: From Next-Token Prediction to Digital Automation*, Princeton University PhD Dissertation, May 2024, 185 pages.
>
> **Purpose**: Deep structural analysis of Yao's dissertation as a reference model for the Pulse thesis. Focuses on narrative architecture, benchmark-first methodology, and how to justify experiments that use only your own methods.

---

## 1. Macro Architecture: The Three-Part Arc

Yao's dissertation is organized into three clean parts:

| Part | Chapters | Role | What it establishes |
|------|----------|------|---------------------|
| **Part I: Benchmarks** | Ch2 WebShop, Ch3 InterCode | "Here's a problem nobody can solve well" | Defines environments, shows existing methods fail |
| **Part II: Methods** | Ch4 ReAct, Ch5 Tree of Thoughts | "Here are methods that work" | Proposes reasoning techniques, evaluates on Part I benchmarks + others |
| **Part III: Framework** | Ch6 CoALA | "Here's how to think about all of this" | Unifying cognitive architecture framework |

**The crucial insight**: Parts I and II are *published papers* (NeurIPS 2022, ICLR 2023, NeurIPS 2023, arXiv 2023). Part III is a survey/framework paper. The dissertation is a *stapled thesis* --- each chapter stands alone as a published work, but the dissertation narrative weaves them into a coherent story.

### Parallel to Pulse

Our thesis has an analogous three-part structure:

| Pulse | Yao | Structural Role |
|-------|-----|-----------------|
| Ch4 Benchmark Design + Ch5 Failure Cases | Part I (WebShop, InterCode) | "Here's a problem, and here's how agents fail" |
| Ch6 Solution Proposal + Ch7 Experiments | Part II (ReAct, ToT) | "Here are our solutions, and they work" |
| Ch3 Problem Formulation | Part III (CoALA) | Formal framework tying everything together |

The key difference: Yao puts the framework *last* (as a synthesis), while we put the formal problem *first* (as a foundation). Both are valid. Yao's approach works because readers discover the need for a framework *after* seeing the messy empirical landscape. Our approach works because the context-security trade-off needs to be formally stated before the benchmark makes sense.

---

## 2. WebShop: Deep Dive on Benchmark Motivation

### How Yao motivates WebShop (Ch2, pp. 21-49)

The motivation follows a tight logical chain:

1. **Language agents need grounded environments** --- text games exist (TextWorld, ALFWorld) but are synthetic, small, lack real-world complexity
2. **Real web environments are too noisy** --- actual websites change constantly, have ads, are non-reproducible
3. **Therefore: build a simulated environment with real data** --- 1.18M real Amazon products, 12K human-written instructions, but in a controlled HTML environment

The critical move: Yao argues that **no existing benchmark tests what he cares about** (language agents doing complex web tasks with real product data). He doesn't attack existing benchmarks --- he shows they test *different things* and there's an empty space his benchmark fills.

### How we should motivate the Pulse benchmark

Our motivation is structurally similar but in a different domain:

| Yao's gap | Our gap |
|-----------|---------|
| Existing text game benchmarks are synthetic and small | Existing agent security benchmarks test single-turn attacks, not relational trust |
| Real web environments are non-reproducible | Real personal agents can't be safely tested with actual user data |
| No benchmark tests grounded web shopping | No benchmark simultaneously measures utility AND security across trust tiers |

**Key takeaway**: The benchmark motivation should emphasize what *existing benchmarks cannot test*. For us, that's the **dual measurement** (utility + security simultaneously) and the **trust-tier gradient** (family to stranger). This is genuinely novel --- most agent security papers only measure attack resistance, not the utility cost of defenses.

---

## 3. Why WebShop Can Use Only Its Own Methods (No External Baselines)

This is the most directly useful insight for our thesis. WebShop's experiment section (Ch2, pp. 35-45) uses only methods Yao himself builds:

### The methods tested in WebShop:
1. **Rule baseline** --- heuristic keyword search + random choice (lower bound)
2. **Imitation Learning (IL)** --- BART for search, BERT for choice, trained on human demonstrations
3. **IL + RL** --- Policy gradient fine-tuning on top of IL (upper bound from author's methods)
4. **Human performance** --- Amazon Turk workers doing the same tasks (ceiling)

### Why this works (no one asks "where's GPT-3?"):

**Reason 1: The benchmark is new.** When you *create* the benchmark, there are no prior results to compare against. You ARE the first. This is the strongest justification --- and it applies to us too. Nobody has a cross-boundary agent security benchmark with trust tiers.

**Reason 2: The baselines span a meaningful spectrum.** Rule (simple) -> IL (learned) -> IL+RL (learned+optimized) -> Human (ceiling). This creates a *gradient* that shows the methods are working, without needing external methods. The reader can see the improvement trajectory.

**Reason 3: Human performance provides the ceiling.** By including human evaluation (59.6% task score), Yao shows both (a) the task is hard (humans aren't at 100%) and (b) there's room for improvement (IL+RL at 28.7% is well below human).

**Reason 4: Ablations do the heavy lifting.** Instead of comparing against external methods, Yao runs detailed ablations:
- Search module ablation (what if you remove the learned search?)
- Choice module ablation (what if you simplify the choice model?)
- Reward component ablation (attribute matching vs option matching vs price)
- Sim-to-real transfer (does performance in simulation predict real Amazon performance?)

### Application to Pulse:

We have the same structural advantage:

| Yao's spectrum | Pulse spectrum |
|----------------|---------------|
| Rule baseline | M0: Naive (full access, no protection) |
| IL | M1: +Memory (relationship context) |
| IL+RL | M2: +MCC (permission enforcement) |
| Human ceiling | M3: +All (full system with escalation) |

Our M0 -> M3 progression IS the experiment. Each configuration adds one architectural layer. We don't need "someone else's agent security method" because:
1. **Our benchmark is new** --- no prior results exist for cross-boundary trust-tier evaluation
2. **Our baselines span a meaningful spectrum** --- M0 (0 protection) to M3 (full protection)
3. **The ablation IS the experiment** --- each config is an ablation of the full system
4. **We can include a human ceiling** --- have a human decide what to share for each query, measuring both accuracy and response time (this also gives us the overhead metric)

---

## 4. How Benchmark and Method Chapters Are Isolated

### Yao's isolation strategy

This is subtle and clever. WebShop (Ch2) and ReAct (Ch4) are kept separate even though ReAct is later tested ON WebShop:

**In Ch2 (WebShop):** The benchmark is evaluated with IL/RL methods. ReAct doesn't exist yet in the narrative. The chapter establishes: "here's a hard environment, here are reasonable methods, here's how far they get."

**In Ch4 (ReAct):** ReAct is introduced as a *general reasoning method*, not as a "solution to WebShop." It's tested on HotPotQA, FEVER, ALFWorld, AND WebShop. When ReAct achieves 40% success rate on WebShop (vs 28.7% for the best Ch2 method), this is presented as *evidence that ReAct generalizes* --- not as "fixing" WebShop.

**The isolation trick**: Each chapter has its own **research question**, its own **motivation**, and its own **primary evaluation domain**:
- WebShop asks: "Can we build a realistic benchmark for grounded language agents?"
- ReAct asks: "Does interleaving reasoning and acting help language agents?"

WebShop is evaluated with *task-specific trained methods*. ReAct is evaluated with *prompting-based general methods*. They operate at different levels of the stack. The fact that ReAct does well on WebShop is a **bonus finding**, not the chapter's thesis.

### Application to Pulse:

Our isolation should follow the same pattern:

**Ch4-5 (Benchmark + Failure Cases)**: Evaluate with M0 and M1 --- the *naive* configurations. The finding is: "here are the failure modes, here's the baseline performance, here's why the problem is hard." These chapters should NOT use MCC or IEP.

**Ch6-7 (Solutions + Experiments)**: Introduce MCC, Dual-Track Memory, IEP as *general architectural solutions*. Evaluate M2 and M3. The finding is: "these architectural interventions improve security without catastrophic utility loss."

The isolation is maintained because:
- Ch4-5 answers: "What goes wrong?" (diagnosis)
- Ch6-7 answers: "How do we fix it?" (treatment + evaluation)

Each has its own research question (RQ1-2 vs RQ3-4).

---

## 5. CoALA: The Framework Chapter as Synthesis

### What CoALA does (Ch6, pp. 113-148)

CoALA (Cognitive Architectures for Language Agents) is NOT a method you run experiments with. It's a **conceptual framework** that organizes all language agents along three axes:

1. **Memory**: Working memory (LLM context) + Long-term memory (episodic, semantic, procedural)
2. **Action space**: Internal (reasoning, retrieval, learning) + External (grounding)
3. **Decision-making**: Planning (propose, evaluate, select) + Execution

CoALA then uses this framework to:
- Classify existing agents (Table 6.2: SayCan, ReAct, Voyager, Generative Agents, ToT)
- Identify gaps (e.g., "updating retrieval procedures is understudied")
- Suggest future directions (modular agents, structured reasoning, long-term memory)

### Why it works as a dissertation chapter

CoALA serves three narrative functions:
1. **Retrospective coherence**: "See? All my previous work (WebShop, ReAct, ToT) fits into this unified picture"
2. **Scope expansion**: Positions the thesis as contributing to a *field*, not just individual papers
3. **Future work generator**: The framework naturally reveals empty cells = future research

### Relevance to Pulse

We don't have a CoALA-style chapter, but our **Ch3 Problem Formulation** plays a similar unifying role. The formal definitions ($F$, $S$, $M_{self}$, the Pareto frontier of $\mathcal{U}$, $\mathcal{S}$, $\mathcal{O}$) are our "CoALA" --- they provide the vocabulary that makes the rest of the thesis coherent.

One thing we could borrow: CoALA's **case study approach** (Section 6.5). We could add a section to Ch3 or Ch6 that casts existing agent systems (ChatGPT plugins, Notion AI, Google's Project Astra) into our framework, showing how they handle (or fail to handle) cross-boundary trust. This would strengthen our claim to generality.

---

## 6. Storytelling Architecture: The Narrative Spine

### Yao's narrative arc (one sentence per chapter):

1. **Introduction**: Language agents are the next paradigm; they need environments, methods, and frameworks.
2. **WebShop**: Here's a realistic web environment (benchmark) --- existing methods plateau at ~29%.
3. **InterCode**: Here's an even harder coding environment (benchmark) --- confirms the gap.
4. **ReAct**: Reasoning + acting together gives agents a 40% jump on WebShop and SOTA on QA tasks.
5. **Tree of Thoughts**: Deliberate planning with search gives agents another leap on reasoning tasks.
6. **CoALA**: Here's how to think about ALL agents --- memory, actions, decisions.
7. **Conclusion**: Language agents are a new field; here's what's next.

### The emotional arc:

**Problem** (Ch2-3): "Things are broken, look how bad current agents are at real tasks"
-> **Hope** (Ch4-5): "But if we add reasoning/planning, things get dramatically better"
-> **Wisdom** (Ch6): "Here's the big picture of what we've learned"

### Pulse's narrative should follow a similar emotional arc:

**Problem** (Ch4-5): "When personal agents talk to external entities, things go catastrophically wrong --- data leaks, social engineering works, memory contaminates"
-> **Hope** (Ch6-7): "But architectural enforcement (MCC + Memory + IEP) pushes the Pareto frontier dramatically"
-> **Wisdom** (Ch3 + Ch8): "Here's the formal framework for thinking about this, and here's what's next"

---

## 7. Key Techniques to Borrow

### 7.1 The Reward Function as Automated Judge

WebShop uses an automated reward based on:
- **Attribute F1**: Overlap between purchased and target product attributes
- **Option F1**: Overlap between selected and required options (color, size)
- **Price constraint**: Whether the product is within budget

This gives a **continuous score [0,1]** rather than binary pass/fail. The score is automatically computable, reproducible, and interpretable.

**For Pulse**: We should define an analogous automated scoring function:
- **Utility score**: Keyword/fact overlap between agent response and ground truth answer
- **Security score**: Binary (did the agent leak protected information? 0 or 1)
- **Escalation score**: Did the agent correctly escalate vs incorrectly escalate?

The March 10 run used heuristic eval. We should formalize this into a reproducible scoring function (or use LLM-as-judge with a rubric for the qualitative aspects).

### 7.2 Sim-to-Real Transfer Validation

Yao validates WebShop by checking whether simulated performance predicts real Amazon task performance (Table 2.4). The correlation is strong: methods that do well in simulation also do well on real Amazon.

**For Pulse**: We could validate our benchmark by checking whether performance on simulated guests predicts behavior with real users on the production Pulse system. This is Phase 4+ work, but worth designing for.

### 7.3 Human Baselines with Task Decomposition

Yao has humans do the same tasks and reports their scores (59.6% on WebShop). He also analyzes WHERE humans are better (complex multi-attribute queries) vs where agents are competitive (simple searches).

**For Pulse**: We should have humans (or the thesis author) manually answer the 8 Phase 1 queries in each guest role, deciding what to share. This gives:
- A human ceiling for utility
- A human baseline for security decisions
- A measurement of time/overhead for manual vs automated management

---

## 8. What Yao Does That We Should NOT Copy

### 8.1 Trained models
Yao trains BART, BERT, and uses RL fine-tuning. We don't train models --- our "methods" are architectural (tool filtering, memory sharding, prompt construction). This is fine and arguably stronger: our interventions are **model-agnostic**.

### 8.2 Multiple independent benchmarks
Yao has WebShop AND InterCode as separate benchmarks. We have one benchmark with multiple trust tiers. This is fine for a 4YP --- depth on one benchmark is better than breadth across two.

### 8.3 The "stapled thesis" format
Yao's chapters are published papers with their own related work sections, threat models, etc. Ours should be a more unified narrative (which it already is from the chapter plan).

---

## 9. Concrete Recommendations for Pulse Thesis

Based on this analysis:

1. **Ch4-5 should establish the failure landscape WITHOUT using our solutions.** Test M0 and M1 only. Show the problem is hard. This is our "Part I."

2. **Ch6-7 should introduce and evaluate solutions.** Test M2 and M3. Show architectural enforcement works. This is our "Part II."

3. **The experiment needs no external baselines.** Our M0-M3 spectrum IS the experiment, just like Yao's Rule->IL->IL+RL spectrum. Each config is an ablation.

4. **Add a human ceiling.** Have a human answer each query manually. Report time and quality.

5. **Formalize the scoring function.** Move from heuristic eval to a defined, reproducible scoring rubric.

6. **The motivation should emphasize the gap.** No existing benchmark simultaneously measures utility and security across trust tiers. We ARE the first.

7. **Consider adding a "cast existing systems" section.** Show how ChatGPT plugins, Notion AI, etc. would score on our benchmark (conceptually). This is our mini-CoALA.

---

## 10. Summary Table

| Dimension | Yao | Pulse | Lesson |
|-----------|-----|-------|--------|
| Structure | Benchmark -> Method -> Framework | Problem -> Benchmark -> Failure -> Solution -> Experiment | Both valid; ours is more unified |
| Benchmark motivation | No realistic web agent benchmark exists | No dual utility+security trust-tier benchmark exists | Emphasize the gap, not attacks on existing work |
| Methods tested | Only author's (Rule, IL, IL+RL) | Only author's (M0, M1, M2, M3) | Self-contained is fine when benchmark is new |
| Why no external baselines | New benchmark = no prior results | New benchmark = no prior results | Ablations + human ceiling compensate |
| Isolation between benchmark/method | Ch2 uses IL/RL; Ch4 uses prompting; different levels of stack | Ch4-5 uses M0-M1; Ch6-7 uses M2-M3; different RQs | Keep diagnosis and treatment in separate chapters |
| Automated scoring | Attribute/option F1 + price constraint | Keyword overlap + leak detection + escalation correctness | Must formalize before Phase 2 |
| Human ceiling | Amazon Turk workers (59.6%) | Manual human decisions on each query | Essential for calibrating expectations |
| Framework contribution | CoALA (organizing all agents) | Formal problem ($\mathcal{U}$, $\mathcal{S}$, $\mathcal{O}$ Pareto frontier) | Both provide vocabulary for the field |

---

*Written 2026-04-10. Based on full reading of all 185 pages of Yao's dissertation.*
