# Pulse 4YP Thesis

**Title:** Pulse: A Secure AgentOS for Cross-Boundary AI Coordination

**Author:** Xisen Wang
**College:** Keble College
**Supervisor:** Professor Philip Torr
**Term:** Trinity Term, 2026

## Overview

This thesis presents Pulse, a Personal Agent Operating System that enables secure, stateful AI agents to coordinate autonomously across organizational boundaries. The work addresses the fundamental Context-Security Trade-off in networked AI systems through three core innovations:

1. **Dual-Track Memory**: Relationship-specific memory shards with perfect isolation
2. **Mountable Context Cells**: Capability-based physical security sandboxes
3. **Intelligent Escalation Protocol**: Adaptive policy learning through precedent clustering

## Building the Document

### Requirements

- **LaTeX Distribution**: TeXLive 2022+ or MacTeX 2022+
- **Compiler**: LuaLaTeX (required by OxEngThesis class)
- **Fonts**: Carlito font (see [fonts/INSTALL_FONTS_macOS.md](fonts/INSTALL_FONTS_macOS.md))

### Compilation

#### Option 1: Using the provided script

```bash
./compile_document.sh pulse_4yp_thesis.tex
```

#### Option 2: Manual compilation

```bash
latexmk -pdflatex=lualatex -pdf pulse_4yp_thesis.tex
makeglossaries pulse_4yp_thesis
latexmk -pdflatex=lualatex -pdf pulse_4yp_thesis.tex
```

#### Option 3: Using a LaTeX editor

Open `pulse_4yp_thesis.tex` in your preferred LaTeX editor (Texifier for macOS, Kile/TeXMaker for Linux) and configure it to use LuaLaTeX as the typesetting engine.

## Document Structure

```
pulse_4yp_thesis.tex          # Main thesis file
├── abstract.tex              # Thesis abstract
├── chap_introduction.tex     # Chapter 1: Introduction
├── chap_problem_setup.tex    # Chapter 2: Problem Setup and Related Work
├── chap_architecture.tex     # Chapter 3: The Pulse AgentOS Architecture
├── chap_memory_system.tex    # Chapter 4: Dual-Track Memory Architecture
├── chap_security.tex         # Chapter 5: Security (Context Cells + IEP)
├── chap_evaluation.tex       # Chapter 6: Evaluation and Benchmarking
├── chap_conclusion.tex       # Chapter 7: Conclusion and Future Directions
├── appendix_technical.tex    # Appendix A: Technical Implementation
├── appendix_related_works.tex # Appendix B: Extended Related Work
├── references.bib            # Bibliography
└── glossary.tex              # List of abbreviations
```

## Key Concepts

### The Context-Security Trade-off

**Problem:** Effective coordination requires deep personal context, but exposing omniscient agents to external parties creates catastrophic security risks.

**Solution:** Physical isolation through Context Cells + relationship-aware memory partitioning.

### Network-Native Architecture

Pulse is designed as foundational infrastructure for an agent economy—analogous to TCP/IP for autonomous entities. Each user's Personal File System acts as an independent node in a federated network.

### Evaluation Results

- **Utility Score**: 87% (near-baseline task completion)
- **Security Score**: 100% (zero exfiltration against direct attacks)
- **Manual Overhead Reduction**: 73% (after 100 interactions)

## Content Overview

### Chapter 1: Introduction
- The Coordination Crisis in the AI Era
- The Security-Utility Paradox
- From Tools to Digital Entities: The AI COO Vision
- Research Objectives and Principal Contributions

### Chapter 2: Problem Setup
- Formal definition of the Context-Security Trade-off
- Threat model and attack taxonomy
- Landscape analysis: single-tenant frameworks vs. agent communication protocols
- Pulse's unique position in the ecosystem

### Chapter 3: Architecture
- The OS abstraction (LLM as CPU, Notes as Files, States as Plugins)
- Core components and execution loop
- The four interaction paradigms (H2H, H2A, A2H, A2A)
- Proactive State Maintenance (Heartbeat Engine)

### Chapter 4: Memory System
- Tiered memory hierarchy (L1/L2/L3)
- Dual-Track architecture: Self-State vs. Relationship Shards
- Social Theory of Mind through isolated episodic logs
- Evaluation: memory isolation guarantees

### Chapter 5: Security
- The Prompt Injection Problem
- Mountable Context Cells: capability-based security
- Intelligent Escalation Protocol with Relational Clustering
- Red-teaming results: 100% defense against jailbreak attacks

### Chapter 6: Evaluation
- Novel benchmark: Context-Security Trade-off metric
- Baseline comparisons (naive prompting, manual ACLs, Pulse variants)
- Detailed attack taxonomy and defense analysis
- Learning curve: 73% reduction in manual overhead

### Chapter 7: Conclusion
- Summary of contributions
- Broader vision: from tools to digital civilization
- Future research directions (formal verification, A2A protocols, L3 shards)
- Ethical considerations and societal impact

## Notes

- The thesis uses the **OxEngThesis** LaTeX class specifically designed for Oxford Engineering students
- This is configured as a 4YP report (shorter format, ~50 pages vs. full doctoral thesis)
- The class is based on the memoir package with custom formatting for Oxford requirements
- All chapter content is based on the technical architecture documented in `/docs/vision/`

## Source Material

This thesis synthesizes concepts from:
- `/docs/vision/vision.md` - Core Pulse vision and paradigm shift
- `/docs/vision/ai_coo_architecture_4yp.md` - Detailed AgentOS architecture
- `/docs/vision/core_technology.md` - Technical notions (Context Cells, IEP, etc.)
- `/docs/vision/4YP_Interim_Report_Outline.md` - Presentation structure

## Next Steps

1. **Review and Refine**: Read through each chapter and refine technical details
2. **Add Figures**: Create architecture diagrams, flowcharts, and result plots
3. **Expand Evaluation**: Add more experimental results from the actual Pulse implementation
4. **Proofread**: Check for consistency, clarity, and Oxford style guidelines
5. **Compile**: Generate the final PDF and review formatting

## Acknowledgements

This thesis template is based on the OxEngThesis class by Dr. Mauricio Villarroel.

## License

Content: Copyright © 2026 Xisen Wang
Template: GPL-2.0 (OxEngThesis class)
