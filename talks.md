---
title: Talks
---

Conference talks, invited lectures, and class presentations. Slide decks are built with [Slidev](https://sli.dev/) and deployed as standalone static sites. Each entry below links to the live deck and to a landing page with context, references, and recording (where available).

## Upcoming

*No upcoming talks scheduled.*

## 2026

- **[Mamba: Linear-Time Sequence Modeling with Selective State Spaces](talks/cse5469-mamba.md)** (May 1, 2026)
  Paper presentation for CSE 5469 on Gu & Dao (COLM 2024) — selective state spaces with hardware-aware parallel scan for linear-time sequence modeling.

- **[Do I Know This Entity? Knowledge Awareness and Hallucinations in Language Models](talks/cse5469-entity-hallucinations.md)** (Feb 11, 2026)
  Paper presentation for CSE 5469 on Ferrando et al. (ICLR 2025) — SAE steering reveals causal directions for entity recognition in language models.

---

::: {.callout-note collapse="true"}
## Talk-entry convention

Each talk lives at `talks/<slug>.md` with the structure below. Slidev decks live in a single [**`presentations/`**](https://github.com/RobertFrenken/presentations) monorepo — each deck is a subdirectory, shared styling and Vue components live in `shared/` as a Slidev addon, and each deck deploys to its own sub-path on GitHub Pages under `robertfrenken.github.io/presentations/<deck>/`.

```markdown
---
title: <Full talk title>
subtitle: <Optional subtitle>
date: YYYY-MM-DD
---

**Venue:** <Course / conference / seminar>
**Duration:** <N minutes>
**Slides:** [Live deck](https://robertfrenken.github.io/<repo-name>/<deck-slug>/) · [Source](https://github.com/RobertFrenken/<repo-name>/tree/main/<deck-slug>) · [PDF](./<slug>.pdf)
**Recording:** <YouTube / Zoom link if public>

## Abstract

<1–2 paragraphs summarizing the talk>

## Embedded Deck

<iframe src="https://robertfrenken.github.io/<repo-name>/<deck-slug>/"
        width="100%" height="500" frameborder="0"
        allowfullscreen></iframe>

## References

- <Paper or repo links cited in the talk>
```

**Thumbnails:** save a 16:9 screenshot of the title slide as `talks/<slug>-thumb.png` and reference it in the talk entry's frontmatter (`thumbnail: talks/<slug>-thumb.png`).

**Why a separate monorepo (not this repo)?** Slidev's Vite build doesn't play well inside MyST's build pipeline. Keeping decks in a separate repo isolates tooling and keeps the main site's build fast. Bundling all talks into one monorepo (instead of per-talk repos) lets shared styling, layouts, and reusable Vue components (e.g. an attention visualizer that gets reused across multiple talks) live in `shared/` as a Slidev addon and be pulled into every deck via `addons: [../shared]` in the deck's frontmatter.

**New-deck checklist:** mkdir `<deck-slug>/` in the presentations repo, create `slides.md` with `addons: [../shared]` + `theme: academic`, add build/dev/export scripts to the root `package.json`, register the deck in `scripts/write-index.mjs`, then add a `talks/<slug>.md` entry here pointing at the deployed URL.
:::
