---
title: Task Graph Engine
tags:
  - astra
  - architecture
  - tasks
  - dag
---

# Task Graph Engine

The task graph is Astra's unit of work. A `TaskGraph` is a DAG of `TaskNode`s, each representing an atomic unit of execution. Dependencies between tasks are explicit edges. The scheduler detects when a task's dependencies are complete and dispatches it.

## Go types

`internal/tasks/tasks.go` defines the core types. `Status` is a string type with constants for each lifecycle state: `created`, `pending`, `queued`, `scheduled`, `running`, `completed`, and `failed`. The `Task` struct holds ID, graph ID, goal ID, agent ID, type, status, JSONB payload, JSONB result, priority, retries, and max retries. `Dependency` records a `task_id`/`depends_on` pair. `Graph` holds an ID, a slice of tasks, and a slice of dependencies. See `internal/tasks/tasks.go` in the Astra repo.

## State machine

Tasks flow through the following states: `created` → `pending` → `queued` → `scheduled` → `running` → `completed`. From `running`, a task can also transition to `failed`, after which it either retries (returning to `queued`) or moves to dead-letter if retries are exhausted.

| Transition | Trigger |
|---|---|
| `created` → `pending` | Task added to graph, waiting for dependencies |
| `pending` → `queued` | All dependencies completed, task is ready |
| `queued` → `scheduled` | Scheduler assigned task to a worker |
| `scheduled` → `running` | Worker started execution |
| `running` → `completed` | Worker finished successfully |
| `running` → `failed` | Worker reported error |
| `failed` → `queued` | Retry (if `retries < max_retries`) |
| `failed` → `dead-letter` | Exhausted retries |

## Transactional state transitions

Every state transition persists to Postgres in a transaction **and** appends to the `events` table in the same transaction. This is the event-sourcing backbone — if the transition commits, the event is durable. If either write fails, both roll back.

The `Transition` method in `internal/tasks/store.go` begins a transaction, issues `UPDATE tasks SET status = $1 WHERE id = $2 AND status = $3`, and checks that exactly one row was affected (returning `ErrInvalidTransition` if not). It then inserts a corresponding row into the `events` table and commits. See `internal/tasks/store.go` in the Astra repo.

The `WHERE status = $3` check in the UPDATE implements optimistic concurrency. If another process already transitioned the task, `rows_affected = 0` and `ErrInvalidTransition` is returned. No separate lock needed.

## Database tables

The `tasks` table stores each task with a UUID primary key, references to `graph_id`, `goal_id`, and `agent_id`, a `type` string, a `status` string (defaulting to `created`), JSONB `payload` and `result`, `priority`, `retries`, and `max_retries`. The `task_dependencies` table stores directed edges as `(task_id, depends_on)` pairs with a composite primary key. Both reference `migrations/0001` and `migrations/0002`. See `migrations/0001_core.sql` and `migrations/0002_task_dependencies.sql` in the Astra repo.

Indexes: `idx_tasks_status`, `idx_tasks_agent`, `idx_tasks_graph`, `idx_task_dep_task`, `idx_task_dep_dependson`.

!!! warning "Tradeoff"
    JSONB payloads give flexibility but sacrifice query-time type safety. Task `type` is a free-form string; there's no DB-level constraint on which types are valid. This is intentional — new task types should not require migrations. The tradeoff is that type validation is the caller's responsibility.
