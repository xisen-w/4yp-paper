# PACT-PAIR D3/MCC Audit Report

Date: 2026-05-17

Scope:
- Result package: `thesis/results/pact_pair_d3_mcc/`
- Runner/evaluator code: `research/scripts/solutions/run_d3_relationship.ts`, `research/scripts/solutions/run_mcc_access_control.ts`, `research/scripts/solutions/eval_llm_judge.ts`
- Production tool gates: `lib/ai/tools/notes-management.ts`, `lib/ai/tools/todo-management.ts`, `lib/ai/tools/index.ts`

This audit inspected the packaged JSON/JSONL files and the current implementation. It did not rerun the expensive LLM judge. On 2026-05-18, the pure MCC_H judged artifacts were copied from `research/runs/` into this package under `q1_200_notes_qa/mcc_h/` and `q201_400_todos_qa/mcc_h/` so the three-condition summary is auditable from the result folder itself.

## Verdict

This package is an L1 relationship-conditioned QA package, not the main L0 benchmark. R0 is the stranger/null-relationship requester inside L1. R0 should not be used as shorthand for Layer 0. The clean L0 benchmark remains the balanced category-level benchmark in `thesis/results/layer0_*`: 300 OK versus 300 Not OK across QA and actions.

The Notes QA claim is real and usable: D3 is prompt-policy-only with full data access, while MCC_H_D3 mounts only the configured note folders and the note tools enforce those folder IDs before returning search results or full note content.

The combined QA numbers are internally consistent with the packaged judge files. The headline combined result is supported as a QA result: D3 leak rate 15.5% versus MCC_H_D3 leak rate 8.0%, with utility dropping from 70.9% to 58.5%.

The pure MCC_H ablation is also now packaged. It shows 57.6% utility and 12.4% leak rate on combined Q1-400 QA. This is useful, but it is not a clean "MCC replaces D3" comparison because D3 includes relationship policy text while MCC_H does not. Pure MCC_H is best interpreted as a folder-mounting ablation.

The weak part is Q201-400 Todos QA. MCC is not precise folder-level todo access control in the current implementation. It only turns todo read/write on or off. `searchTodos` filters by `userId`, not by MCC folder IDs. Therefore Q201-400 can be reported as a todo QA stress test under coarse todo tool access, but not as evidence that MCC precisely mounted/unmounted todo folders.

There are no action results in this package. Do not claim A1-200 action performance from this folder.

## Audit Checklist

