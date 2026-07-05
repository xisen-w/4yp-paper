# SharedOS: Measuring the Utility-Security Frontier of Cross-Boundary Agentic Delegation

This repository contains the ICML 2026 AIWILD workshop version of:

**How Should Your Agent Talk to Mine? Measuring the Utility-Security Frontier of Cross-Boundary Agentic Delegation**

Authors: **Xisen Wang, Adel Bibi, Qinghong Lin, Philip Torr, Jindong Gu**  
Affiliation: University of Oxford  
Keywords: multi-agent systems, privacy, security, LLM agents

SharedOS is a multi-agent shared delegation system for studying what happens when personal agents interact across ownership boundaries. Each agent holds private state, uses typed tools, and must decide what to share, refuse, or act on when another agent makes a request. The project measures the resulting **utility-security frontier**: how much useful coordination is possible before private information or unsafe actions leak across the boundary.

## News

- **2026-05-23:** Accepted to the **ICML 2026 AIWILD Workshop**.
- **2026-05:** A version of this work was also submitted to **NeurIPS**.
- **2026-05:** Workshop paper, appendix, and result figures added.

See [NEWS.md](NEWS.md) for release notes.

## Project Components

- **SharedOS:** a cross-boundary agent delegation system with private files, structured state, relationship context, governance policy, and typed tool access.
- **PACT-PAIR:** a 600-task pairwise benchmark covering files QA, structured-state QA, and action safety across one privacy boundary.
- **PACT-Net:** a 25-agent network-scale extension described in the appendix for studying transitive leakage, confused deputies, and network amplification.
- **Policy gradient:** D0 no policy, D1 generic privacy instruction, D2 category-specific deny list, plus layered prompt defences in ablations.
- **Evaluation modes:** single-step queries and 240-tick multi-turn heartbeat interactions.

## Repository Layout

```text
.
├── main.tex                         # ICML AIWILD workshop paper source
├── main.pdf                         # compiled workshop paper
├── appendix_datastore.tex            # synthetic datastore details
├── appendix_relationships.tex        # relationship-conditioned benchmark appendix
├── appendix_validation.tex           # validation and audit appendix
├── references.bib                    # bibliography
├── figures/
│   ├── shared_os_overview.png        # system overview
│   ├── fig_specificity.png           # policy-specificity result
│   ├── erosion-case-study-final.png  # multi-turn erosion case study
│   ├── fig_frontier_msg_security.png # frontier summary
│   └── gen_*.py                      # figure generation scripts
└── NEWS.md                           # project updates
```

## Key Findings

### 1. The frontier only moves when the policy names the boundary

Generic privacy instructions are statistically inert. In files QA, D1 is indistinguishable from D0, while D2 reduces file leakage from **83% to 14%** with utility preserved at **77%**.

![Policy specificity determines security across boundary surfaces](figures/fig_specificity.png)

### 2. Multi-turn interaction reveals erosion invisible to single-turn tests

Under D2, the multi-turn message leak rate remains bounded at **12.6%**, close to the single-turn rate, but the global leak rate rises to **38.0%** because sensitive facts surface incidentally in unrelated answers.

![Multi-turn erosion case study](figures/erosion-case-study-final.png)

### 3. The same policy creates different frontiers for different requesters

Relationship context changes both leakage and over-refusal. Under D2, requester leak rates range from **1.7% to 9.2%**, while over-refusal on legitimate items ranges from **31% to 86%**. The dominant practical failure becomes blocked legitimate access, not direct leakage.

![Privacy-utility frontier across policy, time, and relationship](figures/fig_frontier_msg_security.png)

### 4. Data surface matters

D2 costs only **1 percentage point** of utility on long-form files, but **37 percentage points** on structured state. Terse state queries share vocabulary with protected categories and trigger false refusals.

## System Overview

![SharedOS overview](figures/shared_os_overview.png)

SharedOS models each personal agent as an operating-system-like delegate. Private data is mounted behind tools, and cross-boundary interaction routes through a delegation layer that loads relationship context and governance policy. This lets the same architecture support collaboration while exposing measurable privacy and action-safety risks.

## Citation

If you use this project, please cite:

```bibtex
@inproceedings{wang2026sharedos,
  title = {How Should Your Agent Talk to Mine? Measuring the Utility-Security Frontier of Cross-Boundary Agentic Delegation},
  author = {Wang, Xisen and Bibi, Adel and Lin, Qinghong and Torr, Philip and Gu, Jindong},
  booktitle = {ICML 2026 AIWILD Workshop},
  year = {2026}
}
```

## Release Status

This directory currently packages the workshop paper, appendices, figures, and figure-generation scripts. Before a full public open-source release, add the executable SharedOS code, benchmark task files, evaluation scripts, model configuration examples, and the intended code/data licenses.
