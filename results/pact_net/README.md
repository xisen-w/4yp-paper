# PACT-NET Results (Layer 2: Network Privacy)

25-agent SharedOS privacy benchmark measuring information flow across a multi-agent network.

## Experiment Overview

- **Benchmark**: PACT-NET V2 (namespace-isolated, 997 tasks, 25 agents, 9 clusters)
- **Model**: gpt-5.5 (Azure) for both source and target agents
- **Conditions**: D0 (no policy) vs D1 (base policy loaded into target agent system prompt)
- **Reps**: 2 per condition (4 runs total). All complete and evaluated.

## Headline Numbers (4-run averaged)

| Metric | D0 (no policy) | D1 (base policy) | Delta |
|--------|:-:|:-:|:-:|
| Safety | 26.6% | 71.4% | **+44.8pp** |
| Utility | 88.5% | 78.8% | -9.8pp |
| Overall | 55.9% | 74.9% | +19.0pp |
| Tradeoff ratio | | | **4.6:1** (safety gain / utility loss) |

## Key Files

| File | Purpose |
|------|---------|
| [`v2_results_analysis.md`](v2_results_analysis.md) | Full 4-run results with per-category breakdown, network metrics, V1 comparison, audit caveats |
| [`v2_case_studies.md`](v2_case_studies.md) | 3 cases per category (30 total): failure modes, success patterns, D0 vs D1 trace comparisons |
| [`v2_methodology_audit.md`](v2_methodology_audit.md) | Architecture, task taxonomy, execution model, eval methodology, reproducibility checklist |
| [`v1_vs_v2_comparison.md`](v1_vs_v2_comparison.md) | Why V1 data was corrupted, quantified deltas, what V1 still validates |

## Naming

- PACT-NET = Privacy Assessment for Cross-boundary Trust in Networks
- D0/D1/D2-D5 = Defense conditions (cumulative)
- T/D/C/X/A = Network metrics (Transitive leak, Confused deputy, Contact enforcement, Cross-cluster, Amplification)
- V1 = Pre-isolation runs (race condition on POLICY.md). V2 = Namespace-isolated (clean measurement)
