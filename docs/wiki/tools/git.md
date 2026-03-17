---
title: Git workflow
---

# Git workflow

- **Branches:** `main` is deployable for this site; use feature branches for large edits.  
- **Commits:** Prefer focused commits with clear subjects; body optional for *why* when non-obvious.  
- **PRs:** Describe scope; link issues if any. For wiki-only changes, a short summary is enough.  
- **Rebase vs merge:** Project preference wins; keep history readable on `main`.

For Astra, follow repo rules: PRD updates with architectural changes, `go vet` / lint clean.
