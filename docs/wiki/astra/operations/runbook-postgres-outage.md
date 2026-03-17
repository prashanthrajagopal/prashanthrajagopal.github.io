---
title: "Runbook — Postgres Outage"
tags:
  - astra
  - operations
  - runbook
  - postgres
---

# Runbook — Postgres outage

**Trigger:** Widespread **database connectivity** errors; control plane and workers cannot persist state.

## Symptoms

- Health checks fail across **kernel** and **worker** tiers.  
- APIs return **5xx**; scheduling and task completion stop.  
- Dashboards show **DB down** or connection pool exhaustion.

## Impact

**Severe:** the system cannot **commit** task or agent state until the database is reachable or a **replica** is promoted.

## What operators do (summary)

1. **Confirm** primary vs replica status with your **DBA / cloud console**.  
2. **Fail over** to a healthy instance per your **provider runbook**.  
3. **Update connection config** for all dependent services and **roll** restarts in a controlled order (**internal playbook**).  
4. **Verify** writes and reads; watch **event backlog** if any async consumers lagged.  
5. **Post-incident:** replication lag, data window, and whether **event log** replay is needed — documented in **private** runbooks.

!!! note
    **No SQL, kubectl, or psql recipes** on this public wiki.
