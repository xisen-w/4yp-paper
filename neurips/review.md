# Internal Consistency Audit: main.tex vs. Verified Data

Audit date: 2026-05-05  
Auditor: Claude (automated)  
Scope: Numbers claimed in text/tables vs. raw verified data sources

---

## 1. Confirmed Correct

| Claim (location) | Verification |
|---|---|
| Abstract "69--91 pp reduction" | Cross-model Table: gpt-5-mini +69, gpt-5.4-mini +80, gpt-5.4 +91, Kimi K2 +89, DeepSeek V3 +84. Range is 69--91. CORRECT. |
| Abstract "1 pp utility loss on documents" | D0 Files Util=78%, D2 Files Util=77%. 78-77=1pp. CORRECT. |
| Abstract "37 pp on structured state" | D0 States Util=55%, D2 States Util=18%. 55-18=37pp. CORRECT. |
| Table 2 Files QA: D0 Util=78, Sec=17, D1 Util=78.5, Sec=18.5, D2 Util=77, Sec=86 | Matches raw: D0 leak 83%→Sec=17%, D1 leak 81.5%→Sec=18.5%, D2 leak 14%→Sec=86%. CORRECT. |
| Table 2 States QA: D0 Util=55, Sec=41.5, D1 Util=60.5, Sec=37, D2 Util=18, Sec=92 | D0 leak 58.5%→Sec=41.5%, D1 leak 63%→Sec=37%, D2 leak 8%→Sec=92%. CORRECT. |
| Table 2 Actions: D0 Util=55, Sec=31.5, D1 Util=54, Sec=35.1, D2 Util=58.7, Sec=90 | Matches verified data exactly. CORRECT. |
| "D2 blocks 100% of unauthorised edits, 100% of wipe, 100% of sensitive creates" (line 235) | Raw: 0/40 + 0/32 + 0/32 = 0/104 total destructive. CORRECT. |
| "D0 executes 62.5% and D1 executes 55.8% of destructive actions" (appendix line 676) | D0: 65/104=62.5%, D1: 58/104=55.8%. CORRECT. |
| Table actions detail: D0 edit 30/40=75%, wipe 19/32=59.4%, create 16/32=50% | Matches verified data. CORRECT. |
| Table actions detail: D1 edit 23/40=57.5%, wipe 19/32=59.4%, create 16/32=50% | Matches verified data. CORRECT. |
| "D1 produces the highest overall refusal rate (39%) while adding only 3.6 pp to safety over D0" (line 235) | D1 safety 35.1% - D0 safety 31.5% = 3.6pp. CORRECT. |
| McNemar "10:10, p = n.s." for D0 vs D1 files (line 226) | 83% vs 81.5% with symmetric discordants → chi-sq=0, n.s. Consistent. CORRECT. |
| D2 leak rate "83% to 14% (69 pp)" on files (line 226) | 83-14=69. CORRECT. |
| "D2's overall leak rate rises from 14% (single-step) to 19.5% (Phase 1) and reaches 33% after 240 ticks" (line 275) | Matches Table ms_main "All sensitive" row. CORRECT. |
| "2.4x amplification" (line 275) | 33/14 = 2.36 ≈ 2.4x. CORRECT. |
| Cross-model D0 "leak at 83--93%" (line 331) | 83, 87, 92, 93, 93%. Range 83--93. CORRECT. |
| Cross-model "utility ranges from 78% to 98%" (line 331) | 78, 96, 98, 82, 91. Range 78--98. CORRECT. |
| Table 5 relationship: Jordan QA Util=58, Sec=92 | User: Jordan utility=57.5%→58 rounded, security=92.5%→92. CORRECT. |
| Table 5 relationship: Dana QA Util=71, Sec=88 | User: Dana utility=70.5%→71 rounded, security=88.5%→88. CORRECT. |
| Table 5 Actions: Tina 92/90, Marcus 89/85, Jordan 92/84, Dana 83/91 | Matches verified L1 action data. CORRECT. |
| "Dana's investor framing raises files QA utility (91% vs Jordan's 48%)" (line 358) | Raw: Dana files util=91%, Jordan files util=48%. CORRECT. |
| Multi-step gpt-5.5 D2 leak = 24.5% (Table ms_model_scale) | Matches verified. CORRECT. |
| "D0 leak rate drops from 83% (gpt-5-mini) to 39.5%" for gpt-5.5 (line 283) | Table ms_model_scale confirms. CORRECT. |
| Figure erosion-case-study.png exists (line 247) | File found at figures/erosion-case-study.png. CORRECT. |
| "2 replications" for gpt-5-mini single-step | Consistently stated (Tables, captions, appendix). CORRECT. |
| "1 replication per model except gpt-5-mini" for cross-model (Table crossmodel caption) | CORRECT. |

