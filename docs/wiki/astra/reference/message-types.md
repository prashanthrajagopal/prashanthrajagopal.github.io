---
title: Message Types
tags:
  - astra
  - reference
  - messaging
  - events
---

# Message Types

Messages carry **type**, **source**, **target**, **payload**, and **metadata** (e.g. trace correlation). **PRD §12** defines categories and payloads in full.

## Event bus vs streams

**Durable audit** for many lifecycle events lives in the **database event log**. **Redis streams** carry **operational** traffic: dispatch, worker signals, async usage recording. Encoding (JSON vs binary) is an implementation detail.

**Partitioning:** dispatch traffic is **sharded** so no single stream becomes the only scalability bottleneck.

**Multi-tenancy:** all streams carry `org_id` in the payload when available.

## Event types

### Task lifecycle

| Type | Description |
|------|-------------|
| `TaskScheduled` | Task added to ready queue |
| `TaskStarted` | Worker claimed and began execution |
| `TaskCompleted` | Worker returned success result |
| `TaskFailed` | Worker returned failure or timed out |

### Phase lifecycle

| Type | Description |
|------|-------------|
| `PhaseStarted` | Execution phase began (e.g. planning, execution, review) |
| `PhaseCompleted` | Phase finished successfully |
| `PhaseFailed` | Phase ended in failure |
| `PhaseSummary` | Aggregate summary emitted at phase end |

### LLM audit

| Type | Description |
|------|-------------|
| `LLMUsage` | Per-request LLM audit record: `model`, `tokens_in`, `tokens_out`, `latency_ms`, `cost_dollars` |

### Worker

| Type | Description |
|------|-------------|
| `WorkerHeartbeat` | Liveness signal from worker |
| `WorkerRegistered` | Worker joined the pool |

### Goal

| Type | Description |
|------|-------------|
| `GoalCreated` | New goal submitted |
| `GoalCompleted` | Goal finished; emitted to `astra:goals:completed` for cascade tracking |

## Redis streams

| Stream | Purpose |
|--------|---------|
| `astra:tasks:<shard>` | Sharded task dispatch to workers |
| `astra:workers:heartbeat` | Worker liveness signals |
| `astra:dead_letter` | Tasks that exhausted all retries |
| `astra:usage` | Async LLM usage persistence fan-out (`request_id`, `agent_id`, `task_id`, `org_id`, `user_id`, `model`, `tokens_in`, `tokens_out`, `latency_ms`, `cost_dollars`, `timestamp`) |
| `astra:goals:completed` | `GoalCompleted` events for cascade / dependency tracking |
| `astra:slack:incoming` | Normalized Slack events from slack-adapter |
| `olympus:triggers:raw` | Normalized trigger events from webhook ingest |

Consumer groups process messages with **ack** semantics. Messages that exceed retry limits are moved to `astra:dead_letter`.