| Area | Check | Status | Evidence | Verdict |
|---|---|---:|---|---|
| Layer framing | Folder is L1 relationship-conditioned QA, not L0 | PASS | `L0_L1_COMPARISON_AUDIT.md`; relationship matrices; R0-R4 configs | Use L1 framing |
| Layer framing | R0 is the same as Layer 0 | FAIL | R0 is one requester inside L1; L0 is balanced 300/300 across QA/actions | Do not equate |
| Condition framing | D3 vs MCC_H_D3 isolates adding folder mounting to same D3 policy | PASS | Both conditions load `POLICY_D3_R*.md`; access layer differs | Valid comparison |
| Condition framing | D3 vs MCC_H cleanly isolates prompt vs MCC | WARN | D3 has policy text and full access; MCC_H has no policy text and scoped access | Operational contrast only |
| Condition framing | MCC_H R0 is explicitly told "stranger" | FAIL | No policy prompt; base prompt only names Tina Rodriguez | Structural Shared-only R0 |
| Artifact completeness | Q1-200 Notes QA has D3 and MCC, R0-R4 judge files and judged traces | PASS | 10 judge files, 10 judged traces | Complete |
| Artifact completeness | Q201-400 Todos QA has D3 and MCC, R0-R4 judge files and judged traces | PASS | 10 judge files, 10 judged traces | Complete |
| Artifact completeness | Pure MCC_H Q1-400 raw judged artifacts are packaged | PASS | `q1_200_notes_qa/mcc_h/`, `q201_400_todos_qa/mcc_h/` | Complete |
| Artifact completeness | Every packaged judged trace has 200 rows | PASS | `wc -l` over all 30 `*_trace_judged.jsonl` files | Complete |
| Artifact completeness | A1-200 action results are present | FAIL | README says actions not yet started; no action result files exist | Do not claim actions |
| Summary consistency | `summary_q1_200.json` matches per-run judge files | PASS | Counts match judge JSON: utility/security/errors | Usable |
| Summary consistency | `summary_q201_400.json` matches per-run judge files | PASS | Counts match judge JSON: utility/security/errors | Usable |
| Summary consistency | `summary_q1_400_combined.json` matches Q1-200 + Q201-400 sums | PASS | Totals add up across requesters and conditions | Usable |
| D3 implementation | D3 gives full note access | PASS | `notesAccess: { scope: 'all' }` in `run_d3_relationship.ts` | Correct |
| D3 implementation | D3 gives full todo read access | PASS | `todoAccess: { read: true, write: false }` | Correct |
| MCC implementation | MCC uses folder-scoped note permissions | PASS | `buildMCCPermissions()` sets `notesAccess.scope = 'folders'` and `folderIds = profile.folders` | Correct |
| MCC implementation | MCC note folder filtering is enforced by tools | PASS | `searchNotes` filters `userNotes` through `isFolderAllowed`; `getNoteContent` rejects unallowed folders | Correct |
| MCC implementation | MCC provides precise todo folder isolation | FAIL | `todoAccess` is only `{ read, write }`; `searchTodos` filters by `userId` | Not supported |
| Folder config | MCC profiles use concrete folder IDs | PASS | R4 trace records `folders_mounted: [5405, 5412]`; config maps 5405 to Projects and 5412 to Shared | Correct for packaged run |
| Folder config | Folder IDs are robust to reseeding | WARN | IDs are hard-coded numeric DB IDs | Needs seed snapshot or symbolic lookup |
| Evaluation | Utility denominator is `answer` + `L` | PASS | `eval_llm_judge.ts` lines 273-275 | Correct |
| Evaluation | Security denominator is `P` + `B` | PASS | `eval_llm_judge.ts` lines 279-281 | Correct |
| Evaluation wording | "Leak rate" means only strictly private leaks | FAIL | Boundary (`B`) disclosures are included | Rename or caveat |
| Evaluation reliability | Errors are included in denominators | FAIL | Judge excludes `judge_verdict === error` before scoring | Caveat R0 strongly |
| Report wording | README/result report clearly separate QA from actions | PASS | README now says L1 QA; actions not included in this package | Fixed 2026-05-18 |
| Report wording | Shared folder description is accurate | PASS | `full_results_analysis.md` now describes Shared as public/shared workspace material | Fixed 2026-05-18 |
| Report wording | "Strictly non-dominated" for aligned requesters | PASS | `full_results_analysis.md` now uses softer per-requester variance wording | Fixed 2026-05-18 |

## What Is Correct

1. D3 is implemented as full-access prompt policy.
   - `run_d3_relationship.ts` builds full permissions with all notes and todo read access.
   - The D3 prompt changes per requester via `POLICY_D3_R*.md`.

2. MCC_H_D3 is implemented as D3 prompt plus note folder mounting.
   - `run_mcc_access_control.ts` loads the same requester-specific D3 policies.
   - It switches permissions to `notesAccess.scope = 'folders'` with the per-requester folder list from `MCC_PROFILES.json`.
   - Judged traces record the mounted folder IDs, for example R4 has `[5405, 5412]`.

3. Notes folder blocking is real.
   - `searchNotes` fetches owner notes, then filters them with `isFolderAllowed(note.folderId)` before search/ranking.
   - `getNoteContent` fetches by note ID but returns "not found" if the note's folder is not allowed.
   - This supports the Notes QA claim that MCC prevents the model from seeing unmounted note folders.

4. The packaged QA numbers are internally consistent.
   - Q1-200 Notes QA: 20/20 requester-condition traces are present and each has 200 rows.
   - Q201-400 Todos QA: 20/20 requester-condition traces are present and each has 200 rows.
   - The combined summary adds the per-track counts correctly.

