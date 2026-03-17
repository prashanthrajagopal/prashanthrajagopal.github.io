---
title: "Runbook — Worker Lost"
tags:
  - astra
  - operations
  - runbook
  - workers
---

# Runbook — Worker lost

**Trigger:** Worker **heartbeat** missing beyond the platform timeout (see **PRD**). In-flight work may stall until **re-queued**.

## Symptoms

- Elevated **task run time** or tasks stuck **in progress**.  
- Alerts on **worker liveness** or **queue depth**.  
- Partial platform degradation if many workers drop.

## Impact

Work assigned to **lost workers** is delayed until the platform **re-queues** it. **Committed** task state in the database is not discarded by worker loss alone.

## What operators do (summary)

1. **Confirm** which workers or pools are unhealthy (dashboards / health checks).  
2. **Contain:** ensure **orphaned in-flight tasks** are returned to a **runnable** state per **internal runbook** in the Astra repo.  
3. **Remediate:** **restart** or **replace** worker processes / pods.  
4. **Verify:** task completion rate and heartbeats return to normal.  
5. **Escalate** if many workers fail together (possible **messaging** or **control plane** issue).

!!! note
    **Exact commands** (CLI, SQL, deployment names) are **not** published on this wiki — use the **private** `docs/runbooks/` material in the Astra repository.

See [High error rate](runbook-high-error-rate.md) if failures cascade.
