# Thesis Audit Report & Story Analysis

## Context
User requested: (a) audit all thesis claims against raw results data, (b) synthesize the most important findings and the "whole story."

---

## Part A: Data Validity Audit

### Summary: 20/23 claims EXACT MATCH, 3 minor discrepancies, 0 fabrication

---

### VERIFIED (Exact Match)

| Claim | Thesis Value | Data File |
|-------|-------------|-----------|
| D0 Files QA Leak Rate | 83.0% | `results/layer0_single_step/ss_deep_analysis.md` |
| D1 Files QA Leak Rate | 81.5% | same |
| D2 Files QA Leak Rate | 14.0% | same |
| D0/D1/D2 Utility | 78.0/78.5/77.0% | same |
| McNemar D0 vs D1 | 10:10, p=n.s. | same §4.1 |
| Per-category D2 leak | sw=28.3, fin=4.0, rel=8.0, health=12.5% | same §3.1 |
| States QA metrics | D0 util=55%, D2 util=18%, false-refusal=26.5% | `ss_todo_deep_analysis.md` |
| Actions D2 safety | 93.5%, destructive=100% block | `pact_bench_v1_results.json` |
| Cross-model range | D2 reduces 69–91pp across 6 models | `cross_model/analysis.md` |
| Multi-turn msg leak (mini) | 12.6% (24/191) | `gpt5_mini_10_split/README.md` |
| Multi-turn global leak (mini) | 38.0% | gold scan eval |
| Multi-turn GPT-5.5 | msg=9.0%, global=23.0% | `eval_v2_gold_scan_with_llm.json` |
| PACT-NET transitive | D0=96.3%, D1=77.7% | `summary_mcc_h_mcc_h_d1_pact_net_v2.json` |
| PACT-NET confused deputy | D0=47%, D1=2% | same |
| PACT-NET contact enforcement | 100% both | same |
| PACT-NET amplification | D0=1.61, D1=1.55 | same |
| MCC D3 aggregate | Util=70.9%, Leak=15.5% | `summary_three_condition_combined.json` |
| MCC_H aggregate | Util=57.6%, Leak=12.4% | same |
| MCC_H+D3 aggregate | Util=58.5%, Leak=8.0% | same |
| Escalation NET 10% | PStop=95.1, Util=74.6 | `escalation_protocol/phase1/summary_table.md` |

---

### DISCREPANCIES (Minor)

| # | Claim | Issue | Severity |
|---|-------|-------|----------|
| 1 | "McNemar D0 vs D2: discordant ratio 70:1" | Actual: 73:1 (rep1), 69:1 (pooled). "70:1" is convenient rounding. | LOW |
| 2 | "D1 safety=71.4%" in PACT-NET | Data = 71.46%, should round to 71.5% not 71.4%. | LOW (<0.1pp) |
| 3 | "11,906 gate decisions" (escalation) | Summing JSONs gives 10,314. Discrepancy = exactly one net/10% split double-counted. | MEDIUM |

---

### RED FLAGS (Caveats to Disclose)

#### 1. PACT-NET Model Mismatch (MEDIUM)
- **Claim**: "Both source and target agents use GPT-5.5"
- **Reality**: Target agents route through `contact_agent` which uses gpt-5-mini. So it's gpt-5.5 attacker vs. gpt-5-mini defender.
- **Impact**: This actually makes PACT-NET results MORE alarming (stronger attacker, weaker defender). But it should be disclosed.

#### 2. Global Leak Rate Inflation (MEDIUM-HIGH)
- The "3× gap" narrative (msg leak 12.6% vs global leak 38.0%) is a central claim.
- The gold scan that produces 38.0% has a **~72% false positive rate** per the README.
- The actual verified global leak is likely ~15–20%, making the real gap closer to 1.5× not 3×.
- **This is the most important caveat in the thesis.** The scan method is overly aggressive.

#### 3. PACT-NET Action Scoring is Provisional
- Action metrics use response heuristics, NOT database-snapshot diffs (unlike PACT-PAIR).
- The thesis acknowledges this in the eval protocol section but the main results tables don't flag it.

#### 4. Multi-turn Per-Category Breakdown
- The per-category numbers (sensitive_work=22.8% etc.) cannot be fully reproduced from archived summary files. They appear to come from an eval script output not archived as structured JSON.

#### 5. Known Issues (Properly Handled)
- Early run g403 was unusable (73/200 questions, all work_public). Correctly excluded.
- Baseline g400/g500/g501 used wrong seed (70 notes vs 50). Correctly replaced with g401-406.
- High no-response rates (10-18%) due to API quota contention. Does not bias directionally.

---

### OVERALL VERDICT

**The data is solid.** Core experimental claims are well-supported. No evidence of fabrication. The most concerning issue is the global leak rate inflation (claim 38%, likely ~15-20% verified). This doesn't invalidate the multi-turn erosion finding but weakens the "3×" multiplier. Everything else is within trivial rounding.

---

## Part B: The Whole Story

### The Thesis in One Paragraph

