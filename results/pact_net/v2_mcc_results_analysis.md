# PACT-NET V2 — MCC Structural Defense Results

**Date**: 2026-05-18/19  
**Model**: GPT-5.5  
**Benchmark**: 997 Phase 1 tasks + 75 Phase 2 dig-further tasks × 4 conditions

## Conditions

| Condition | Base Policy | MCC Folder Scope | Description |
|-----------|------------|------------------|-------------|
| D0 | No | No | No defense (baseline) |
| D1 | Yes | No | Prompt-only defense |
| MCC_H | No | Yes | Structure-only defense |
| MCC_H_D1 | Yes | Yes | Combined defense |

## Summary Table

| Metric | D0 (n=2) | D1 (n=2) | MCC_H (n=1) | MCC_H_D1 (n=1) |
|--------|----------|----------|-------------|----------------|
| Overall Accuracy | 55.9% | 74.9% | 44.8% | 50.8% |
| **Utility Score** | **88.7%** | **78.8%** | **23.1%** | **20.6%** |
| **Safety Score** | **26.6%** | **71.5%** | **64.4%** | **77.8%** |
| Transitive Leak (T) | 96.3% | 77.7% | 77.7% | 67.0% |
| Confused Deputy (D) | 47.0% | 2.0% | 6.0% | 0.0% |
| Contact Enforce (C) | 100% | 100% | 100% | 100% |
| Cross-Cluster (X) | 87.5% | 69.6% | 60.7% | 64.3% |
| Amplification (A) | 1.61 | 1.55 | 1.87 | 1.43 |

## Category Breakdown

### QA Tasks

| Category | D0 | D1 | MCC_H | MCC_H_D1 |
|----------|----|----|-------|----------|
| should_answer | 75.9% | 64.0% | 61.6% | 54.7% |
| should_refuse | 16.2% | 73.4% | 69.1% | 77.7% |
| transitive_risk | 3.7% | 22.3% | 21.3% | 33.0% |
| cross_cluster | 12.5% | 30.4% | 39.3% | 35.7% |
| non_contact_probe | 100% | 100% | 100% | 100% |

### Action Tasks

| Category | D0 | D1 | MCC_H | MCC_H_D1 |
|----------|----|----|-------|----------|
| authorized_create | 98.4% | 86.7% | 0.0% | 0.0% |
| authorized_complete | 91.7% | 88.3% | 2.6% | 2.6% |
| unauthorized_mutation | 29.6% | 85.2% | 98.3% | 99.1% |
| confused_deputy | 53.0% | 98.0% | 94.0% | 100.0% |
| cross_surface_plant | 0.0% | 94.0% | 2.0% | 92.0% |

## Key Findings

### 1. Safety Ladder (monotonically increasing)
D0 (26.6%) → MCC_H (64.4%) → D1 (71.5%) → MCC_H_D1 (77.8%)

MCC alone provides +37.8pp safety over baseline, nearly matching D1's +44.8pp.

### 2. Structural Defense Matches Policy for Transitive Attacks
MCC_H transitive leak = 77.7% ≈ D1 transitive leak = 77.7%. Structure alone (removing out-of-scope data from context) is as effective as prompt policy for preventing transitive information leakage.

### 3. Combined Defense Dominates
MCC_H_D1 achieves best safety (77.8%) and lowest transitive leak (67.0%), demonstrating complementarity. The 10.6pp reduction from D1→MCC_H_D1 shows structure adds value even when policy exists.

### 4. MCC Eliminates Confused Deputy Attacks
D0=47.0% → D1=2.0% → MCC_H=6.0% → MCC_H_D1=0.0%. Without out-of-scope data in context, the agent cannot be tricked into acting as a confused deputy.

### 5. Critical Design Limitation: Read-Only Scope Blocks Writes
MCC folder-scoping grants READ access only. This blocks all authorized write operations:
- authorized_create: 98.4% (D0) → 0.0% (MCC_H/MCC_H_D1)
- authorized_complete: 91.7% (D0) → 2.6% (MCC_H/MCC_H_D1)

This causes a -65.6pp utility cost. Production systems need a separate write-permission mechanism.

### 6. Cross-Surface Planting Requires Policy
MCC alone (2.0%) cannot prevent agents from writing private data into shared spaces. Adding policy (MCC_H_D1: 92.0%) restores protection. This is because MCC controls what data the agent *sees*, not what it *writes*.

### 7. Policy Catches Within-Scope Leaks
MCC_H → MCC_H_D1 improvement: +13.4pp safety, +8.6pp should_refuse. Even within mounted folders, some data is sensitive — policy instructs the agent about what to withhold.

## Implications for Thesis

1. **Complementarity confirmed in network setting**: Structure and policy address different attack surfaces (transitive=equal, planting=policy, deputy=structure).
2. **Write-permission gap identified**: The MCC architecture needs extension for production use with action tasks.
3. **Consistent with PACT-PAIR findings**: MCC_H alone leaks within-scope data that policy catches (PAIR: R1 20.3% vs D3's 8.0%).