---

## 2. Inconsistencies Found

### 2.1 CRITICAL: "D0 blocks only 5% of sensitive edits" (line 235)

**Paper says:** "D0 blocks only 5% of sensitive edits"  
**Raw data says:** D0 edit_sensitive = 30/40 executed = 75% unsafe, meaning D0 blocks 10/40 = **25%**, not 5%.  
**Fix:** Change "5%" to "25%" or rewrite as "D0 executes 75% of sensitive edits"

### 2.2 CRITICAL: Figure 2 caption "D0/D1 fail at 81--100%" (line 221)

**Paper says:** "D2 achieves 0% unsafe on edit-sensitive and wipe operations where D0/D1 fail at 81--100%"  
**Raw data says:** The highest unsafe rate across all D0/D1 destructive categories is D0 edit_sensitive = 75%. D0 wipe = 59.4%, D1 edit = 57.5%, D1 wipe = 59.4%, D0/D1 create = 50%.  
**No combination reaches 81%, let alone 100%.**  
**Fix:** Change "81--100%" to "50--75%" (the actual range of D0/D1 unsafe rates on destructive categories)

### 2.3 CRITICAL: "D1 achieves 100% unsafe on wipe operations in one replication (11/16)" (line 682)

**Paper says:** "D1 achieves 100% unsafe on wipe operations in one replication (11/16)"  
**Arithmetic:** 11/16 = 68.75%, not 100%.  
**Fix:** Either the numerator/denominator is wrong (should be 16/16 for "100%"), or the claim should read "69% unsafe" (11/16). Given the pooled rate is 59.4% (19/32), one rep could be 11/16=68.75% and the other 8/16=50%. The "100%" claim is arithmetically impossible with "(11/16)".

### 2.4 MODERATE: Table ms_main vs. Table ms_model_scale discrepancy (33% vs 38%)

**Table ms_main (line 268):** "All sensitive Final = 33.0%"  
**Table ms_model_scale (line 298):** gpt-5-mini D2 Leak = 38.0%  
**Explanation in paper:** The appendix (line 824) states the ms_model_scale uses "V2 gold-scan evaluation method" while the main body table may use V1 progress-diff. The paper does NOT explicitly reconcile this 5pp gap.  
**Fix:** Add a footnote to Table ms_main or the text explaining that the 33% is from V1 per-category phase analysis while 38% is the V2 gold-scan re-evaluation across all 240 ticks for both QA surfaces (Notes + Todos combined).

### 2.5 MODERATE: "D0 and D1 multi-step leak rates are near-total (96% and 89%)" (Table ms_main caption, line 252)

**Paper says:** D0=96%, D1=89% multi-step leak rates  
**Available multi-step data:**  
- Table ms_headline (appendix): D0 leak=84.2%, D1 leak=72.9%  
- Table ms_model_scale: gpt-5-mini D0=83.0%, D1=79.5%  
**Neither matches 96%/89%.** These numbers may come from an older evaluation or files-QA-sensitive-only subset under a different method, but they are not substantiated elsewhere in the paper.  
**Fix:** Verify the source of 96%/89%. If from a files-sensitive-only V1 subset, state this explicitly. Otherwise correct to match Table ms_model_scale (83%/79.5%) or Table ms_headline (84.2%/72.9%).

### 2.6 MINOR: Figure 2 caption "47--100 pp" reduction range (line 221)

**Paper says:** "D2 (category-specific deny list) reduces leak/unsafe rates by 47--100 pp"  
**Calculation:** The minimum per-category reduction is states QA "personal relationships": D0=46.2% → D2=7.7% = 38.5pp. The maximum is files QA "personal finance": D0=82% → D2=4% = 78pp. For actions: edit_sensitive D0=75%→D2=0%=75pp, wipe 59.4%→0%=59.4pp, create 50%→0%=50pp.  
**The minimum is ~38.5pp, not 47pp. The maximum is ~78pp, not 100pp.**  
**Note:** If "100pp" refers to the security delta (e.g., D0 Sec=0% → D2 Sec=100% on some sub-category), that framing should be made explicit. If it refers to unsafe rates, the true range is approximately 38--78pp.  
**Fix:** Clarify what the "47--100 pp" refers to, or correct to "38--78 pp" (or restrict to the subset where this holds).

### 2.7 MINOR: Relationship text says "88% vs 93%" but uses different bases

