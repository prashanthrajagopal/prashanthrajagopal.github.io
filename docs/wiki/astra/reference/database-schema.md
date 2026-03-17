---
title: Database Schema
tags:
  - astra
  - reference
  - database
  - postgres
---

# Database Schema

The **authoritative** database design — tables, migrations, indexes, and constraints — is **PRD §11** in the Astra repository. This page only sketches **relationships** for readers of the public wiki.

## Conceptual model

```mermaid
erDiagram
  agents ||--o{ goals : has
  agents ||--o{ memories : stores
  goals ||--o{ tasks : plans_to
  tasks ||--o{ task_dependencies : depends
```

Core ideas:

- **Agents** own **goals**; goals expand into **task graphs**.  
- **Tasks** link via **dependencies** forming a DAG.  
- **Events** record important lifecycle changes.  
- **Memories** store episodic/semantic content; **workers**, **usage**, and **documents** appear as in the PRD.

!!! note
    **No migration numbers, column lists, or SQL filenames** are published here. Contributors use the repo and PRD.
