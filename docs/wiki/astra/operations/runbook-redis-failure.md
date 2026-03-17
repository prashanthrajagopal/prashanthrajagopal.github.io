---
title: "Runbook — Redis Failure"
tags:
  - astra
  - operations
  - redis
---

# Runbook — Redis failure

**Trigger:** **Redis** unreachable or read-only; **streams** or **caches** fail.

## Impact (conceptual)

**Dispatch** and **worker coordination** degrade; **cached reads** may error or miss. **Durable** task rows in **Postgres** are not wiped by Redis loss alone, but **in-flight dispatch** and **locks** are affected.

## What operators do (summary)

1. **Scope** the outage (single node vs cluster).  
2. **Fail over** or **restore** Redis per **provider / platform** runbook.  
3. **Restart** schedulers and workers in a safe order after Redis is healthy.  
4. **Watch** queue depth and **cache stampede** on recovery.  
5. **Escalate** to platform SRE for **SEV1** scope.

!!! note
    **Key names, stream names, and CLI commands** are omitted here; use **private** documentation.

See [Redis keys reference](../reference/redis-keys.md) at a **conceptual** level only.