**Paper (line 358):** "Dana's investor framing raises files QA utility (91% vs Jordan's 48%) while reducing security (88% vs 93%)."  
**Context:** The security numbers cited (88% vs 93%) are files-only security. But Table 5 shows overall QA security (88 and 92). This is technically correct but potentially confusing because the text paragraph follows Table 5. A reader checking Table 5 will see 92 for Jordan (overall), not 93 (files-only).  
**Fix:** Minor -- add "(files only)" qualifier to the security comparison, or note that Table 5 reports overall pooled numbers.

---

## 3. XX Placeholders Remaining

| Location | What's missing |
|---|---|
| Table crossmodel (line 322) | gpt-5.5: entire row (D0, D1, D2 Util/Sec/Ref + DeltaSec) |
| Table crossmodel (line 323) | gpt-5.4-mini: D1 columns (Util, Sec, Ref) |
| Table crossmodel (line 324) | gpt-5.4: D1 columns (Util, Sec, Ref) |
| Table crossmodel (line 325) | Kimi K2: D1 columns (Util, Sec, Ref) |
| Table crossmodel (line 326) | DeepSeek V3: D1 columns (Util, Sec, Ref) |
| Table 5 relationship (line 348) | Tina: QA Util and Sec |
| Table 5 relationship (line 349) | Marcus: QA Util and Sec |

**Total XX cells:** 34 (10 in gpt-5.5 row + 4x3=12 for D1 columns of other models + 4 for Tina/Marcus QA)

**Note:** The paper correctly flags these as "runs in progress at time of writing" (line 331, 337). For NeurIPS submission, all XX cells must be filled or the rows removed.

---

## 4. Suggestions

### 4.1 Reconcile multi-step numbers explicitly
The paper reports D2 multi-step leak as both 33% (per-category final in Table ms_main) and 38% (V2 gold-scan in Table ms_model_scale). Add a sentence explaining: "Table 3 reports per-category phase analysis on files QA (100 sensitive questions); Table 4 reports V2 gold-scan across all QA surfaces (200 sensitive questions combining files and states). The higher rate (38%) reflects inclusion of state queries, which erode differently under multi-turn pressure."

### 4.2 Fix the "81--100%" caption claim
This is the most visible error because Figure 2 is likely the first figure readers study after the abstract. The actual D0/D1 destructive-action unsafe rates are 50--75%. Either update the caption or, if the figure itself shows different bars (possibly per-sub-category within a single replication), align caption to figure data.

### 4.3 Consider removing the "(11/16)" parenthetical
If the intended claim is that D1 wipe operations are extremely unsafe, say "D1 executes 69% of wipe operations in one replication (11/16)" rather than claiming 100%.

### 4.4 Resolve "5% of sensitive edits" arithmetic
This error appears in the main body RQ1 paragraph and will be scrutinized by reviewers. D0 blocks 25% of sensitive edits. This may have been confused with "D0 blocks only 5% of ALL unauthorised actions" (since D0 Sec=31.5% means 68.5% executed). But neither reading gives 5%.

### 4.5 Fill or drop gpt-5.5 cross-model row before submission
The gpt-5.5 multi-step data already exists (Table ms_model_scale shows D0/D2 numbers). The single-step cross-model row could potentially be populated from the same runs if single-step eval was also done. If not feasible before deadline, remove the row rather than submitting with XX.

### 4.6 Abstract precision
The abstract says "600 one-to-one tasks across five model families under three governance policies". The body clarifies this means 600 tasks x 3 policies x 5 models = the full evaluation matrix. But a reviewer might read "600 tasks" as meaning only 600 total data points. Consider "600 tasks per configuration" or "3,600 evaluations" to avoid ambiguity. (The body already says "3,600 evaluations" in the figure caption.)

### 4.7 Consistent terminology for "security" vs "blocked" vs "safety"
The paper uses:
- "Sec" in QA tables = 100% - leak rate (fraction of sensitive queries with no disclosure)
- "Sec" in action row of Table 2 = block rate of unauthorized actions
- "Safety" in Table 5 = same as action Sec

This dual use of "Sec" for both information security and action safety in Table 2 is noted in the caption but could confuse a hurried reviewer. Consider renaming the Actions column to "Safety" in Table 2 for consistency with Table 5.

---

## Summary

- **3 critical errors** that would likely be caught by reviewers (5% claim, 81-100% claim, 100% unsafe with 11/16)
- **2 moderate inconsistencies** between tables that need reconciliation footnotes
- **2 minor issues** (figure caption range, table cross-referencing clarity)
- **34 XX placeholder cells** that must be filled before submission
- All headline claims in the abstract are verified correct
- The core finding (69-91pp reduction, 1pp utility cost on files, 37pp on states) is solid
