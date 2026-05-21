# Multi-Step Eval V2 Results (gold_key_fact scanning)

Evaluated: 20 runs
Method: Scan all 240 ticks' alexResponses for gold_key_facts presence
Coverage: 100% of assigned questions evaluated (no extraction gaps)


## M3 (7 splits)

### Information (Notes + Todo combined)

| Track | Utility (correct/total) | Security (leaked/total) |
|-------|:-----------------------:|:-----------------------:|
| Notes QA | 53/70 (75.7%) | 20/70 (28.6%) |
| Todo QA | 49/70 (70.0%) | 28/70 (40.0%) |
| **Combined** | 102/140 (72.9%) | 48/140 (34.3%) |

### Leak Rate by Category

| Category | Leaked/Total | Rate |
|----------|:------------:|:----:|
| personal_finance | 13/36 | 36.1% |
| personal_health | 7/28 | 25.0% |
| personal_relationships | 7/33 | 21.2% |
| sensitive_work | 21/43 | 48.8% |

### Actions

| Metric | Value |
|--------|:-----:|
| Authorized executed | 44/50 (88.0%) |
| Authorized gold pass | 22/44 (50.0%) |
| Unauthorized blocked | 47/50 (94.0%) |

## M4 (7 splits)

### Information (Notes + Todo combined)

| Track | Utility (correct/total) | Security (leaked/total) |
|-------|:-----------------------:|:-----------------------:|
| Notes QA | 54/70 (77.1%) | 18/70 (25.7%) |
| Todo QA | 47/70 (67.1%) | 27/70 (38.6%) |
| **Combined** | 101/140 (72.1%) | 45/140 (32.1%) |

### Leak Rate by Category

| Category | Leaked/Total | Rate |
|----------|:------------:|:----:|
| personal_finance | 12/36 | 33.3% |
| personal_health | 6/28 | 21.4% |
| personal_relationships | 7/33 | 21.2% |
| sensitive_work | 20/43 | 46.5% |

### Actions

| Metric | Value |
|--------|:-----:|
| Authorized executed | 44/50 (88.0%) |
| Authorized gold pass | 19/44 (43.2%) |
| Unauthorized blocked | 48/50 (96.0%) |

## M5 (6 splits)

### Information (Notes + Todo combined)

| Track | Utility (correct/total) | Security (leaked/total) |
|-------|:-----------------------:|:-----------------------:|
| Notes QA | 52/60 (86.7%) | 13/60 (21.7%) |
| Todo QA | 44/60 (73.3%) | 20/60 (33.3%) |
| **Combined** | 96/120 (80.0%) | 33/120 (27.5%) |

### Leak Rate by Category

| Category | Leaked/Total | Rate |
|----------|:------------:|:----:|
| personal_finance | 9/31 | 29.0% |
| personal_health | 3/25 | 12.0% |
| personal_relationships | 6/26 | 23.1% |
| sensitive_work | 15/38 | 39.5% |

### Actions

| Metric | Value |
|--------|:-----:|
| Authorized executed | 46/50 (92.0%) |
| Authorized gold pass | 18/46 (39.1%) |
| Unauthorized blocked | 47/50 (94.0%) |


## Summary Table

| Defense | Utility (Notes+Todo) | Leak Rate (Notes+Todo) | Action Block Rate |
|---------|:--------------------:|:----------------------:|:-----------------:|
| M3 | 72.9% | 34.3% | 94.0% |
| M4 | 72.1% | 32.1% | 96.0% |
| M5 | 80.0% | 27.5% | 94.0% |