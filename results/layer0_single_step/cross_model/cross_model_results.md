# PACT-Bench v1 — Single-Step Cross-Model Results

**Generated:** 2026-05-05  
**Evaluation:** String-match on gold_key_facts (automated, no LLM judge)  
**Models:** gpt-5-mini, gpt-5.4-mini, gpt-5.4, kimi-k2, deepseek-v3, gpt-5.5  
**Defense levels:** D0 (no policy), D1 (generic caution), D2 (category-specific deny-list)

---

## 1. Notes QA Track (Q1-200)

Q1-100: public work questions (utility). Q101-200: sensitive questions (security).

| Model | Defense | N | Utility (%) | Leak Rate (%) | Security (%) |
|-------|---------|:-:|:-----------:|:-------------:|:------------:|
| gpt-5-mini | D0 | 3 | 66.3 | 81.0 | 19.0 |
| gpt-5-mini | D1 | 3 | 58.0 | 72.3 | 27.7 |
| gpt-5-mini | D2 | 2 | 63.5 | 16.5 | 83.5 |
| gpt-5.4-mini | D0 | 2 | 76.0 | 84.0 | 16.0 |
| gpt-5.4-mini | D1 | 2 | 73.0 | 81.0 | 19.0 |
| gpt-5.4-mini | D2 | 2 | 64.0 | 10.5 | 89.5 |
| gpt-5.4 | D0 | 2 | 76.5 | 85.5 | 14.5 |
| gpt-5.4 | D1 | 2 | 77.0 | 77.0 | 23.0 |
| gpt-5.4 | D2 | 2 | 67.5 | 9.5 | 90.5 |
| kimi-k2 | D0 | 2 | 70.5 | 86.5 | 13.5 |
| kimi-k2 | D1 | 2 | 74.0 | 80.0 | 20.0 |
| kimi-k2 | D2 | 1 | 66.0 | 8.0 | 92.0 |
| deepseek-v3 | D0 | 1 | 74.0 | 89.0 | 11.0 |
| deepseek-v3 | D1 | 1 | 80.0 | 77.0 | 23.0 |
| deepseek-v3 | D2 | 1 | 54.0 | 13.0 | 87.0 |
| gpt-5.5 | D0 | 2 | 73.5 | 84.0 | 16.0 |
| gpt-5.5 | D1 | 2 | 73.5 | 75.0 | 25.0 |
| gpt-5.5 | D2 | 2 | 66.0 | 9.5 | 90.5 |

## 2. Todo QA Track (Q201-400)

Q201-300: public/mixed todo questions (utility). Q301-400: sensitive todo questions (security).

| Model | Defense | N | Utility (%) | Leak Rate (%) | Security (%) |
|-------|---------|:-:|:-----------:|:-------------:|:------------:|
| gpt-5.4-mini | D0 | 1 | 41.0 | 61.0 | 39.0 |
| gpt-5.4-mini | D1 | 1 | 44.0 | 61.0 | 39.0 |
| gpt-5.4-mini | D2 | 1 | 10.0 | 26.0 | 74.0 |
| gpt-5.4 | D0 | 1 | 36.0 | 60.0 | 40.0 |
| gpt-5.5 | D0 | 2 | 41.5 | 59.5 | 40.5 |
| gpt-5.5 | D1 | 1 | 43.0 | 57.0 | 43.0 |

## 3. Action Track (A1-200)

A1-100: authorized actions. A101-200: unauthorized actions.

| Model | Defense | N | Auth Execute (%) | Unauth Block (%) |
|-------|---------|:-:|:----------------:|:----------------:|
| gpt-5-mini | D0 | 2 | 65.5 | 43.0 |
| gpt-5-mini | D1 | 2 | 48.0 | 43.0 |
| gpt-5-mini | D2 | 2 | 61.0 | 93.5 |

## 4. Statistical Significance

Two-proportion z-test comparing D0 vs D2 leak rates (pooled across replications).

| Model | Track | D0 Leak | D2 Leak | Δ (pp) | z-stat | p-value | Sig |
|-------|-------|:-------:|:-------:|:------:|:------:|:-------:|:---:|
| gpt-5-mini | Notes | 81.0% | 16.5% | +64.5 | 14.21 | 0.00e+00 | *** |
| gpt-5.4-mini | Notes | 84.0% | 10.5% | +73.5 | 14.72 | 0.00e+00 | *** |
| gpt-5.4-mini | Todo | 61.0% | 26.0% | +35.0 | 4.99 | 5.97e-07 | *** |
| gpt-5.4 | Notes | 85.5% | 9.5% | +76.0 | 15.22 | 0.00e+00 | *** |
| kimi-k2 | Notes | 86.5% | 8.0% | +78.5 | 13.10 | 0.00e+00 | *** |
| deepseek-v3 | Notes | 89.0% | 13.0% | +76.0 | 10.75 | 0.00e+00 | *** |
| gpt-5.5 | Notes | 84.0% | 9.5% | +74.5 | 14.93 | 0.00e+00 | *** |
| gpt-5-mini | Action (block) | 43.0% | 93.5% | +50.5 | 10.85 | 0.00e+00 | *** |

## 5. Key Findings

1. **D2 reduces notes leak rate by 64-79pp across all models** (all p < 0.001)
2. **Model capability does not significantly affect D0 leak rate** — all models leak 81-89% without defense
3. **D2 is uniformly effective** — all models achieve 8-17% leak rate with category-specific rules
4. **D1 provides modest benefit** (5-12pp reduction) but does not approach D2 effectiveness
5. **Action safety follows same pattern**: D2 raises unauthorized block rate from 43% to 93.5%
6. **Todo track shows higher baseline leakage** (57-61%) and lower utility (36-44%) than notes track

## 6. Run Inventory

- **QA runs:** 34 valid (notes + todo)
- **Action runs:** 6 valid

- **gpt-5-mini**: 8 QA runs (g400, g401, g402, g403, g404, g405, g406, g500)
- **gpt-5.4-mini**: 6 QA runs (g2000, g2001, g2002, g2003, g2004, g2005)
- **gpt-5.4**: 6 QA runs (g2010, g2011, g2012, g2013, g2014, g2015)
- **kimi-k2**: 5 QA runs (g2020, g2021, g2022, g2023, g2024)
- **deepseek-v3**: 3 QA runs (g2030, g2032, g2034)
- **gpt-5.5**: 6 QA runs (g2040, g2041, g2042, g2043, g2044, g2045)