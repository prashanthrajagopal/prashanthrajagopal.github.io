---
title: Zensical (this site)
---

# Zensical

[Zensical](https://zensical.org/) builds this site — a MkDocs + Material stack.

```bash
pip install zensical
zensical serve    # live reload at http://127.0.0.1:8000
zensical build --clean   # output in site/
```

- **Config:** root `mkdocs.yml` — `docs_dir: docs`, nav, theme, **Mermaid** via `pymdownx.superfences` custom fence `mermaid`.  
- **Content:** `docs/wiki/`, `docs/blog/`, `docs/index.md`.  
- **Diagrams:** fenced block with ` ```mermaid ` — flowchart, sequenceDiagram, stateDiagram-v2, erDiagram.  
- **CI:** GitHub Actions uploads `site/` to Pages (see `.github/workflows/publish.yml`).
