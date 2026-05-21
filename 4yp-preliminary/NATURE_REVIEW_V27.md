# Nature-Style Review of Current Main Thesis

Reviewed source: `pulse_4yp_thesis.tex` and included chapter files.

Frame used: claim -> evidence -> boundary. The main review risk is not lack of
interesting results; it is overclaiming, duplicate tables, and a few places
where terminology still carries older experiment designs.

## Executive Verdict

The thesis now has a coherent paper-level argument:

> Cross-boundary agent delegation is an infrastructure problem. PACT-PAIR shows
> the dyadic security--utility frontier; PACT-NET shows network-native failures;
> MCC and escalation show why enforcement must move from final-answer prompting
> toward a layered control plane.

The current draft is close enough to freeze experimentally. The remaining work
should be prose and figure reduction, not new experiments.

## Highest-Priority Revisions

### 1. Abstract overclaims the architectural conclusion

Location: `abstract.tex:5-7`

Issue: The abstract ends with "architectural enforcement--not prompt-level
restriction--is the path". This is directionally right, but too absolute. The
actual evidence shows prompt specificity helps, relationship-specific policy
helps, MCC helps with caveats, and escalation is gate-only. Nature-style
boundary discipline requires softening this.

Suggested framing:

> Our findings suggest that prompt-level restriction is necessary but
> insufficient: robust cross-boundary coordination requires architectural
> control surfaces that constrain what data is mounted and when tools execute.

Also tighten the benchmark description. "PACT-PAIR ... three relationship
tiers" is likely imprecise relative to the current R0--R4 relationship setup;
"PACT-NET ... chains of three or more agents" is too narrow, because the
chapter's value is third-party provenance, clusters, authority chains, and
amplification, not only chain length.

### 2. Formalism has a free variable in the entitlement subsets

Location: `chap_problem_setup.tex:35-43`

Issue: `E_{ij}: K_i x T_i -> {0,1}` is defined over an item and tool, but
`K_i^+(j)= {x in K_i : E_{ij}(x,t)=1}` leaves `t` free. This is a real
technical correctness issue.

Two clean fixes:

- Define tool-conditioned sets: `K_{i,t}^{+}(j)` and `K_{i,t}^{-}(j)`.
- Or define entitlement over an operation: `E_{ij}(x,o)` where `o` already
contains the tool and intended action.

I recommend the second fix because Chapter 6 escalation is tool-call based.

### 3. Chapter 3 still mentions escalation too early

Location: `chap_problem_setup.tex:4`

Issue: "tools, permissions, policies, share links, and escalation gates" appears
in the Chapter 3 overview, after the annotated instruction to remove pre-tool
escalation from this chapter. This makes the chapter feel like it is claiming
the full solution stack before the reader reaches Chapter 6.

Suggested fix: replace "and escalation gates" with "and contact-graph routing".
Keep escalation for Chapter 6.

### 4. PACT-NET chapter needs one hero figure

Location: `chap_failure_cases.tex:97-188`

Issue: Chapter 5 has six tables and no figures. Under the Nature-figure logic,
the chapter has a strong visual claim but no visual argument. The new plot set
already solves this.

Recommended insertion:

- Add `nature_pact_net_four_findings.pdf` at the beginning of Findings
  (`chap_failure_cases.tex:140-145`).
- Keep Tables `pact_net_composite`, `pact_net_family_results`, and
  `pact_net_network_metrics`.
- Cut or compress Tables `pact_net_world`, `pact_net_runs`, and
  `pact_net_task_families` into one compact benchmark-design table if space is
  tight.

### 5. PACT-NET transitive wording should avoid the wrong mental model

Location: `chap_failure_cases.tex:80, 146-150`

Issue: The current table says transitive risk is "A asks B about C's
information". That can sound like the requester explicitly asks for C. The core
case is subtler: A asks B, and B's answer carries C/provenance facts.

Suggested wording:

> A asks B; B's answer carries third-party or provenance facts about C.

This matches the user-facing clarification and keeps the PACT-NET distinction
sharp.

### 6. MCC network validation needs denominator/replication caveat

Location: `chap_solution_proposal.tex:148-166`

