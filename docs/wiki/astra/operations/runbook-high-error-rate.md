---
title: "Runbook — High Error Rate"
tags:
  - astra
  - operations
  - runbook
---

# Runbook — High error rate

**Trigger:** Task **failure rate** or **error budget** burn above threshold (per monitoring).

## Symptoms

- Spike in **failed** tasks or **retry** storms.  
- User-visible **timeouts** or partial goal completion.  
- Correlation with a **deploy** or **dependency** outage.

## What operators do (summary)

1. **Triage:** which **task types**, **workers**, or **regions** are affected.  
2. **Check** recent **releases** — roll back if a bad deploy is likely (**internal procedure**).  
3. **Inspect** downstreams: **LLM provider**, **sandbox**, **browser worker**, **database** health.  
4. **Re-queue** transient failures only after root cause is understood — steps live in **private** runbooks.  
5. **Communicate** severity per [Operations index](index.md).
