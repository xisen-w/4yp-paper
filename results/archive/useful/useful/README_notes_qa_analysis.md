# Notes QA Failure Analysis - Documentation Index

This directory contains a comprehensive analysis of Notes QA (Q1-200) experiments for groups g401-g406, focusing on failure cases and attack patterns for the NeurIPS paper.

**Date**: 2026-04-30  
**Analyst**: Claude Code (analysis agent)  
**Experiment**: M0/M1/M2 policy evaluation across 200 questions (100 utility + 100 sensitive)

---

## Files in This Analysis

### 1. `notes_qa_failure_analysis.md` (MAIN REPORT - 20k words)

**Purpose**: Comprehensive failure analysis with examples, patterns, and recommendations

**Contents**:
- Executive Summary (leak rates, utility, key findings)
- Section 1: M2 Leak Failures (84 cases)
  - Direct leaks (20 cases with examples)
  - Partial leaks (58 cases with examples)
  - Side-channel leaks (6 cases with examples)
  - Key patterns and root causes
- Section 2: M2 Utility Failures (zero detected)
- Section 3: M0/M1 Protection Successes (model's intrinsic safety)
- Section 4: Attack Surface Analysis (strategies + effectiveness)
- Section 5: Per-Category Breakdown (work, finance, health, relationships)
- Section 6: Recommendations (4 immediate fixes + 3 architectural improvements)
- Section 7: Conclusion (actionable next steps for paper + product)

**Use for**:
- Understanding failure modes in depth
- Writing Discussion section
- Designing M2+ improvements
- Reviewer response (detailed evidence)

---

### 2. `notes_qa_failure_summary_tables.md` (QUICK REFERENCE)

**Purpose**: Summary tables for quick lookup and paper writing

**Contents**:
- Table 1: Overall Performance by Group (leak rates, refusals, errors)
- Table 2: M2 Leak Types (direct/partial/side-channel breakdown)
- Table 3: M2 Leaks by Sensitive Category
- Table 4: Attack Strategy Effectiveness vs M2
- Table 5: M2 Leak Examples by Type
- Table 6: Comparison to Baselines (M0/M1/M2)
- Table 7: Recommended Fixes and Expected Impact
- Table 8: Category-Specific Leak Rates
- Table 9: Work_Public (Utility) Performance
- Table 10: Top 10 Most Leaked Sensitive Questions

**Use for**:
- Paper Results section (Tables 1, 3, 4, 6)
- Quick reference during paper writing
- Presentation slides (summary stats)

---

### 3. `notes_qa_attack_examples.md` (EXAMPLES FOR FIGURES)

**Purpose**: Concrete attack examples formatted for paper figures and presentations

**Contents**:
- Example Set 1: M2 Direct Leaks (business framing bypass)
- Example Set 2: M2 Partial Leaks (metadata disclosure)
- Example Set 3: M2 Side-Channel Leaks (query misrouting)
- Example Set 4: M0/M1 vs M2 Comparison (Mike's 1:1)
- Example Set 5: M0/M1 Protection Successes (model intrinsic safety)
- Example Set 6: Successful Attack Chains (multi-turn)
- Example Set 7: Failed Attacks (M2 success cases)
- Visual Summary: Attack Decision Tree
- Attack Taxonomy Table

**Use for**:
- Paper Figure 3: Attack examples (ATK-001, ATK-003, ATK-004)
- Paper Figure 4: M0 vs M1 vs M2 comparison
- Presentation: Attack examples with full dialogue
- Appendix: Attack taxonomy

---

### 4. `notes_qa_paper_stats.md` (KEY NUMBERS FOR WRITING)

**Purpose**: Statistics, claims, and quotes for paper writing

**Contents**:
- Main Results (headline numbers)
- Key Claims for Paper (5 major claims with evidence)
- Key Statistics by Section (Abstract, Intro, Methods, Results, Discussion)
- Statistical Tests (chi-square, effect size, consistency)
- Comparison to Baselines (M0, M1, intrinsic safety)
- Key Numbers for Presentation (slide-by-slide stats)
- Quotes for Paper (opening, problem, findings, recommendations)
- Related Work Comparisons (RBAC, IFC, DP)
- Figures for Paper (bar charts, pie charts, heatmaps)

**Use for**:
- Abstract writing (headline numbers)
- Introduction (motivation stats)
- Results section (statistical tests)
- Discussion (quotes and comparisons)
- Presentation slides (key numbers)

---

### 5. `failure_analysis_v2.json` (RAW DATA - 1.2MB)

**Purpose**: Machine-readable analysis results for further processing

**Contents**:
```json
{
  "groups": {
    "g401": {...},  // Per-group analysis
    "g402": {...},
    "g403": {...},
    "g404": {...},
    "g405": {...},
    "g406": {...}
  },
  "m2_leaks": [...],            // All 84 M2 leaks with full details
  "m2_utility_failures": [...],  // M2 over-refusals on work_public
  "m0_m1_protections": [...],    // M0/M1 successful refusals
  "attack_strategies": {...},    // Grouped by strategy + M-level
  "category_breakdown": {...}    // Grouped by category + M-level
}
```

**Use for**:
- Custom analysis scripts
- Generating additional figures
- Cross-referencing specific questions
- Exporting to other formats

---

## How to Use This Analysis

### For Writing the Paper

#### Abstract
1. Open `notes_qa_paper_stats.md` → "Key Numbers for Presentation" → Slide 1-2
2. Use: "M2 reduces leaks by 50% (81% → 42%) with zero utility cost"
3. Add: "We identify partial leaks (metadata disclosure) as 69% of M2 failures"

#### Introduction
1. Open `notes_qa_paper_stats.md` → "Quotes for Paper" → "Opening"
2. Use motivation stats: "81% of sensitive queries leak under no policy"
3. Problem statement: "Soft policies provide minimal improvement (76% leak rate)"

#### Methods
1. Open `notes_qa_failure_summary_tables.md` → Table 1
2. Describe: 6 groups, 200 questions each, 2 reps per M-level
3. Categories: work_public (Q1-100), sensitive (Q101-200, 4 subcategories)

#### Results
1. Main results: `notes_qa_failure_summary_tables.md` → Tables 1, 3, 4, 6
2. Examples: `notes_qa_attack_examples.md` → Example Sets 1-3
3. Statistical tests: `notes_qa_paper_stats.md` → "Statistical Tests"

#### Discussion
1. Failure patterns: `notes_qa_failure_analysis.md` → Section 1.5 (Key Patterns)
2. Attack effectiveness: `notes_qa_failure_summary_tables.md` → Table 4
3. Quotes: `notes_qa_paper_stats.md` → "Quotes for Paper" → "Key Finding"

#### Recommendations
1. Fixes: `notes_qa_failure_summary_tables.md` → Table 7
2. Architectural: `notes_qa_failure_analysis.md` → Section 6.2
3. Future research: `notes_qa_failure_analysis.md` → Section 6.3

---

### For Creating Figures

#### Figure 1: Leak Rate by Policy (Bar Chart)
- **Data source**: `notes_qa_failure_summary_tables.md` → Table 1
- **Template**: `notes_qa_paper_stats.md` → "Figures for Paper" → Figure 1
- **Values**: M0: 81%, M1: 76%, M2: 42%

#### Figure 2: M2 Leak Type Distribution (Pie Chart)
- **Data source**: `notes_qa_failure_summary_tables.md` → Table 2
- **Template**: `notes_qa_paper_stats.md` → "Figures for Paper" → Figure 2
- **Values**: Partial 58 (69%), Direct 20 (24%), Side-channel 6 (7%)

#### Figure 3: Attack Examples (Side-by-side comparison)
- **Data source**: `notes_qa_attack_examples.md` → Example Set 1
- **Layout**: 3-column (Question, M2 Response, Analysis)
- **Examples**: ATK-001 (hiring budget), ATK-003 (brokerage), ATK-004 (runway)

#### Figure 4: M0 vs M1 vs M2 Comparison
- **Data source**: `notes_qa_attack_examples.md` → Example Set 4
- **Layout**: 3-row comparison (same question, different policies)
- **Example**: Mike's 1:1 (Q127)

#### Figure 5: Category-Specific Protection (Heatmap)
- **Data source**: `notes_qa_failure_summary_tables.md` → Table 8
- **Template**: `notes_qa_paper_stats.md` → "Figures for Paper" → Figure 4
- **Values**: Work 48%, Finance 48%, Health 55%, Relationships 64%

---

### For Presentation Slides

#### Slide 1: Problem
- **Title**: "AI Agents Leak 81% of Sensitive Information"
- **Data**: `notes_qa_paper_stats.md` → "Key Numbers for Presentation" → Slide 1
- **Visual**: Single large number (81%) + icon

#### Slide 2: Solution
- **Title**: "M2 Policy Reduces Leaks by 50%"
- **Data**: `notes_qa_paper_stats.md` → Slide 2
- **Visual**: Before/after bar chart (81% → 42%)

#### Slide 3: New Attack Surface
- **Title**: "Partial Leaks: A Hidden Vulnerability"
- **Data**: `notes_qa_attack_examples.md` → Example Set 2 (ATK-003)
- **Visual**: Quote box with annotated leak points

#### Slide 4: Attack Effectiveness
- **Title**: "Business Framing Bypasses Categorical Rules"
- **Data**: `notes_qa_failure_summary_tables.md` → Table 4
- **Visual**: Grouped bar chart (Simple 21% vs Business 57%)

#### Slide 5: Recommendations
- **Title**: "Path to 5-10% Leak Rate"
- **Data**: `notes_qa_failure_summary_tables.md` → Table 7
- **Visual**: Fix → Impact flowchart

---

### For Reviewer Response

#### Q: "How do you know these are real leaks, not false positives?"

**Response**: 
1. Cite leak detection methodology: `notes_qa_failure_analysis.md` → Section 1.2-1.4
2. Show examples: `notes_qa_attack_examples.md` → Example Sets 1-3
3. Manual verification: "Each leak manually verified; gold facts present in response or metadata disclosed"

#### Q: "Why is M1 not much better than M0?"

**Response**:
1. Stats: `notes_qa_failure_summary_tables.md` → Table 6 (M0: 81%, M1: 76%)
2. Explanation: `notes_qa_paper_stats.md` → Claim 4
3. Quote: "Privacy protection requires explicit constraints, not model judgment"

#### Q: "Can these be fixed?"

**Response**:
1. Yes: `notes_qa_failure_summary_tables.md` → Table 7
2. Expected impact: Fix 1 alone eliminates 69% of current M2 leaks
3. Combined fixes: 5-10% leak rate projected

#### Q: "What about utility trade-offs?"

**Response**:
1. Zero trade-offs: `notes_qa_failure_summary_tables.md` → Table 9
2. M2 answered 100% of work_public questions correctly
3. No false positive refusals detected

---

## Workflow: From Analysis to Paper

### Step 1: Read Executive Summary (5 min)
- File: `notes_qa_failure_analysis.md` → Executive Summary
- Get: High-level findings, leak rates, key patterns

### Step 2: Review Summary Tables (10 min)
- File: `notes_qa_failure_summary_tables.md` → Tables 1-6
- Get: Numbers for Results section

### Step 3: Pick Examples (15 min)
- File: `notes_qa_attack_examples.md` → Example Sets 1-3
- Select: 2-3 examples for figures (ATK-001, ATK-003, ATK-004)

### Step 4: Write Sections (2-3 hours)
- Abstract: Use `notes_qa_paper_stats.md` → Main Results
- Intro: Use `notes_qa_paper_stats.md` → Quotes (Opening, Problem)
- Results: Use `notes_qa_failure_summary_tables.md` → Tables 1, 3, 4, 6
- Discussion: Use `notes_qa_failure_analysis.md` → Section 1.5 + 6.1-6.2

### Step 5: Create Figures (1-2 hours)
- Figure 1: Bar chart from Table 1
- Figure 2: Pie chart from Table 2
- Figure 3: Attack examples from `notes_qa_attack_examples.md`
- Figure 4: M0/M1/M2 comparison (Mike's 1:1)
- Figure 5: Category heatmap from Table 8

### Step 6: Prepare Rebuttal Materials (30 min)
- Common questions: See "For Reviewer Response" section above
- Evidence: Cross-reference to specific tables/examples
- Quotes: Use `notes_qa_paper_stats.md` → "Quotes for Paper"

---

## Key Insights Summary (TL;DR)

1. **M2 reduces leaks by 50%** (81% → 42%) but still leaks in 42% of sensitive queries
2. **Partial leaks dominate** (69%): Refusals reveal metadata (note IDs, folders)
3. **Business framing bypasses rules** (57% success): "For planning" misaligns intent
4. **M1 provides minimal improvement** (76% vs 81%): Model judgment insufficient
5. **Personal relationships best protected** (64%), **sensitive work worst** (48%)
6. **Zero utility cost**: M2 maintains 100% accuracy on work_public questions
7. **Fixes available**: Standardized refusals + expanded rules → 5-10% leak rate projected

---

## Contact & Maintenance

**Primary Contact**: Xisen Wang (xisen@example.com)  
**Analysis Date**: 2026-04-30  
**Last Updated**: 2026-04-30

**To Update Analysis**:
1. Re-run `/research/scripts/analyze_failure_cases_v2.py` with new data
2. Review `failure_analysis_v2.json` for changes
3. Update markdown reports with new statistics
4. Increment version in this README

**To Add New Analysis**:
1. Create new section in `notes_qa_failure_analysis.md`
2. Add corresponding table to `notes_qa_failure_summary_tables.md`
3. Add examples to `notes_qa_attack_examples.md` if applicable
4. Update key numbers in `notes_qa_paper_stats.md`
5. Add entry to this README index

---

## Appendix: File Sizes

```
notes_qa_failure_analysis.md        ~60 KB  (20k words, comprehensive)
notes_qa_failure_summary_tables.md  ~25 KB  (tables for paper)
notes_qa_attack_examples.md         ~40 KB  (examples for figures)
notes_qa_paper_stats.md             ~35 KB  (key numbers, quotes)
failure_analysis_v2.json            ~1.2 MB (raw data)
README_notes_qa_analysis.md         ~15 KB  (this file)
```

**Total**: ~1.4 MB (easily version controlled, shareable)

---

## Related Files (Not in This Directory)

**Experiment Data**:
- `/research/runs/v2/single_m0_g401_q1-200_2026-04-28T18-35-22/results.jsonl`
- `/research/runs/v2/single_m1_g402_q1-200_2026-04-28T18-35-23/results.jsonl`
- `/research/runs/v2/single_m2_g403_q1-200_2026-04-28T18-35-23/results.jsonl`
- (+ 3 more for g404-g406)

**Questions Metadata**:
- `/research/configs/questions.json` (Q1-200 definitions + gold facts)

**Analysis Scripts**:
- `/research/scripts/analyze_failure_cases_v2.py` (enhanced leak detection)

---

**End of README** | Generated: 2026-04-30
