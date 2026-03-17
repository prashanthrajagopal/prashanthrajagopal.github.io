---
title: Getting Started
tags:
  - setup
  - reference
---

# Getting Started

## Local Development

```bash
# Install
pip install zensical

# Serve with live reload
zensical serve

# Build static site
zensical build
```

## Writing Content

- **Blog posts** go in `docs/blog/posts/` with a date in the frontmatter
- **Wiki pages** go in `docs/wiki/`

### Blog post frontmatter

```yaml
---
title: My Post Title
date: 2026-01-15
authors:
  - your-name
categories:
  - Category
tags:
  - tag1
  - tag2
draft: false
---
```

### Wiki page frontmatter

```yaml
---
title: Page Title
tags:
  - topic
---
```

## Deployment

The site deploys automatically to GitHub Pages via the `publish` workflow when you push to `main`.
