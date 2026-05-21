# PACT-NET Audit Report

Date: 2026-05-17

Scope:
- Result package: `thesis/results/pact_net/`
- Raw source runs: `research/runs/pact_net_v2_d0_r1_2026-05-15T15-18-41`, `research/runs/pact_net_v2_d0_r2_2026-05-16T10-10-56`, `research/runs/pact_net_v2_d1_r1_2026-05-15T15-18-41`, `research/runs/pact_net_v2_d1_r2_2026-05-16T10-11-40`
- Runner/evaluator code: `research/scripts/run_pact_net_v2.ts`, `research/scripts/eval_pact_net.ts`, `research/scripts/seed_pact_net.ts`, `research/scripts/pact_net/ids.ts`
- Production contact path: `lib/ai/tools/agent-network.ts`, `lib/ai/agent-v04/route-integration.ts`

This audit inspected the thesis reports, raw `config.json`, `summary.json`, `eval.json`, `trace.jsonl`, and the implementation. It did not rerun the benchmark.

## Verdict

The main D0 versus D1 numerical result is reproducible from the raw eval files: average overall score improves by about +19.0pp, safety improves by about +44.8pp, and utility drops by about -9.8pp. Namespace isolation is real in the run configs and UUID prefixes. The high-level "base policy helps a lot" finding is supported.

However, the current thesis package has several paper-critical caveats:

1. The thesis folder is not self-contained. It contains reports only, not the raw `config.json`, `summary.json`, `eval.json`, or `trace.jsonl` files.
2. The action numbers are response-heuristic results, not DB-diff verified action outcomes.
3. The trace field `policy_loaded` is null, so policy application is proven by config/namespace setup, not per-contact trace instrumentation.
4. The report's model claim is wrong: source-agent runner deployment is `gpt-5.5`, but the contacted target agent path is hard-coded through `gpt-5-mini` deployment in `contact_agent`.
5. The report's infra-error wording is wrong: D0 R2 has 2 Phase 1 errors plus 3 Phase 2 errors; D1 R2 has a Phase 1 content-filter error excluded by clean metrics but not marked as `infra_error`.
6. `v2_methodology_audit.md` still contains stale D0-vs-D2 wording, while the reported V2 results are D0-vs-D1.

## Audit Checklist

| Area | Check | Status | Evidence | Verdict |
|---|---|---:|---|---|
| Raw runs | All four reported run directories exist | PASS | D0 R1, D0 R2, D1 R1, D1 R2 under `research/runs` | Complete |
| Raw runs | Each run has 997 Phase 1 tasks and 75 Phase 2 ticks | PASS | `trace.jsonl` line count = 1072; phase counts = 997/75 | Complete |
| Raw runs | `eval.json` exists for all four runs | PASS | Verified | Complete |
| Thesis package | Raw eval/trace/config files copied into `thesis/results/pact_net` | FAIL | Thesis folder contains markdown reports only | Not self-contained |
| Headline metrics | D0/D1 overall, utility, safety averages reproduce | PASS | Computed from raw `eval.json` | Supported |
| Namespace isolation | Conditions use distinct namespaces and UUID prefixes | PASS | D0 `d0_r*` prefix `10000000`; D1 `d1_r*` prefix `11000000` | Supported |
| Policy condition | D1 base policy loaded into target namespace | PASS WITH CAVEAT | `config.json` flags and `setupDefenseCondition()` write POLICY.md | Not traced per contact |
| Trace policy field | `policy_loaded` proves policy per contact | FAIL | 0 non-null `policy_loaded` rows in all four traces | Instrumentation missing |
| Model claim | Source and target agents both use gpt-5.5 | FAIL | Source runner uses gpt-5.5; target `contact_agent` uses `getAzureProviderConfig("gpt-5-mini")` | Report must be corrected |
| Action scoring | Reported action metrics are DB-diff verified | FAIL | All four runs have 0 non-null `action_db_eval`; eval sources are response heuristic/error only | Provisional only |
| Action instrumentation | Current runner can emit DB-diff action eval for fresh runs | PASS | Current `run_pact_net_v2.ts` snapshots/diffs/rolls back actions | Needs rerun |
| Infra reporting | "Phase 1 had zero infra errors across all runs" | FAIL | D0 R2 has Phase 1 `NET-A-0183` timeout and `NET-A-0184` ENOTFOUND | Report wrong |
| Error naming | `clean_metrics.infra_errors_excluded` means only infra errors | FAIL | Evaluator excludes all `actual === error`, including D1 R2 Azure content-filter error | Rename/caveat |
| Phase 2 reporting | Phase 2 resistance uses clean top-level phase2 score | PASS WITH CAVEAT | Top-level `phase2_accuracy = 1`; `phase_metrics[phase=2]` is 0 and should not be used | Eval footgun |
| Methodology report | D0-vs-D1 naming is consistent | FAIL | `v2_methodology_audit.md` section 8.2 says "D0 vs D2 Comparison Now Valid" | Stale |
| D1/D2 distinction | Paper can distinguish D1 and D2 in current flags | FAIL | Methodology says D1 and D2 flags are identical | Do not claim D2 distinction |

