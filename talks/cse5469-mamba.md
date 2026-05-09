---
title: "Mamba: Linear-Time Sequence Modeling with Selective State Spaces"
subtitle: Paper presentation for CSE 5469
date: 2026-05-01
---

**Venue:** CSE 5469 — Ohio State University
**Duration:** 25 minutes
**Slides:** [Live deck](https://robertfrenken.github.io/presentations/mamba/) · [Source](https://github.com/RobertFrenken/presentations/tree/main/decks/mamba)
**Paper:** Gu, A., & Dao, T. (2024). *Mamba: Linear-Time Sequence Modeling with Selective State Spaces.* COLM 2024.

## Abstract

Gu & Dao introduce Mamba, a selective state space model (SSM) that matches or exceeds Transformer quality on language tasks while scaling linearly in sequence length rather than quadratically. The key insight is *input-dependent* state transitions: unlike prior SSMs (S4, H3) whose transition matrices are fixed at inference time, Mamba gates the SSM parameters as functions of the current token, giving the model content-aware memory selection analogous to attention — but without the full key-value product.

This presentation covers the structured state space foundation, the selectivity mechanism and why it breaks the convolutional view that makes prior SSMs fast, the hardware-aware parallel scan that recovers efficiency in spite of this, and a critical read of the empirical claims: where the linear-time scaling genuinely matters, where Transformers remain competitive, and what the architecture leaves open for follow-up work (Mamba-2, hybrid models).

## References

- Gu & Dao (2024). [*Mamba: Linear-Time Sequence Modeling with Selective State Spaces.*](https://arxiv.org/abs/2312.00752) COLM.
- Gu et al. (2022). [*Efficiently Modeling Long Sequences with Structured State Spaces.*](https://arxiv.org/abs/2111.00396) ICLR.
- Dao & Gu (2024). [*Transformers are SSMs: Generalized Models and Efficient Algorithms through Structured State Space Duality.*](https://arxiv.org/abs/2405.21060) ICML.
