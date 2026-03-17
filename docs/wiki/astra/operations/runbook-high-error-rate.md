---
title: "Runbook: High Error Rate"
tags:
  - astra
  - operations
  - runbook
  - errors
---

# Runbook: High Error Rate

**Alert:** `HighTaskFailureRate` — >5% task failures over a 5-minute window.

## Triage

1. Sample recent failed tasks: query Postgres for `id`, `type`, `agent_id`, `payload->>'error'`, and `updated_at` from `tasks` where `status = 'failed'`, ordered by `updated_at DESC`, limited to 20 rows.
2. Check failure rate by task type: query Postgres grouping failed tasks from the last 10 minutes by `type` and ordering by failure count descending.

## Trace correlation

1. Find the `trace_id` for a specific failed task: query the `events` table for `payload->>'trace_id'` where `actor_id = '<task_id>'` and `event_type = 'TaskFailed'`.
2. Open the trace in Jaeger or Tempo using that trace ID.

## Contain

If failures are widespread and escalating, pause goal intake at the gateway using a feature flag or temporary config change. This stops new goals from generating new tasks while in-flight tasks continue processing.

If failures started after a recent deployment, check the rollout history with `kubectl rollout history deployment/execution-worker -n workers`. If a bad deploy is confirmed, roll it back with `kubectl rollout undo deployment/execution-worker -n workers`.

## Common causes

| Symptom | Likely cause |
|---|---|
| Failures concentrated on one task type | Bug in task handler for that type |
| All failures from one agent | Bad agent config or system_prompt |
| Failures started after deploy | Code regression |
| Failures on `tool_execution` tasks | Tool runtime issue — see tool-runtime logs |
| LLM-related failures | LLM provider down or rate limited — check `astra:usage` stream backup |
| Failures on all tasks from same graph | Planner generated a broken DAG |

## Remediation

Fix the root cause first. Then re-queue failed tasks if the failures were transient: issue `UPDATE tasks SET status='queued', retries=retries+1, updated_at=now() WHERE status='failed' AND retries < max_retries AND updated_at > now() - interval '1 hour'` in Postgres.

!!! warning
    Don't bulk-retry failed tasks without understanding the root cause. If the cause is still active, you'll generate another wave of failures and potentially hit rate limits or exhaust budgets.