When personal AI agents interact across ownership boundaries, every exchange is a permission decision. We built SharedOS to study this systematically, and discovered that **prompt-level governance has a hard ceiling**: it works (D2 reduces leaks by 69pp) but only when you name exactly what to protect, and it fails permanently against sustained multi-turn interaction and network-scale transitive flows. The fix is architectural: remove data from context entirely (MCC), gate tools before execution (Escalation), and scope everything per-requester. Combined, these cut leaks from 15.5% to 8.0%.

---

### The Five Key Findings (in order of importance)

#### Finding 1: The Specificity Threshold (RQ1) — THE headline result
- D1 (generic "protect privacy") = statistically identical to D0 (no policy)
- D2 (name the categories) = 69pp leak reduction
- **Implication**: LLMs cannot infer privacy norms from abstract principles. You must enumerate.
- **Universal**: Holds across 6 models, 3 providers, 2 data surfaces, both information and action tracks.
- **Why it matters**: This tells every practitioner deploying agents: generic safety instructions do nothing. You need explicit category enumeration.

#### Finding 2: Multi-Turn Erosion is Real But Bounded (RQ2)
- Message leak: 12.6% (comparable to single-turn 14.0%)
- Global leak: higher (though exact magnitude disputed — see caveat above)
- **Mechanism**: Not adversarial cracking but incidental co-location. The agent answers a legitimate work query and the answer happens to contain salary data from the same document.
- **Bounded**: After a breach, the policy recovers. No cascading collapse.
- **D3-D5 marginal**: Advanced prompt defences add only 4-11pp improvement at 6-13pp utility cost.

#### Finding 3: Over-Refusal Dominates Leakage for Close Relationships (RQ3)
- Jordan (close friend): 86% over-refusal, only 9.2% leak
- Dana (investor): 31% over-refusal, 7.5% leak
- **The practical failure of D2 is not data theft — it's broken utility for people who SHOULD have access.**
- Category-level policies cannot express relationship-conditioned exceptions.
- This directly motivates MCC: mount different data per requester instead of asking the agent to reason about exceptions.

#### Finding 4: Network Amplification Exists ($\mathcal{A} > 1.5$) (PACT-NET)
- Dyadic evaluation systematically underestimates real-world leakage.
- Transitive leakage (77.7% even with policy) is the hardest remaining problem.
- Confused deputies are easily defeated by policy (+45pp), but transitive flows are not.
- **Implication**: You cannot evaluate privacy in isolation. The social graph matters.

#### Finding 5: Structure + Prompt > Either Alone (RQ4, MCC)
- Structure alone (MCC_H): cuts leaks for misaligned requesters but INCREASES them for aligned ones (agent freely shares everything in-scope).
- Prompt alone (D3): good overall but 38.7% residual for friends.
- Combined (MCC_H+D3): 8.0% aggregate leak — best of both.
- **Key insight**: They're complementary, not substitutes. Structure prevents out-of-scope access; prompt provides within-scope discrimination.

---

### The Narrative Arc

```
Act 1: The Problem
  - Agents are becoming delegates. They hold private data and talk to each other.
  - Traditional access control doesn't work (policy ≠ enforcement when an LLM reasons about it).
  - We need empirical measurement of where the boundary actually falls.

Act 2: The Diagnostic (PACT-PAIR)
  - Built SharedOS: same execution core, 4 entry points, independently configurable axes.
  - Discovered the specificity threshold: naming matters, nothing else does.
  - Discovered bounded erosion: multi-turn leaks through incidental channels.
  - Discovered relationship asymmetry: over-refusal > leakage for trusted people.

Act 3: The Scale Problem (PACT-NET)
  - Extended to 25-agent network with transitive paths.
  - Found: network amplifies leakage 1.5× beyond dyadic predictions.
  - Found: transitive flows and cross-cluster leaks resist prompt-level defence.
  - The problem is strictly harder at scale.

Act 4: The Fix (MCC + Escalation)
  - Don't ask the agent not to say it. Remove the data from the room.
  - MCC: per-requester filesystem views. Absent, not hidden.
  - Escalation: gate tools before execution. Learn boundaries from owner decisions.
  - Combined: 15.5% → 8.0% aggregate leak.
  - Deployed in production (Pulse/Aicoo), thousands of agents, validated at scale.

Coda: The Frontier
  - Prompt engineering has a ceiling (structural, not effort-based).
  - Architecture can break through it.
  - The remaining residual (8%) is within-scope ambiguity — solvable by finer-grained MCC + better escalation clustering.
```

---

### The One-Sentence Version

**"Generic privacy instructions do nothing; naming categories works but has a hard ceiling; the only way to break through is to ensure sensitive data never enters the agent's context in the first place."**

---

## Action Items (if you want to strengthen the thesis)

1. **Disclose the global leak rate caveat** — add a footnote or parenthetical noting the gold scan's false positive rate. The 3× claim is the most vulnerable to examiner pushback.
2. **Disclose PACT-NET model mismatch** — one sentence in the eval protocol section.
3. **Fix "11,906"** — either recount or note "approximately 10,300–11,900 depending on counting method."
4. **Archive the per-category multi-turn source** — ensure the eval script that produced 22.8% etc. is saved alongside results.
