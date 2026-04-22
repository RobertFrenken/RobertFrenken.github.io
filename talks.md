---
title: Talks
---

Conference talks, invited lectures, and class presentations. Slide decks are built with [Slidev](https://sli.dev/) and deployed as standalone static sites. Each entry below links to the live deck and to a landing page with context, references, and recording (where available).

## Upcoming

*No upcoming talks scheduled.*

## 2026

- **[Do I Know This Entity? Knowledge Awareness and Hallucinations in Language Models](talks/cse5469-entity-hallucinations.md)** (Feb 11, 2026)
  Paper presentation for CSE 5469 on Ferrando et al. (ICLR 2025) — SAE steering reveals causal directions for entity recognition in language models.

---

:::{note} Talk-entry convention
:class: dropdown

Each talk lives at `talks/<slug>.md` with the structure below. Slidev decks live in a **course-coded monorepo** (one repo per course or talk series) — e.g. [`CSE-5469-lecture-slides`](https://github.com/RobertFrenken/CSE-5469-lecture-slides) — with each deck as a subdirectory and shared styling / Vue components promoted to a `shared/` Slidev addon. Each deck deploys to its own sub-path on GitHub Pages.

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

**Why a separate monorepo per course (not this repo)?** Slidev's Vite build doesn't play well inside MyST's build pipeline. Keeping decks in a separate repo isolates tooling and keeps the main site's build fast. Using one repo per course (instead of per-talk) lets shared styling, layouts, and reusable Vue components (e.g. an attention visualizer that gets used across multiple talks) live in `shared/` as a Slidev addon and be pulled into every deck via `addons: [../shared]` in the deck's frontmatter.

**New-deck checklist:** mkdir `<deck-slug>/` in the course repo, create `slides.md` with `addons: [../shared]` + `theme: academic`, add build/dev/export scripts to the root `package.json`, register the deck in the course repo's `scripts/write-index.mjs`, then add a `talks/<slug>.md` entry here pointing at the deployed URL.
:::
