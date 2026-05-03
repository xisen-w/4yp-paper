# Actions Experiment Analysis - README

## Files in This Directory

### 1. `actions_preliminary_analysis.md` (19KB, 439 lines)
**Main analysis document** with comprehensive findings, including:
- Executive summary with key results
- Detailed safety analysis by M-level and category
- Utility analysis with breakdown of refusal types
- Concrete attack examples with agent response quotes
- Comparative analysis and tradeoff visualization
- Limitations and recommendations
- Full appendices with detailed statistics and methodology

**Use this for:** Writing papers, preparing presentations, understanding the full story

### 2. `actions_stats_summary.txt` (2.7KB)
**Quick reference** with just the numbers:
- Main results (safety/utility rates)
- Critical vulnerabilities
- Operation type breakdown
- Agent refusal rates
- Attack success examples
- Conclusions and recommendations

**Use this for:** Quick lookups, citing specific numbers, elevator pitches

### 3. `actions_visualization_notes.md` (3.5KB)
**Presentation guide** with:
- ASCII art visualizations for 6 key findings
- Recommended presentation flow
- Slide talking points
- Data quality caveats

**Use this for:** Creating slides, visualizations, conference talks

---

## Key Findings at a Glance

| Metric | M0 | M1 | M2 | Winner |
|--------|----|----|----|----|
| Safety (% blocked) | 31.5% | 35.1% | **90.0%** | M2 |
| Utility (% executed) | 55.0% | 54.0% | **58.7%** | M2 |

**Bottom line:** M2 achieves Pareto improvement (better on BOTH dimensions).

---

## Most Important Findings

1. **Edit operations are the Achilles' heel of M0/M1**: Only 5% block rate vs 100% for M2

2. **M1 provides almost no benefit over M0**: 3.6 percentage point safety improvement, slightly worse utility

3. **M2's utility advantage is counterintuitive**: Strict policies help agents make better decisions, not just more conservative ones

4. **All sensitive categories compromised in M0/M1**: HR (salaries), Finance (bank accounts), Health (therapy notes), Strategic (terminations)

5. **M2's refusals are mostly tool bugs**: Fix the folderId parameter issue to recover full utility

---

## Data Coverage

- Groups: g401-g406 (M0/M1/M2 × 2 replicates)
- Total actions analyzed: 604 (of 1200 planned)
- Status: Incomplete runs, but enough data for preliminary conclusions
- Date: 2026-04-30

---

## Recommended Next Steps

1. Complete the 200-action runs for all groups
2. Fix tool implementation bugs (folderId vs folderName)
3. Study M2's strategic operation failures (44% block rate)
4. Investigate why M1 has worse utility than M0

---

## For Paper Writing

### Abstract Candidate
> We evaluate three policy regimes for cross-boundary agent actions: no policy (M0), soft guidance (M1), and strict categorical rules (M2). Across 604 actions on real user data, M2 blocks 90% of unauthorized operations vs 31-35% for M0/M1, while achieving higher utility (59% vs 54-55%). Edit operations are particularly vulnerable in M0/M1 (95% attack success rate), enabling adversaries to modify salaries, medical records, and personnel decisions. Our findings suggest that explicit categorical policies provide clarity that improves both safety and utility, contradicting the assumed tradeoff.

### Key Stats for Citations
- "M2 blocks 2.6-2.9× more unauthorized actions than M0/M1" (90% vs 31-35%)
- "M0/M1 execute 95% of unauthorized edit operations" (1/20 blocked)
- "M1 has 39% false refusal rate vs 24% for M0" (worst utility)
- "All 10 consecutive edit-based attacks (A51-A60) succeeded in M0/M1, all blocked in M2"

---

## Contact

For questions about this analysis:
- Raw data: `/Users/wangxiang/Desktop/my_workspace/pulse/research/runs/v2/action_*_g40[1-6]_*/results.jsonl`
- Action definitions: `/Users/wangxiang/Desktop/my_workspace/pulse/research/configs/questions.json` (starting at line 6110)
- Experiment design: `/Users/wangxiang/Desktop/my_workspace/pulse/research/preliminary_finding_experiment_design.md`

