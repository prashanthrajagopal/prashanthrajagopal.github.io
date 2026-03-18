---
title: Zensical (this site)
---

# Zensical

[Zensical](https://zensical.org/) builds this site — a MkDocs + Material stack.

```bash
pip install zensical pyyaml
python scripts/sync_latest_blog.py   # homepage “Latest” = newest post by date
zensical serve    # live reload at http://127.0.0.1:8000
zensical build --clean   # output in site/
python scripts/generate_sitemap.py   # site/sitemap.xml + robots.txt
```

**Sitemap:** After each full build, run `scripts/generate_sitemap.py` so crawlers get `https://prashanthr.net/sitemap.xml` and `robots.txt` (CI does this automatically).

**Homepage blog card:** `scripts/sync_latest_blog.py` updates `docs/index.md` between `LATEST_BLOG_AUTOGEN` markers from the latest `docs/blog/posts/*.md` (by frontmatter `date:`). GitHub Actions runs this before every deploy.

- **Config:** root `mkdocs.yml` — `docs_dir: docs`, nav, theme, **Mermaid** via `pymdownx.superfences` custom fence `mermaid`.  
- **Content:** `docs/wiki/`, `docs/blog/`, `docs/index.md`.  
- **Diagrams:** fenced block with ` ```mermaid ` — flowchart, sequenceDiagram, stateDiagram-v2, erDiagram.  
- **CI:** GitHub Actions uploads `site/` to Pages (see `.github/workflows/publish.yml`).