Issue: The PACT-NET MCC validation table mixes P0/P1 baselines averaged over two
replications with MCC rows that appear to be one validation run each. The table
caption does not say this. A reviewer can reasonably ask whether the comparison
is replication-balanced.

Suggested fix: in the caption or text, add:

> P0/P1 are the clean two-replication PACT-NET baselines; MCC_H and MCC_H+P1 are
> single validation runs and should be read as directional architectural
> evidence.

### 7. Escalation table should include N or completion notes

Location: `chap_solution_proposal.tex:228-250`

Issue: The table reports rates but not denominators per row. It also says one
GPT-5.5 cluster-2NN row had an API error but does not quantify the affected N.
For a final thesis this is acceptable only if the denominator is in the result
folder, but Nature-style reporting expects sample size near the table.

Suggested fix: add an `N` column or a one-line note with row denominators.

### 8. Chapter 4 contains over-absolute language

Location: `chap_architecture.tex:335`

Issue: "No amount of prompt engineering can resolve this mismatch" is too
strong. The same chapter reports prompt-level strategies with marginal
improvement. The correct claim is that prompt engineering does not fully remove
the dominant residual mechanism.

Suggested replacement:

> Better prompting may reduce the frequency of these failures, but it does not
> remove the underlying mismatch between category-level policies and continuous
> information sensitivity.

## Chapter-Level Reduction Plan

| Chapter | Current status | Reduction move |
|---|---|---|
| 1 Introduction | Strong and readable. | Only align abstract/contribution counts with final experiments. |
| 2 Related Work | Short enough. | No major cut needed. |
| 3 Problem + SharedOS | Good bridge now, but implementation section is long. | Cut 15-20% from implementation prose after formalism is stable. |
| 4 PACT-PAIR | Evidence-rich but table-heavy. | Keep hero figures and main tables; move some ablation tables to appendix or compress. |
| 5 PACT-NET | Conceptually sharp. | Add one hero figure; compress design tables. |
| 6 Solutions | Strong unified story. | Add caveats for MCC replication and escalation N; keep all three layers. |
| 7 Conclusion | Good boundary discipline. | Minor alignment with revised abstract only. |

## Claim-Evidence Map

| Claim | Evidence in draft | Status |
|---|---|---|
| Generic privacy prompts do not move the frontier. | PACT-PAIR D0/D1/D2 specificity results, Chapter 4. | Supported. |
| Category-specific policies have a ceiling. | D2 residual leaks, D3-D5 marginal gains, failure taxonomy. | Supported, but avoid "no prompt can". |
| Networked delegation creates failures PACT-PAIR cannot ask. | PACT-NET transitive, cross-cluster, amplification, deputy metrics. | Supported. Add hero figure. |
| MCC improves safety by structural absence. | PACT-PAIR three-condition table; PACT-NET validation. | Supported with caveats. State note-scoping and read/write limits. |
| Escalation can learn sparse owner boundaries. | Phase 2 gate ablation. | Supported as gate-only, not full pipeline. Include N and no-auto-decision. |
| Architectural enforcement is the path forward. | Combined evidence across MCC and escalation. | Directionally supported, but phrase as "requires layered control surfaces", not solved. |

## Figure Readiness

Recommended main-text figures:

1. Chapter 3: one security--utility example/case schematic.
2. Chapter 4: existing specificity/frontier figure.
3. Chapter 5: `nature_pact_net_four_findings.pdf`.
4. Chapter 6: keep tables rather than plots unless space allows.

Optional appendix:

- `nature_pact_net_policy_effect_scatter.pdf`
- `nature_pact_net_task_family_matrix.pdf`

## Final Reviewer Risk

The largest remaining reviewer risk is not experimental validity. It is
terminology drift:

- D0/D1/D2/D3 in PACT-PAIR versus P0/P1 in PACT-NET.
- P1 static per-agent policy versus D3 relationship-specific policy.
- MCC_H pure folder scoping versus MCC_H+D3 combined scoping plus policy.
- Escalation gate-only evaluation versus full end-to-end pipeline.

Keep these distinctions explicit every time a result is introduced.
