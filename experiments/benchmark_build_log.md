# PART-Bench v1 Build Log

**Date**: 2026-04-28
**Builder**: Claude + Xisen
**Benchmark version**: questions.json v5

---

## Summary

Expanded PART-Bench from 200 Notes QA items to 600 total items across 3 tracks:

| Track | Items | ID Range |
|-------|-------|----------|
| Notes QA | 200 | Q001-Q200 |
| Todo QA | 200 | Q201-Q400 |
| Actions | 200 | A001-A200 |

## Changes Made

### 1. seed_experiment_groups.ts

- Added `TODO_FOLDERS` array: 8 folders (Work, Projects, HR, Finance, Health, Family, Personal, Shared)
- Expanded `TODOS` array: 50 → 150 items
  - Each todo now has: `title`, `description`, `folderId`, `priority`, `category`, `completed`, `dueDate`/`completedAt`
  - Distribution: 53 work_public, 20 sensitive_work, 20 personal_finance, 21 personal_health, 36 personal_relationships
  - Status: 89 pending, 61 completed
- Added `todoFolders` import from schema
- Updated `resetUserWorkspace()` to also clear `todo_folders`
- Added todo folder creation step in `seedGroup()`
- Updated todo INSERT to include `description`, `folder_id`, `priority`, `category`
- Removed unused `tags` from INSERT (no todos use tags)

### 2. questions.json (v4 → v5)

- Structure: added `tracks` object, `actions` array
- Categories: 5 original + 10 new todo categories = 15 total
- Notes QA (Q001-Q200): unchanged
- Todo QA (Q201-Q400): 200 new questions
  - Q201-Q300: correlated with Notes (same facts accessible through todo surface)
  - Q301-Q400: todo-only facts (unique to todo descriptions)
  - Uses `source_todos` field (not `source_notes`)
- Actions (A001-A200): 200 new tasks
  - A001-A100: Notes mutations (create/edit/delete)
  - A101-A200: Todo mutations (create/edit/delete/complete)
  - 9 category types with expected verdicts (execute/refuse/escalate)

### 3. experiment_procedure.md

- Updated A4: todo count 50 → 150
- Added A9: todo folder count = 8
- Added 2 new failure modes to known failures table

## Consistency Check Results

**Errors: 0**

All 600 items passed validation:
- Every `source_notes` title in Q001-Q200 matches a real note title
- Every `source_todos` title in Q201-Q400 matches a real todo title
- Every action `target_item` matches a real note or todo title
- All 400 question IDs unique (Q001-Q400)
- All 200 action IDs unique (A001-A200)
- Notes QA: 100 work_public + 30 sensitive_work + 25 personal_finance + 20 personal_health + 25 personal_relationships
- Todo QA: 100 work_public + 30 sensitive_work + 24 personal_finance + 20 personal_health + 26 personal_relationships
- Todo QA correlated block: 100 items (Q201-Q300)
- Todo QA todo-only block: 100 items (Q301-Q400)
- Actions: 100 notes + 100 todos; 60 execute + 110 refuse + 30 escalate

**Warnings: 14 (all false positives)**

The fuzzy gold_key_facts checker flagged 14 items where facts use slightly different formatting than the todo description text (e.g., "$650/mo" vs "$650" in description, ISO dates vs human dates). Manual review confirmed all facts are grounded in actual data.

## Todo Category Distribution

| Category | Count | Folders |
|----------|-------|---------|
| work_public | 53 | Work (15), Projects (26), Shared (9), other (3) |
| sensitive_work | 20 | HR (20) |
| personal_finance | 20 | Finance (20) |
| personal_health | 21 | Health (20), Personal (1) |
| personal_relationships | 36 | Family (26), Personal (7), other (3) |

## Action Category Distribution

| Category | Notes | Todos | Total | Verdict |
|----------|-------|-------|-------|---------|
| authorized_create | 25 | 22 | 47 | execute |
| authorized_edit | 25 | 20 | 45 | execute |
| authorized_complete | 0 | 8 | 8 | execute |
| unauthorized_edit_sensitive | 10 | 10 | 20 | refuse |
| unauthorized_wipe | 8 | 8 | 16 | refuse |
| unauthorized_create_sensitive | 8 | 8 | 16 | refuse |
| probing_action | 8 | 8 | 16 | refuse |
| info_leaking_action | 8 | 8 | 16 | refuse |
| unauthorized_strategic | 8 | 8 | 16 | refuse |

> **v5b**: Removed `delete` ops (no tool), rephrased as edit-clear (`unauthorized_wipe`). Merged `escalation_worthy` → `unauthorized_strategic`. Binary execute/refuse only.
>
> **v5c (rebalance)**: 62/138 → **100/100** with 50n+50t per side. Added 45 new execute actions (5 notes create, 15 notes edit, 7 todos create, 10 todos edit, 8 todos complete). Trimmed 38 refuse actions symmetrically. Fixed bug: 7 `authorized_complete` targets were already-completed todos — replaced with 8 pending work-public targets. Social norm audit: all 100 executes target Work/Projects/Meetings/Shared folders; all 100 refuses involve sensitive data, strategic overreach, or data exfiltration.

## Known Issues

1. **POLICY_M2.md is category-based, not folder-based for todos**: M2 uses semantic category rules ("personal finance", "personal health") which should generalize to todos. But it does NOT explicitly mention todo folders. This is by design — the benchmark tests whether the agent can apply category-level policy across surfaces.

2. ~~**Experiment runner needs updates**~~: DONE. `experiment_v2.ts` now supports all 3 tracks:
   - `single-all --from 1 --to 200` for Notes QA
   - `single-all --from 201 --to 400` for Todo QA
   - `action-all` for Actions (DB snapshot/diff/rollback)

3. **Previously-seeded groups (g401, g402) are stale**: They were seeded with the old 50-todo dataset. Need re-seeding before running experiments.

4. **Todos use encrypted columns**: `title` and `description` are `encrypted()` in schema. Raw SQL INSERT stores plaintext, which works for experiment purposes (same pattern as notes).

5. **Action permissions**: Action track sets `notes_access.access = "readwrite"` and `todo_access.write = true` so Alex's agent can execute mutations. QA tracks only need read access.

## Files Changed

- `research/scripts/seed_experiment_groups.ts` — TODO_FOLDERS, expanded TODOS, updated seed function
- `research/configs/questions.json` — v5 with 600 items (100/100 action balance)
- `research/scripts/experiment_v2.ts` — Todo QA support (Q201-400), Action track (snapshot/diff/rollback/gold_check)
- `research/scripts/eval_single_step.ts` — category-based security detection, action run eval
- `thesis/experiments/experiment_procedure.md` — updated commands for 3 tracks
- `thesis/experiments/benchmark_build_log.md` — this file
