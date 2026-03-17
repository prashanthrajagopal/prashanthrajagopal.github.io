---
title: Local Development
tags:
  - astra
  - deployment
  - local
---

# Local development

Typical local setup: **infrastructure** (database, Redis, cache, object storage) in **containers**, **services** as **native processes** for fast iteration. **Exact commands, scripts, ports, and env vars** are maintained **only in the Astra repository** — not duplicated here.

## Expectations

- You need **compatible Go**, **container runtime**, and **provider keys** if you call external LLMs.  
- **Migrations** must be applied before services start.  
- A **validation** or **health** checklist exists in-repo after changes.

## Dashboard

An operator **dashboard** is available in local setups when the gateway is running; URL and credentials are **deployment-specific** (see PRD / repo docs).

!!! note
    **No copy-paste commands** on this public wiki.
