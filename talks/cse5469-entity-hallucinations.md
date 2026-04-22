---
title: "Do I Know This Entity? Knowledge Awareness and Hallucinations in Language Models"
subtitle: Paper presentation for CSE 5469
date: 2026-02-11
---

**Venue:** CSE 5469 — Ohio State University
**Duration:** 25 minutes
**Slide source:** [GitHub — CSE-5469-lecture-slides](https://github.com/RobertFrenken/CSE-5469-lecture-slides) (archived, Slidev format)
**Paper:** Ferrando, J., Obeso, O., Rajamanoharan, S., & Nanda, N. (2025). *Do I Know This Entity? Knowledge Awareness and Hallucinations in Language Models.* ICLR 2025.

## Abstract

Ferrando et al. use sparse autoencoders (SAEs) to identify directions in Gemma 2's residual stream that causally control whether the model recognizes an entity. Activating the "known entity" latent on an *unknown* entity makes the model confidently fabricate facts; activating the "unknown" latent on a *known* entity makes the model refuse to answer. Most strikingly, SAEs trained on the base (pre-training) model transfer to the chat (RLHF'd) model — suggesting refusal behavior was repurposed from pre-existing entity recognition representations rather than created fresh during fine-tuning.

This presentation walks through the SAE methodology (JumpReLU, separation score, MaxMin selection), the core steering experiments, the attention-gating mechanism that implements the switch, and a critical analysis of the paper's open questions (steering magnitude, scaling behavior, scope of tested entity types, and whether "self-knowledge" overstates what's actually a pattern-familiarity signal).

## References

- Ferrando et al. (2025). [*Do I Know This Entity?*](https://arxiv.org/abs/2411.14257) ICLR.
- Meng et al. (2022). *Locating and Editing Factual Associations in GPT.* NeurIPS.
- Nanda et al. (2023). *Attribution Patching: Activation Patching at Industrial Scale.*
