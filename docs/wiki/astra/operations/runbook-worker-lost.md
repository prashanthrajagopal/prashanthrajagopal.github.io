---
title: "Runbook: Worker Lost"
tags:
  - astra
  - operations
  - runbook
  - workers
---

# Runbook: Worker Lost

**Alert:** Worker heartbeat not received within 30s. In-flight tasks may be stuck.

## Detection

1. Run `redis-cli GET worker:heartbeat:<worker_id>` to check the last recorded heartbeat timestamp.
2. Run `redis-cli XRANGE astra:worker:events - + COUNT 20` to review recent worker events from the stream.
3. Query Postgres to find tasks currently assigned to the lost worker: select `id`, `type`, `status`, and `updated_at` from `tasks` where `worker_id = '<worker_id>'` and `status = 'running'`.

## Containment

1. Move in-flight tasks back to queued status: issue `UPDATE tasks SET status='queued', worker_id=NULL, updated_at=now() WHERE worker_id='<worker_id>' AND status='running'` in Postgres.
2. The `worker-manager` service does this automatically — verify it ran by checking worker-manager logs for the message "re-queuing orphaned tasks". The scheduler will pick them up on its next 100ms tick.

## Remediation

For Kubernetes deployments, restart the worker pod with `kubectl rollout restart deployment/execution-worker -n workers`.

For native process deployments, run `./scripts/deploy.sh --restart execution-worker`.

## Verify recovery

1. Confirm tasks are re-queued and being processed: query Postgres for `SELECT status, count(*) FROM tasks WHERE updated_at > now() - interval '5 minutes' GROUP BY status`.
2. Confirm the new worker is heartbeating: run `redis-cli GET worker:heartbeat:<new_worker_id>`.

## Escalate if

- Multiple workers lost simultaneously (worker-manager crash? Redis issue?)
- Tasks not re-queued after 5 minutes (worker-manager health?)
- New worker fails to start (image issue? resource constraint?)

See [Runbook: High Error Rate](runbook-high-error-rate.md) if worker loss is causing cascading task failures.
