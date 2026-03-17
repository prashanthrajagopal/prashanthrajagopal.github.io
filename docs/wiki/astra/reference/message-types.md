---
title: Message Types
tags:
  - astra
  - reference
  - messaging
  - events
---

# Message Types

All actor messages and stream events in Astra. Messages follow a standard envelope:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "TaskScheduled",
  "source": "scheduler-01",
  "target": "worker-pool",
  "payload": { "task_id": "...", "graph_id": "...", "priority": 100 },
  "meta": { "trace_id": "abc123" },
  "timestamp": "2026-03-18T10:30:00Z"
}
```

## Message type catalogue

| Category | Types |
|---|---|
| **Goal lifecycle** | `GoalCreated`, `PlanRequested`, `PlanGenerated` |
| **Task lifecycle** | `TaskCreated`, `TaskScheduled`, `TaskStarted`, `TaskCompleted`, `TaskFailed` |
| **Phase lifecycle** | `PhaseStarted`, `PhaseCompleted`, `PhaseFailed`, `PhaseSummary` |
| **LLM usage & audit** | `LLMUsage` (model, tokens in/out, latency, cost; persisted to `llm_usage` and `events`) |
| **Memory** | `MemoryWrite`, `MemoryRead` |
| **Tool execution** | `ToolExecutionRequested`, `ToolExecutionCompleted` |
| **Evaluation** | `EvaluationRequested`, `EvaluationCompleted` |
| **Agent lifecycle** | `AgentSpawned`, `AgentStopped`, `AgentError` |
| **Worker** | `WorkerHeartbeat`, `WorkerRegistered`, `WorkerDraining` |
| **Chat (WebSocket)** | `chunk`, `message_start`, `message_end`, `tool_call`, `tool_result`, `done`, `error`, `pong`, `session` |

## Stream schemas

### `astra:tasks:shard:<n>`

| Field | Type | Description |
|---|---|---|
| `task_id` | UUID | Task to execute |
| `graph_id` | UUID | Parent graph |
| `agent_id` | UUID | Owning agent |
| `task_type` | string | Task classifier |
| `payload` | JSON | Task payload (includes `agent_context` from Phase 9+) |
| `priority` | int | Scheduling priority (lower = higher priority) |
| `org_id` | UUID | Org scope (multi-tenancy) |
| `created_at` | RFC3339 | Creation timestamp |

### `astra:usage`

| Field | Type | Description |
|---|---|---|
| `request_id` | string | Unique per LLM request |
| `agent_id` | UUID | Requesting agent |
| `task_id` | UUID | Associated task |
| `org_id` | UUID | Org scope |
| `user_id` | UUID | User if request-triggered |
| `model` | string | Model identifier |
| `tokens_in` | int | Input tokens |
| `tokens_out` | int | Output tokens |
| `latency_ms` | int | LLM call latency |
| `cost_dollars` | decimal | Computed cost |
| `timestamp` | RFC3339 | Request timestamp |

Consumer: writes to `llm_usage` table + appends `LLMUsage` event to `events` table. Async — keeps hot path under 10ms.

### `astra:worker:events`

| Field | Type | Description |
|---|---|---|
| `worker_id` | UUID | Worker identity |
| `event_type` | string | `heartbeat`, `registered`, `draining`, `task_claimed`, `task_completed` |
| `task_id` | UUID | (for task events) |
| `metadata` | JSON | Additional context |
| `timestamp` | RFC3339 | Event timestamp |
