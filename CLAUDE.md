# RobertFrenken.github.io

Personal academic website built with Quarto.

## Tech Stack

- **Framework**: Quarto (quarto.org) — Pandoc-based, multi-format publishing
- **CV**: Typst (standalone `.typ` file, compiled to PDF separately)
- **Hosting**: GitHub Pages (`quarto render` → static HTML)

## Key Files

| File | Purpose |
|------|---------|
| `_quarto.yml` | Project + website config, navbar, sidebar, theme |
| `cv/cv.typ` | CV source (Typst) — single source of truth for resume |
| `cv/Frenken_Robert_CV.pdf` | Compiled CV (generated, do not edit) |
| `cv/drafts/` | Gitignored — cover letters and application-specific drafts |
| `index.md` | Homepage |
| `research.md` | Research listing |
| `posts.md` | Blog posts listing (manual, pending listing page conversion) |
| `posts/` | Blog post sources and post-local data/assets |
| `_static/custom.css` | Custom styles (scarlet accent, Source Sans 3) |

## CV Workflow

The CV is written in Typst for better editing experience (full LSP support via Tinymist extension).

**Edit**: `cv/cv.typ` — Typst source with page setup, helpers, and content
**Compile**: `typst compile --root . cv/cv.typ cv/Frenken_Robert_CV.pdf` (the `--root .` flag lets Typst reach `images/icons/` at repo root)
**Preview**: Use Tinymist extension's live preview, or compile manually

CI compiles the CV in a separate step before `quarto render`, then copies the PDF into `_site/` so it serves at `/Frenken_Robert_CV.pdf`.

## CV Conventions

### Typst Syntax Notes
- `@` is a label reference in Typst — avoid using `@` in text (use "at" or omit)
- Links: `#link("url")[text]`
- Bold: `*text*` or `#text(weight: "bold")[text]`
- Italic: `_text_` or `#text(style: "italic")[text]`

### Current Formatting
- Page margins: 0.4in x, 0.35in y
- Base font: 10.5pt
- Section titles: 12pt bold, accent color (#bb0000)
- Entry titles: 10.5pt bold
- Secondary text (dates, orgs): 10pt italic

### Section Structure
1. Education (condensed — single school header, coursework inline)
2. Professional Experience (GRA combined with sub-entries for labs)
3. Publications
4. Projects (bulleted descriptions)
5. Technical Stack (layered grid: Applications → ML Pipeline → Data → Infrastructure → Languages)
6. Service & Mentorship

## Build Commands

```bash
# Compile CV only (run from repo root)
typst compile --root . cv/cv.typ cv/Frenken_Robert_CV.pdf

# Render entire site (output: _site/)
quarto render

# Preview site locally with live reload
quarto preview

# Full build (CV + site)
typst compile --root . cv/cv.typ cv/Frenken_Robert_CV.pdf && quarto render
```

## Dependencies

- Quarto 1.4+ (`~/.local/bin/quarto` on OSC)
- Typst (for CV compilation) — `~/.local/bin/typst` on OSC

## Quarto Conventions

### Syntax
- Pages stay `.md` (Quarto supports both `.md` and `.qmd`)
- Figures: `![Caption](path){#fig-label width=600 fig-alt="..."}` — `#fig-` prefix enables cross-refs as `@fig-label`
- Callouts: `::: {.callout-note collapse="true"}\n## Title\nbody\n:::` (also `callout-tip`, `callout-warning`, `callout-important`, `callout-caution`)
- Tabs: `::: {.panel-tabset}\n## Tab 1\n...\n## Tab 2\n...\n:::`
- Cross-references: `@fig-label`, `@sec-label`, `@tbl-label`
- Per-page front matter overrides project defaults (e.g. `format.html.toc: false` to drop the right-hand outline)

### Project Layout
- `_quarto.yml` allowlist: `*.md`, `*.qmd`, `!CLAUDE.md` — keeps project instructions out of the rendered site
- Resources copied as-is: `Frenken_Robert_CV.pdf`, `files/**` (PDFs), images via `images/`
- Theme: `light: cosmo, dark: darkly` — Bootstrap 5 base, dark-mode toggle built in
- Blog posts live under `posts/` as standalone `.qmd` or `.md` files
- Keep post-specific data files next to the post source when practical, using the same slug prefix
- Blog listing is still manual; add new post links to `posts.md`

### Known Gaps
- Blog listing is manual (no Quarto listing page yet — `posts.md` is hand-written)

## History

Reverted from MyST back to Quarto on 2026-05-08. Previously migrated Quarto → MyST on 2026-03-14 over parser-extensibility and React-SPA arguments; that experiment did not survive contact with myst-theme fork maintenance and the absence of a built-in blog. The `claude-code-power-users` post was deleted in the same change.
