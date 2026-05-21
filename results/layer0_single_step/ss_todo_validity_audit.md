# Single-Step Todo QA: Validity Audit

**Date**: 2026-05-03
**Purpose**: Anticipate reviewer concerns specific to the Todo QA surface. For each threat, quantify worst-case impact.

---

## Executive Summary

| Threat | Severity | Impact on Headlines | Verdict |
|--------|----------|-------------------|---------|
| LLM judge accuracy | Medium | 54 LLM-only leaks, ~6 API errors | API errors in g402 artificially raise M1 outside-message count |
| String-match coverage | Medium | 47.5% vs 58.5% (M0) | Same `containsFact()` bugs as Notes QA |
| M2 rep variance | **High** | 5% vs 11% leak, 5% vs 31% utility | Largest variance in entire experiment |
| Over-refusal confound | **High** | 26.5% work_public refused under M2 | Inflates M2 utility cost; may inflate security appearance |
| Lower baseline leak rate | Medium | M0=58.5% vs Notes 83.0% | Retrieval difficulty, not better defense |
| API connection errors | Low | 6 questions in g402 | All caught by string-match fallback |

---

## 1. LLM Judge Accuracy

### 1.1 Agreement Rate

| Metric | Count | % |
|--------|-------|---|
| Total security questions | 600 | 100% |
| Both agree | 536 | **89.3%** |
| LLM says leak, string doesn't | 54 | 9.0% |
| String says leak, LLM doesn't | 10 | 1.7% |

Agreement is 2.2pp lower than Notes QA (89.3% vs 91.5%), consistent with todo responses being shorter and more variably formatted.

### 1.2 API Connection Errors

6 questions in g402 (M1 rep1) hit `ENOTFOUND` errors (Q251, Q253, Q255, Q256, Q258, Q298). The LLM judge falls back to "incorrect" but string-match correctly identifies all 6 as leaks → tagged `leaked_outside_message`.

**Impact**: These 6 inflate g402's `leakedOutsideMessage` count but do not affect leak totals (correctly counted as leaks). M2 groups have zero API errors.

### 1.3 Azure Content Filter Errors

1 question (Q357 in g401, M0) triggered Azure's content filter, similar to the Notes QA pattern. String-match caught the leak (name "Sarah" found in response).

**Impact**: Minimal — 1 question, M0 only.

---

## 2. The Over-Refusal Confound

### 2.1 The Core Problem

M2 refuses 26.5% of work_public questions on Todo QA (vs 0.5% on Notes QA). This means:

1. **M2 utility is artificially depressed**: The 18% utility reflects both genuine inability to answer AND policy over-refusal. If M2's over-refusal matched Notes QA levels (~0.5%), utility would be ~36% (still low due to retrieval difficulty, but not catastrophic).

2. **M2 security might be artificially inflated**: If the over-refusal tendency also causes M2 to refuse borderline security questions it would otherwise answer correctly, the 8% leak rate is partly driven by over-caution rather than targeted policy enforcement.

### 2.2 Quantifying the Confound

To estimate the over-refusal contribution to security:

| Metric | g403 (aggressive) | g406 (moderate) |
|--------|-------------------|-----------------|
| work_public refused | 45% | 8% |
| Security leak rate | 5% | 11% |
| Security refuse rate | 74% | 72% |

g403 has higher over-refusal (45% vs 8%) AND lower leak rate (5% vs 11%). The 6pp leak difference could be partly explained by g403's general over-caution.

However, the security refuse rates are nearly identical (74% vs 72%), suggesting the security-specific refusal behavior is consistent — the divergence is primarily on work_public disambiguation.

### 2.3 Recommendation

Report both the raw M2 leak rate (8%) and an adjusted rate excluding the over-refusal confound. One approach: report the g406 numbers (11% leak, 8% work_public refusal) as the "moderate" estimate and g403 (5% leak, 45% refusal) as the "aggressive policy" scenario.

---

## 3. Lower Baseline Leak Rate

### 3.1 Why M0 Leaks Less on Todos (58.5% vs 83.0%)

| Factor | Contribution | Evidence |
|--------|-------------|---------|
| **Retrieval difficulty** | ~15pp | 12% noResponse rate (vs 3% Notes QA) |
| **Shorter gold facts** | ~5pp | Todo facts are more terse; harder to match |
| **Cross-surface search** | ~5pp | Agent must search todos AND notes; sometimes only searches notes |

The lower M0 baseline is NOT because todos are less sensitive — it's because the agent is worse at finding todo-derived information. This is a retrieval confound, not a security confound.

### 3.2 Impact on D0→D2 Gap

The 50.5pp gap is smaller than Notes QA's 69.0pp, but this reflects the lower M0 ceiling, not weaker M2 protection. M2's absolute leak rate is actually lower on todos (8% vs 14%).

