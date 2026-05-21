# Phase 2 Insights

## 1. Sparse Same-Pair Precedents Are Highly Conservative

`individual_10` has high PStop but low Utility:

| Model | PStop | Utility |
|---|---:|---:|
| gpt-5-mini | 90.8% | 69.8% |
| gpt-5.5 | 94.2% | 67.1% |

This is a classic privacy-gate failure mode: when the gate sees only 2--3 same-pair examples, it often treats uncertain work requests as private.

## 2. Relationship Transfer Improves Utility

`cluster_2nn_10` increases Utility:

| Model | Utility Individual 10 | Utility Cluster 10 | Gain |
|---|---:|---:|---:|
| gpt-5-mini | 69.8% | 76.7% | +6.9pp |
| gpt-5.5 | 67.1% | 71.3% | +4.1pp |

This supports the weaker claim:

> Similar requester precedents under the same owner can reduce false stops.

## 3. Anonymous Cluster Cards Are Not Enough

`cluster_2nn_10` had roughly the same average number of visible precedents as `individual_30`:

| Condition | Avg Precedents |
|---|---:|
| cluster_2nn_10 | 7.5 |
| individual_30 | 7.4 |

But it did not match Utility:

| Model | Cluster 10 Utility | Individual 30 Utility | Gap |
|---|---:|---:|---:|
| gpt-5-mini | 76.7% | 91.0% | -14.3pp |
| gpt-5.5 | 71.3% | 87.4% | -16.2pp |

Conclusion:

> Precedent count is not enough. Precedent semantic quality matters.

## 4. Direct Same-Pair Labels Remain Stronger

The same number of direct same-pair precedents was much more useful than shared anonymous precedents. This implies the owner-requester relationship is not fully captured by cluster labels alone.

## 5. Rich Cards Help, But Not Monotonically

The rich-card ablation has now been run:

| Condition | Shared Card |
|---|---|
| `cluster_2nn_10` | query pattern + requester cluster + category + decision |
| `rich_cluster_2nn_10` | source identity + relationship note + similarity reason + sensitivity + decision |

Result:

| Model | Rich vs Anonymous PStop | Rich vs Anonymous Utility | Interpretation |
|---|---:|---:|---|
| gpt-5-mini | +2.7pp | +1.3pp | Rich cards dominate anonymous cards |
| gpt-5.5 | +1.7pp | -3.2pp | Rich cards make GPT-5.5 safer but more conservative |

This answers the representation question with nuance:

> Relationship-aware cards matter, but richer context does not automatically improve utility. For stronger models, richer boundary details can shift the gate toward STOP.

## 6. Direct Same-Pair Labels Still Dominate Utility

Even rich cards did not match `individual_30`:

| Model | Rich Cluster 10 Utility | Individual 30 Utility | Gap |
|---|---:|---:|---:|
| gpt-5-mini | 78.0% | 91.0% | -13.0pp |
| gpt-5.5 | 68.1% | 87.4% | -19.4pp |

This means the current method does not prove "10% + two similar relationships equals 30% direct labels." It proves something narrower:

> Similar-relationship transfer is useful, and rich cards can improve the transfer signal, but direct same-pair labels remain the strongest source of utility.

## 7. Product Implication

For Aicoo/Systemind, the result is useful even though H2 failed:

- Users do not need a perfect global policy.
- Precedent learning is useful.
- But production precedent cards must balance **relationship richness** with **utility-preserving specificity**.
- If rich cards overemphasize boundary policy, the gate can become too conservative.

The product should store precedent records as structured policy objects, not just text examples:

```text
owner
requester
relationship summary
resource/tool pattern
sensitivity
decision
rationale
similarity reason
```

## 8. Thesis Takeaway

Phase 2 should be written as an ablation, not as the final algorithm:

> Same-owner relationship transfer improves sparse precedent learning. Rich relationship-aware cards further improve the mini model and improve security for GPT-5.5, but they can also make the gate more conservative. The broader lesson is that escalation quality depends on both retrieval and precedent representation; direct pair-specific labels remain the utility ceiling.
