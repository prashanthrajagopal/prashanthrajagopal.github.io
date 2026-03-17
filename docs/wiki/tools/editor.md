---
title: Editor & IDE
---

# Editor & IDE

**VS Code / Cursor** is the default assumption. Useful setup:

- **Go:** `gopls`, format on save with `goimports` or `gofumpt`.  
- **Markdown:** spell check; preview for wiki pages.  
- **YAML:** schema validation for workflows and Helm when editing Astra deploy charts.  
- **Protobuf:** Buf extension or equivalent for `.proto` in the Astra repo.

Keep **tab width consistent** with each project (Go: tabs as spaces, 4 or 8 per team norm). For this site, follow existing Markdown style: ATX headings, fenced code blocks with language tags.
