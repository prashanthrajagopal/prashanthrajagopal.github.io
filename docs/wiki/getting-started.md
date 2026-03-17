---
title: Site contributing
description: How to author and publish prashanthr.net
---

# Contributing to this site

This site is built with **Zensical** (MkDocs Material) and deploys from **GitHub Actions** on push to `main`.

## Directory layout

| Path | Purpose |
|------|---------|
| `docs/index.md` | Home page |
| `docs/blog/` | Blog posts under `posts/` |
| `docs/wiki/` | Wiki (Astra, Rails, Systems, Tools) |
| `docs/astra/` | Short Astra landing (nav entry) |
| `mkdocs.yml` | Site config, nav, theme |
| `docs/stylesheets/` | Custom CSS |
| `docs/javascripts/` | Custom JS |
| `.github/workflows/publish.yml` | Build + GitHub Pages |

## Frontmatter

```yaml
---
title: Page title
description: Optional SEO
tags:
  - tag1
---
```

Blog posts additionally need `date`, `authors`, `categories`, `draft`.

## Mermaid diagrams

Use a fenced block with language `mermaid`:

````markdown
```mermaid
flowchart LR
  A --> B
```
````

Prefer **flowchart**, **sequenceDiagram**, **stateDiagram-v2**, **erDiagram**. Avoid spaces in node IDs (use camelCase).

## Images

Static assets: place under `docs/` and reference with relative paths, e.g. `../assets/diagram.png` from a wiki page, or configure `extra` in `mkdocs.yml` if you add a dedicated assets dir.

## Preview & CI

- Local: `zensical serve`  
- CI: workflow runs `zensical build --clean`, adds `.nojekyll` and `CNAME`, uploads `site/`.

## Style

- **Headings:** sentence case or title case — stay consistent within a page.  
- **Spelling:** British or US — pick one per document.  
- **Links:** use relative paths within `docs/` so builds stay portable.

## Related

- [Zensical](tools/zensical.md)  
- [Wiki overview](index.md)