## Reproduced Headline Numbers

From raw `eval.json` files:

| Metric | D0 avg | D1 avg | Delta |
|---|---:|---:|---:|
| Overall accuracy | 55.9% | 74.9% | +19.0pp |
| Utility score | 88.5% | 78.8% | -9.8pp |
| Safety score | 26.6% | 71.4% | +44.8pp |

These match the main thesis report.

The per-run source configs also match the report:

| Run | Condition | Namespace | UUID prefix | Source deployment | Phase 1 | Phase 2 |
|---|---|---|---|---|---:|---:|
| D0 R1 | D0 | `d0_r1` | `10000000` | `gpt-5.5` | 997 | 75 |
| D0 R2 | D0 | `d0_r2` | `10000000` | `gpt-5.5` | 997 | 75 |
| D1 R1 | D1 | `d1_r1` | `11000000` | `gpt-5.5` | 997 | 75 |
| D1 R2 | D1 | `d1_r2` | `11000000` | `gpt-5.5` | 997 | 75 |

Important: "Source deployment" here means the source heartbeat runner model. It does not prove the contacted target agent used `gpt-5.5`.

## What Is Correct

1. The D0-vs-D1 result tables are numerically supported.
   - The main overall/utility/safety averages reproduce from raw eval files.
   - Category-level QA and action tables in `v2_results_analysis.md` match the raw eval structure.

2. Namespace isolation is correctly represented.
   - Each condition/rep has a unique namespace string.
   - User IDs are separated by condition prefix.
   - The race condition from the earlier shared UUID setup is addressed for these V2 runs.

3. D1 is applied through DB-backed POLICY.md setup.
   - `seed_pact_net.ts` and `run_pact_net_v2.ts` write/clear `POLICY.md` according to defense flags.
   - This supports condition-level D0/D1 assignment.
   - The missing part is per-contact trace proof.

4. The action-scoring caveat is mostly documented.
   - `v2_results_analysis.md` correctly says all four runs predate DB-diff action instrumentation.
   - It correctly says action rows are directional/provisional.

5. Current code now has the right action-eval direction for future runs.
   - `run_pact_net_v2.ts` currently snapshots the target workspace before action ticks, diffs after contact, records `action_db_eval`, and rolls back changes.
   - The reported runs do not contain that field, so this requires a fresh rerun before paper use.

## What Is Wrong Or Needs Fix

1. The model claim is wrong.
   - `README.md` and `v2_results_analysis.md` say `gpt-5.5 (Azure) for both source and target agents`.
   - `run_pact_net_v2.ts` uses the requested `deployment` for the source heartbeat model.
   - But `lib/ai/tools/agent-network.ts` builds the contacted target agent with `getAzureProviderConfig("gpt-5-mini")`.
   - `lib/ai/agent-v04/route-integration.ts` uses `azure(config.azure.deployment)` as the actual model. The `metadata.model` value is only emitted as metadata; it does not select the target model.
   - Therefore the reported experiment is best described as: source runner `gpt-5.5`, target agent execution path `gpt-5-mini`, judge/evaluator heuristic code as implemented.

2. The report's Phase 1 infra-error statement is false.
   - `v2_results_analysis.md` says Phase 1 had zero infra errors across all four runs.
   - Raw D0 R2 has two Phase 1 action errors:
     - `NET-A-0183`: tick timed out after 600s.
     - `NET-A-0184`: Azure endpoint ENOTFOUND.
   - D0 R2 also has three Phase 2 errors.
   - Correct wording: D0 R1 has 2 Phase 2 infra errors; D0 R2 has 2 Phase 1 infra errors and 3 Phase 2 infra errors.

3. `infra_errors_excluded` is misnamed in `eval.json`.
   - `eval_pact_net.ts` excludes every score with `actual === "error"` from clean metrics.
   - That includes infrastructure errors, but also includes at least one D1 R2 content-management-policy error on `NET-A-0260`.
   - Reports should say "errors excluded" unless the code separately filters true infra errors.

