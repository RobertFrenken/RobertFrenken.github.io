# RobertFrenken.github.io

Personal academic website built with MyST.

## Tech Stack

- **Framework**: MyST (mystmd.org) — Jupyter ecosystem, unified.js AST
- **CV**: Typst (standalone `.typ` file, compiled to PDF separately)
- **Hosting**: GitHub Pages (React SPA via `myst build --html`)

## Key Files

| File | Purpose |
|------|---------|
| `myst.yml` | Project + site config, TOC, nav |
| `cv.typ` | CV source (Typst) — single source of truth for resume |
| `Frenken_Robert_CV.pdf` | Compiled CV (generated, do not edit) |
| `index.md` | Homepage |
| `research.md` | Research listing |
| `posts.md` | Blog posts listing (manual, pending blog plugin) |
| `tooling.md` | Tooling dashboard (placeholder, pending OJS→Jupyter migration) |
| `_static/custom.css` | Custom styles (scarlet accent, Source Sans Pro) |

## CV Workflow

The CV is written in Typst for better editing experience (full LSP support via Tinymist extension).

**Edit**: `cv.typ` — Typst source with page setup, helpers, and content
**Compile**: `typst compile cv.typ Frenken_Robert_CV.pdf`
**Preview**: Use Tinymist extension's live preview, or compile manually

CI compiles the CV in a separate step before `myst build`.

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
# Compile CV only
typst compile cv.typ Frenken_Robert_CV.pdf

# Build entire site
myst build --html

# Preview site locally
myst start

# Full build (CV + site)
typst compile cv.typ Frenken_Robert_CV.pdf && myst build --html
```

## Dependencies

- Node.js v20+ (for MyST)
- MyST CLI (`npm install -g mystmd`)
- Typst (for CV compilation) — installed at `~/.local/bin/typst` on OSC

## MyST Conventions

### Syntax
- Directives: `:::{name}` (block-level extensions)
- Roles: `` {name}`content` `` (inline extensions)
- Cross-references: `[](#label)` or `@label`
- Figures: `:::{figure} path` with `:label:` option
- Admonitions: `:::{note}`, `:::{warning}`, etc.

### Known Gaps
- Blog listing is manual (no categories/RSS yet — see `~/plans/myst-blog-plugin.md`)
- Tooling page is a placeholder (OJS charts need migration to Jupyter)
- Only 2 built-in themes (book, article)

# currentDate
Today's date is 2026-03-14.
