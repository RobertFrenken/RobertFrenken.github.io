# RobertFrenken.github.io

Personal academic website built with Quarto.

## Tech Stack

- **Framework**: Quarto (website project)
- **CV**: Typst (standalone `.typ` file, compiled to PDF via pre-render)
- **Hosting**: GitHub Pages

## Key Files

| File | Purpose |
|------|---------|
| `cv.typ` | CV source (Typst) — single source of truth for resume |
| `Frenken_Robert_CV.pdf` | Compiled CV (generated, do not edit) |
| `_quarto.yml` | Site config, navbar, pre-render hook |
| `index.qmd` | Homepage |
| `research.qmd` | Research page |
| `posts.qmd` | Blog posts listing |

## CV Workflow

The CV is written in Typst for better editing experience (full LSP support via Tinymist extension).

**Edit**: `cv.typ` — Typst source with page setup, helpers, and content
**Compile**: `typst compile cv.typ Frenken_Robert_CV.pdf` (or via Quarto pre-render)
**Preview**: Use Tinymist extension's live preview, or compile manually

The `_quarto.yml` pre-render hook compiles the CV automatically during `quarto render`.

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

# Build entire site (includes CV via pre-render)
quarto render

# Preview site locally
quarto preview
```

## Dependencies

- Quarto (for site build)
- Typst (for CV compilation) — installed at `~/.local/bin/typst` on OSC
