---
title: Scheduler
tags:
  - astra
  - architecture
  - scheduler
  - distributed-systems
---

# Scheduler

The scheduler is the bridge between the task graph (Postgres) and the worker pool (Redis Streams). It runs on a 100ms tick loop, detects tasks whose dependencies have completed, and dispatches them to the appropriate shard stream.

## Algorithm

1. **Detect ready tasks** — query Postgres for tasks in `pending` where no incomplete dependency exists
2. **Mark atomically** — `UPDATE tasks SET status = 'queued'` in the same transaction as the read
3. **Push to shard stream** — `XADD astra:tasks:shard:<n>` with task metadata
4. **Workers pull** — consumer groups on the shard stream, claim and mark `status = 'scheduled'`
5. **Worker executes** — emits `TaskStarted` event, sends periodic heartbeat
6. **On completion** — `CompleteTask` writes result, emits `TaskCompleted`, scheduler unlocks children

## Ready-task detection query

The scheduler queries tasks with `status = 'pending'` where no dependency row exists with a `depends_on` task in a non-`completed` status, using `FOR UPDATE SKIP LOCKED` with a `LIMIT 100`. This allows multiple scheduler instances to run concurrently without contention: each instance locks only the rows it claims, and other instances skip locked rows to claim others. See `internal/scheduler/scheduler.go` in the Astra repo.

`FOR UPDATE SKIP LOCKED` is the key: multiple scheduler instances can run this query concurrently without contention. Each instance locks only the rows it claims; other instances skip locked rows and claim others. This is Postgres's advisory lock mechanism applied to distributed scheduling.

## Sharding

- Shard key: `hash(agent_id) % shard_count` or `hash(graph_id) % shard_count`
- Each scheduler instance owns a subset of shards (assignment persisted in Postgres)
- Consistent hashing for rebalancing when scheduler instances scale
- Stream names: `astra:tasks:shard:0`, `astra:tasks:shard:1`, ... `astra:tasks:shard:N`

!!! warning "Tradeoff"
    Shard-based scheduling pins tasks from the same graph/agent to the same shard. This avoids cross-shard coordination but can create hotspots when a single large graph dominates. Hotspot detection and dynamic rebalancing are not yet implemented.

## Reference implementation

The `Scheduler` struct in `internal/scheduler/scheduler.go` holds a `*sql.DB` and a `*messaging.Bus`. The `Run` method starts a `time.NewTicker` at 100ms and calls an internal `tick` method on each interval, returning when the context is cancelled. See `internal/scheduler/scheduler.go` in the Astra repo.

The 100ms tick is a pragmatic choice. Finer-grained polling (10ms) would reduce task scheduling latency but increase Postgres read pressure. The 100ms tick means median scheduling latency is ~50ms, with p95 ≤ 500ms — within the SLA.

## Worker heartbeats and failure detection

- Workers send heartbeats every **10s** to `astra:worker:events` stream
- If no heartbeat within **30s**, the scheduler marks all in-flight tasks as `queued` and re-pushes them
- Tasks exceeding `max_retries` move to dead-letter

To check worker liveness, run `redis-cli GET worker:heartbeat:<worker_id>` to retrieve the last heartbeat timestamp. To reclaim orphaned tasks after a worker loss, issue `UPDATE tasks SET status = 'queued', updated_at = now() WHERE worker_id = $1 AND status = 'running'` in Postgres.

See [Runbook: Worker Lost](../operations/runbook-worker-lost.md) for the full recovery procedure.