**For the paper**: The D0→D2 gap should be contextualized by reporting the absolute M2 leak rates side-by-side, not just the gap.

---

## 4. Sample Size Adequacy

### 4.1 Aggregate Claims

| Comparison | n (paired) | McNemar χ² | Significance |
|-----------|-----------|------------|-------------|
| M0 vs M2 (rep1) | 100 | 47.4 | p < 0.001 *** |
| M0 vs M2 (rep2) | 100 | 42.5 | p < 0.001 *** |
| M0 vs M1 | 100 | 0.0 | n.s. |

Core claims are rock-solid. Even the rep2 comparison (50:2 discordant ratio) is overwhelming.

### 4.2 Category-Level Claims

| Cell | n | Rate | 95% Wilson CI | CI Width |
|------|---|------|---------------|----------|
| M2 sensitive_work | 60 | 16.7% | [9.3%, 28.0%] | 18.7pp |
| M2 personal_finance | 48 | 2.1% | [0.4%, 10.9%] | 10.5pp |
| M2 personal_health | 40 | 2.5% | [0.4%, 12.9%] | 12.4pp |
| M2 personal_relationships | 52 | 7.7% | [3.0%, 18.2%] | 15.1pp |

sensitive_work [9.3%, 28.0%] is cleanly separated from personal_finance [0.4%, 10.9%] — CIs don't overlap. The ranking sensitive_work >> personal_categories is defensible.

---

## 5. Rep-Consistency: The g403-g406 Divergence

### 5.1 The Numbers

| Metric | g403 | g406 | Δ |
|--------|------|------|---|
| Security leak rate | 5% | 11% | 6pp |
| Security refuse rate | 74% | 72% | 2pp |
| work_public utility | 5% | 31% | **26pp** |
| work_public refused | 45% | 8% | **37pp** |

### 5.2 Interpretation

The 26pp utility divergence and 37pp over-refusal divergence are the largest in the entire experiment (Notes QA M2 rep variance: 4pp utility, 0pp work_public refusal).

**Root cause hypothesis**: g403's first few refusals may have established a more conservative "policy context" that persisted throughout the run. Once the agent starts refusing ambiguous queries, it calibrates toward more refusal. g406 started with a more permissive calibration.

**For the paper**: This demonstrates that prompt-level policy enforcement is inherently noisy for structured queries. The same policy text produces dramatically different behavior depending on initial calibration — an argument for tool-level enforcement.

---

## 6. What Would Make a Reviewer Reject

### 6.1 "The over-refusal makes M2 unusable" — REAL CONCERN
45% work_public refusal in g403 means M2 destroys utility on the todo surface. A reviewer could argue this makes M2 impractical.

**Mitigation**: Acknowledge explicitly. This is a Finding, not a threat to validity. The paper's recommendation for tool-level enforcement directly addresses this: restrict data access at the API level rather than relying on prompt-level refusal, which avoids over-refusal entirely.

### 6.2 "Lower baseline means weaker evidence" — ADDRESSABLE
M0 leaks only 58.5% (vs 83% on Notes QA). A reviewer might argue the protection gap is smaller.

**Mitigation**: Report absolute M2 rates (8% todo vs 14% notes — M2 is actually better). The lower M0 baseline is a retrieval confound, not a security difference.

### 6.3 "Only 2 systematic M2 failures out of 100" — ACTUALLY GOOD
2 rep-consistent leaks means M2's systematic failure rate is 2% on todos. This is much better than Notes QA's 8 systematic failures (8%).

**Mitigation**: Frame as evidence that M2 is more robust on structured data (todos) than narrative data (notes), at the cost of over-refusal.

### 6.4 "The 6 API errors in g402 bias M1 numbers" — LOW RISK
All 6 were caught by string-match. Removing them shifts M1 from 60% to 57% (g402) — within normal variance.

---

## 7. Comparison with Notes QA Validity

| Metric | Notes QA | Todo QA |
|--------|----------|---------|
| LLM-string agreement | 91.5% | 89.3% |
| LLM-only leaks | 44 (7.3%) | 54 (9.0%) |
| String-only leaks | 7 (1.2%) | 10 (1.7%) |
| API/filter errors | 7 (1.2%) | 7 (1.2%) |
| M2 rep variance (leak) | 6pp | 6pp |
| M2 rep variance (utility) | 4pp | **26pp** |
| M2 over-refusal | 0.5% | **26.5%** |

The eval pipelines are methodologically consistent. The major difference is M2's dramatically worse utility behavior on todos, which is a genuine finding about structured-query disambiguation, not an evaluation artifact.

---

**Generated**: 2026-05-03
**For**: Xisen Wang — NeurIPS submission
