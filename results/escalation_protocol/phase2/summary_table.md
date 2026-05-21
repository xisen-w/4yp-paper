# Phase 2 Summary Tables

## Overall Results

| Model | Scope | Frac | PStop | Utility | False Continue | False Stop | Avg Precedents | N | Errors |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5-mini | individual | 10% | 90.8% | 69.8% | 9.2% | 30.2% | 2.4 | 1548 | 0 |
| gpt-5-mini | cluster_2nn | 10% | 88.5% | 76.7% | 11.5% | 23.3% | 7.5 | 1548 | 0 |
| gpt-5-mini | rich_cluster_2nn | 10% | 91.3% | 78.0% | 8.8% | 22.0% | 7.5 | 1548 | 0 |
| gpt-5-mini | individual | 30% | 87.7% | 91.0% | 12.3% | 9.0% | 7.4 | 1186 | 0 |
| gpt-5.5 | individual | 10% | 94.2% | 67.1% | 5.8% | 32.9% | 2.4 | 1548 | 0 |
| gpt-5.5 | cluster_2nn | 10% | 92.7% | 71.3% | 7.3% | 28.7% | 7.5 | 1547 | 1 |
| gpt-5.5 | rich_cluster_2nn | 10% | 94.4% | 68.1% | 5.6% | 31.9% | 7.5 | 1548 | 0 |
| gpt-5.5 | individual | 30% | 92.1% | 87.4% | 7.9% | 12.6% | 7.4 | 1186 | 0 |

## Transfer Analysis

| Model | Comparison | Delta PStop | Delta Utility | Interpretation |
|---|---|---:|---:|---|
| gpt-5-mini | cluster_2nn_10 vs individual_10 | -2.3pp | +6.9pp | Cluster transfer improves utility but slightly reduces security recall |
| gpt-5-mini | cluster_2nn_10 vs individual_30 | +0.8pp | -14.3pp | PStop matches, Utility does not |
| gpt-5-mini | rich_cluster_2nn_10 vs individual_10 | +0.4pp | +8.2pp | Rich cards improve both security and utility over sparse same-pair |
| gpt-5-mini | rich_cluster_2nn_10 vs cluster_2nn_10 | +2.7pp | +1.3pp | Rich cards dominate anonymous cards for mini |
| gpt-5-mini | rich_cluster_2nn_10 vs individual_30 | +3.5pp | -13.0pp | PStop matches, Utility still does not |
| gpt-5.5 | cluster_2nn_10 vs individual_10 | -1.5pp | +4.1pp | Cluster transfer improves utility but slightly reduces security recall |
| gpt-5.5 | cluster_2nn_10 vs individual_30 | +0.6pp | -16.2pp | PStop matches, Utility does not |
| gpt-5.5 | rich_cluster_2nn_10 vs individual_10 | +0.2pp | +0.9pp | Rich cards slightly improve sparse same-pair |
| gpt-5.5 | rich_cluster_2nn_10 vs cluster_2nn_10 | +1.7pp | -3.2pp | Rich cards improve security but make GPT-5.5 more conservative |
| gpt-5.5 | rich_cluster_2nn_10 vs individual_30 | +2.3pp | -19.4pp | PStop matches, Utility gap widens |

## Decision Change Analysis

`cluster_2nn_10` compared against `individual_10` on the same 10% test set:

| Model | Same Decision | Changed Decision | Changed to Correct | Changed to Wrong | L Improved | L Regressed | P Improved | P Regressed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5-mini | 1379 | 169 | 116 | 53 | 113 | 39 | 3 | 14 |
| gpt-5.5 | 1418 | 129 | 83 | 46 | 82 | 38 | 1 | 8 |

`rich_cluster_2nn_10` compared against `cluster_2nn_10` on the same 10% test set:

| Model | Same Decision | Changed Decision | Changed to Correct | Changed to Wrong | L Improved | L Regressed | P Improved | P Regressed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5-mini | 1393 | 155 | 91 | 64 | 72 | 58 | 19 | 6 |
| gpt-5.5 | 1457 | 90 | 32 | 58 | 23 | 57 | 9 | 1 |

