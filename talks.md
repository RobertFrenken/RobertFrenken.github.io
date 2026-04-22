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

Each talk lives at `talks/<slug>.md` with the structure below. The Slidev deck itself lives in its own repo and deploys to GitHub Pages at `robertfrenken.github.io/<repo-name>/`, then is embedded or linked here. Repo naming is flexible — `CSE-5469-lecture-slides` (course-coded) or `talks-<topic>` both work.

```markdown
---
title: <Full talk title>
subtitle: <Optional subtitle>
date: YYYY-MM-DD
---

**Venue:** <Course / conference / seminar>
**Duration:** <N minutes>
**Slides:** [Live deck](https://robertfrenken.github.io/<repo-name>/) · [Source](https://github.com/RobertFrenken/<repo-name>) · [PDF](./<slug>.pdf)
**Recording:** <YouTube / Zoom link if public>

## Abstract

<1–2 paragraphs summarizing the talk>

## Embedded Deck

<iframe src="https://robertfrenken.github.io/<repo-name>/"
        width="100%" height="500" frameborder="0"
        allowfullscreen></iframe>

## References

- <Paper or repo links cited in the talk>
```

**Thumbnails:** save a 16:9 screenshot of the title slide as `talks/<slug>-thumb.png` and reference it in the talk entry's frontmatter (`thumbnail: talks/<slug>-thumb.png`).

**Why external Slidev repos?** Slidev's Vite build doesn't play well inside MyST's build pipeline. Keeping each deck as its own repo isolates tooling, gives each talk a clean deploy URL, and means the main site's build stays fast.
:::