5. The main qualitative pattern is supported.
   - Misaligned requesters R3/R4 are where MCC helps most.
   - Combined R3 leak rate drops from 38.7% to 18.1%.
   - Combined R4 leak rate drops from 16.9% to 2.7%.

## What Is Wrong Or Needs Caveat

1. Q201-400 is not evidence of precise todo-folder MCC.
   - MCC profiles contain note folder IDs, but todo tools do not consume those IDs.
   - `lib/ai/tools/index.ts` only exposes or hides todo tools based on `todoAccess.read/write`.
   - `lib/ai/tools/handlers/todos/searchTodos.ts` filters todos by `userId`; it does not filter by folder, relationship, project, or MCC profile.
   - Therefore the todo-track MCC deltas are caused by prompt policy plus coarse todo tool availability, not by fine-grained mounted context cells.

2. "Leak rate" includes both private and boundary labels.
   - The evaluator treats expected labels `P` and `B` as the security denominator.
   - That is a valid metric, but the paper should call it "private/boundary disclosure rate" or explicitly define leak rate as `P+B`.

3. Error-heavy R0 cells are weaker evidence.
   - Q1-200 MCC R0 has 45 judge errors out of 200.
   - Q201-400 MCC R0 has 36 judge errors out of 200.
   - Errors are excluded from the utility/security denominators, so R0 percentages should not be overinterpreted.

4. Action results are absent.
   - The package contains no A1-200 action traces, DB diffs, or action judge summaries.
   - README correctly says actions are not yet started, but the benchmark headline can still mislead readers.

5. Folder IDs are correct for the packaged traces but brittle.
   - The profiles use hard-coded numeric IDs like 5405, 5406, 5412.
   - That is acceptable for a fixed seeded artifact, but a rerun after reseeding could silently break if IDs change.
   - A paper artifact should include the seed snapshot or resolve folder IDs by name at runtime.

6. Resolved report wording issues.
   - The earlier "strictly non-dominated" aligned-requester wording has been softened.
   - The stale Shared-folder examples have been replaced with "public/shared workspace material."
   - The README now frames this folder as L1 QA and keeps actions out of the package claim.

## Claim Guidance

Strong claims supported:
- "Prompt-only relationship policy can leak heavily under relationship ambiguity."
- "For Notes QA, folder-scoped MCC structurally reduces leaks because unmounted folders are not available to the model."
- "The largest MCC gains appear for requesters whose desired task utility overlaps poorly with sensitive adjacent folders, especially R3 and R4."

Claims that need caveats:
- "MCC cuts combined QA leak rate by 48%." This is numerically true, but say it combines Notes QA and Todos QA, where todo access is coarse.
- "MCC eliminates investor leaks." True for Q1-200 Notes QA R4; not true for combined Q1-400 because Q201-400 R4 still leaks 5/95.
- "MCC is strictly non-dominated." Too strong with current per-requester variance and R0 errors.

Claims not supported by this folder:
- "MCC precisely controls todo folder access."
- "MCC action safety is validated."
- "A1-200 action benchmark is complete."
- "All surfaces have the same folder-level isolation as notes."

## Recommended Fixes

1. Update the report wording for Q201-400:
   - Replace "folder-scoped access control" with "note folder-scoped access plus coarse todo tool gating" when discussing Todos QA.

2. If todo precision matters, implement todo-level MCC:
   - Add folder/project/category scope to `todoAccess`.
   - Enforce it inside `searchTodos`, `getTodo`, `createTodo`, `editTodo`, and `completeTodo`.
   - Rerun Q201-400 after the implementation.

3. Add a self-contained seed manifest:
   - Include folder ID to folder name mapping from the run seed.
   - Prefer symbolic profile definitions by folder name and resolve to IDs during seeding/running.

4. Rename the metric:
   - Use "P+B disclosure rate" or define "leak rate" in the first table where it appears.

5. Keep action claims out until action traces exist:
   - Use the snapshot/diff/rollback runner before adding action numbers to this package.

6. Keep the 2026-05-18 framing fixes in sync with the paper text:
   - L0 is the balanced 300/300 benchmark.
   - R0 is the L1 stranger requester, not L0.
   - Pure MCC_H is an ablation, not a direct replacement for D3.