4. Action results are not DB-grounded.
   - Every reported run has 0 trace rows with non-null `action_db_eval`.
   - `action_metrics.eval_sources` are response heuristics plus error rows:
     - D0 R1: 508 response heuristic, 6 error.
     - D0 R2: 506 response heuristic, 8 error.
     - D1 R1: 510 response heuristic, 4 error.
     - D1 R2: 509 response heuristic, 5 error.
   - The action tables are useful for debugging, but not strong enough for final paper claims about real mutation safety.

5. `policy_loaded` is not instrumented.
   - All four traces have 0 non-null `policy_loaded` values.
   - This does not invalidate the run, because configs and namespace setup show condition assignment.
   - It does mean the paper cannot claim per-contact policy load was traced.

6. `v2_methodology_audit.md` is stale in places.
   - Section 8.2 is titled "D0 vs D2 Comparison Now Valid".
   - The current reported V2 results are D0 vs D1.
   - The same file also notes D1 and D2 currently have identical flags. This is important and should stay, but D2 should not be presented as a distinct evaluated condition here.

7. `phase_metrics` in `eval.json` is a footgun.
   - Top-level `phase2_accuracy` is 100% after excluding Phase 2 errors.
   - But `phase_metrics` reports Phase 2 accuracy as 0 because the generic phase-metric block does not correctly score Phase 2 dig traces.
   - Do not use `phase_metrics[phase=2]` for paper tables unless the evaluator is fixed.

8. The thesis package is not reproducible by itself.
   - `thesis/results/pact_net/` lacks raw configs, summaries, evals, and traces.
   - A reviewer cannot recompute the tables from the thesis folder alone.

## Claim Guidance

Strong claims supported:
- "In namespace-isolated V2 runs, D1 base policy substantially improves response-level safety over D0."
- "The D0-vs-D1 comparison is not polluted by the previous shared-UUID POLICY.md race."
- "QA/refusal metrics are stronger evidence than action metrics in the current report."

Claims that need caveats:
- "Safety improves by +44.8pp." Supported, but safety includes response-heuristic action categories.
- "Action-surface attacks are reduced." Directionally supported only; not DB-diff verified in reported runs.
- "Phase 2 persistent probes failed." Supported by top-level phase2 scoring, but explain that broad aggregate probes may be easier to refuse than single-shot precision attacks.

Claims not supported:
- "Both source and target agents used gpt-5.5."
- "Action outcomes were verified against database mutations."
- "Every contact trace proves whether POLICY.md was loaded."
- "Phase 1 had zero infra/errors across all runs."
- "D2 was evaluated as a distinct condition in these V2 results."

## Recommended Fixes

1. Correct the model wording immediately.
   - Replace "gpt-5.5 for both source and target agents" with "source heartbeat runner used gpt-5.5; contacted target agent path used the production `contact_agent` model configuration, currently `gpt-5-mini`."
   - If the intended experiment is truly gpt-5.5 target agents, patch `contact_agent` to respect the experiment deployment and rerun.

2. Copy raw artifacts into the thesis folder.
   - Add each run's `config.json`, `summary.json`, `eval.json`, and preferably compressed `trace.jsonl`.
   - Or add a manifest with checksums and exact source paths.

3. Fix infra/error reporting.
   - Update D0 R2 to "2 Phase 1 errors + 3 Phase 2 errors".
   - Rename `infra_errors_excluded` in reports to "errors excluded" unless the evaluator separates infra from content-filter/model errors.

4. Rerun PACT-NET actions with DB-diff instrumentation before final paper claims.
   - Current code is patched to record `action_db_eval`; the reported traces are not.
   - The final paper should split QA-strong results from action-provisional results unless rerun.

5. Add per-contact policy instrumentation.
   - Record `policy_loaded`, `policy_bytes`, and a `policy_hash` from `loadIdentityFiles()` in the target agent path.
   - Include the resolved target model/deployment in every trace row.

6. Fix stale D2 references.
   - Rename section 8.2 of `v2_methodology_audit.md` to D0-vs-D1 or make it a general namespace-isolation note.
   - Do not present D2 as distinct until D2 has distinct flags/policies and fresh results.

7. Fix `phase_metrics`.
   - Either remove the misleading phase 2 row from `phase_metrics` or compute it from Phase 2 dig scores the same way top-level `phase2_accuracy` does.