`rich_cluster_2nn_10` compared against `individual_10` on the same 10% test set:

| Model | Same Decision | Changed Decision | Changed to Correct | Changed to Wrong | L Improved | L Regressed | P Improved | P Regressed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5-mini | 1340 | 208 | 149 | 59 | 132 | 44 | 17 | 15 |
| gpt-5.5 | 1419 | 129 | 70 | 59 | 63 | 53 | 7 | 6 |

## Per-Category Results

### gpt-5-mini

| Scope | Category | N | L | P | PStop | Utility |
|---|---|---:|---:|---:|---:|---:|
| individual_10 | cross_cluster | 98 | 68 | 30 | 70.0% | 75.0% |
| individual_10 | should_answer | 638 | 593 | 45 | 75.6% | 81.6% |
| individual_10 | should_refuse | 495 | 122 | 373 | 93.6% | 42.6% |
| individual_10 | transitive_risk | 317 | 285 | 32 | 100.0% | 55.4% |
| cluster_2nn_10 | cross_cluster | 98 | 68 | 30 | 70.0% | 82.3% |
| cluster_2nn_10 | should_answer | 638 | 593 | 45 | 68.9% | 88.4% |
| cluster_2nn_10 | should_refuse | 495 | 122 | 373 | 91.4% | 46.7% |
| cluster_2nn_10 | transitive_risk | 317 | 285 | 32 | 100.0% | 63.9% |
| rich_cluster_2nn_10 | cross_cluster | 98 | 68 | 30 | 73.3% | 77.9% |
| rich_cluster_2nn_10 | should_answer | 638 | 593 | 45 | 68.9% | 90.7% |
| rich_cluster_2nn_10 | should_refuse | 495 | 122 | 373 | 94.6% | 48.4% |
| rich_cluster_2nn_10 | transitive_risk | 317 | 285 | 32 | 100.0% | 64.2% |
| individual_30 | cross_cluster | 77 | 57 | 20 | 60.0% | 93.0% |
| individual_30 | should_answer | 488 | 447 | 41 | 63.4% | 94.2% |
| individual_30 | should_refuse | 375 | 94 | 281 | 92.5% | 69.2% |
| individual_30 | transitive_risk | 246 | 222 | 24 | 95.8% | 93.2% |

### gpt-5.5

| Scope | Category | N | L | P | PStop | Utility |
|---|---|---:|---:|---:|---:|---:|
| individual_10 | cross_cluster | 98 | 68 | 30 | 86.7% | 69.1% |
| individual_10 | should_answer | 638 | 593 | 45 | 75.6% | 76.7% |
| individual_10 | should_refuse | 495 | 122 | 373 | 96.8% | 41.0% |
| individual_10 | transitive_risk | 317 | 285 | 32 | 96.9% | 57.9% |
| cluster_2nn_10 | cross_cluster | 98 | 68 | 30 | 80.0% | 86.8% |
| cluster_2nn_10 | should_answer | 638 | 593 | 45 | 68.9% | 81.5% |
| cluster_2nn_10 | should_refuse | 495 | 122 | 373 | 96.5% | 38.5% |
| cluster_2nn_10 | transitive_risk | 316 | 285 | 31 | 93.5% | 60.4% |
| rich_cluster_2nn_10 | cross_cluster | 98 | 68 | 30 | 86.7% | 69.1% |
| rich_cluster_2nn_10 | should_answer | 638 | 593 | 45 | 68.9% | 77.7% |
| rich_cluster_2nn_10 | should_refuse | 495 | 122 | 373 | 97.9% | 39.3% |
| rich_cluster_2nn_10 | transitive_risk | 317 | 285 | 32 | 96.9% | 60.0% |
| individual_30 | cross_cluster | 77 | 57 | 20 | 80.0% | 94.7% |
| individual_30 | should_answer | 488 | 447 | 41 | 61.0% | 91.3% |
| individual_30 | should_refuse | 375 | 94 | 281 | 97.9% | 66.0% |
| individual_30 | transitive_risk | 246 | 222 | 24 | 87.5% | 86.9% |
