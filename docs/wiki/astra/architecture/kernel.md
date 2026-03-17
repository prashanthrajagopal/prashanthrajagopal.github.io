---
title: Kernel Design
tags:
  - astra
  - architecture
  - kernel
---

# Kernel Design

The Astra kernel is intentionally minimal. It does exactly four things and refuses to do anything else. This constraint is not a limitation — it's what makes the system composable.

## Responsibilities

1. **Actor Runtime** — run millions of actors efficiently (goroutine-per-actor, mailbox model)
2. **Task Graph Engine** — persist and coordinate DAGs, dependency resolution, partial execution
3. **Scheduler** — shard-aware distributed scheduler, capability matching, priority
4. **Message Bus** — Redis Streams + local in-memory mailboxes
5. **State Manager** — transactional persistence in Postgres, event sourcing, snapshots

## Kernel invariants

- Kernel must remain small and stable. Adding features to the kernel requires explicit architectural justification.
- All non-kernel services run in user-space (SDK/services). They interact with the kernel only via its published gRPC API.
- Kernel guarantees: message delivery within configured SLAs, consistent task state, transactionally consistent state writes.
- Kernel packages (`internal/actors`, `internal/kernel`, `internal/tasks`, `internal/scheduler`, `internal/messaging`, `internal/events`) must not import service-layer packages.

## Kernel gRPC API

Defined in `proto/kernel.proto` (`astra.kernel.KernelService`):

| RPC | Input | Output | Description |
|---|---|---|---|
| `SpawnActor` | `actor_type`, `config` | `ActorID` | Create and start a new actor goroutine |
| `SendMessage` | `actorID`, `Message` | `ack` | Deliver message to actor mailbox |
| `CreateTask` | `task_spec` | `TaskID` | Create task node in a graph |
| `ScheduleTask` | `taskID` | `ack` | Mark task ready, push to worker queue |
| `CompleteTask` | `taskID`, `result` | `ack` | Mark task completed, store result, unlock children |
| `FailTask` | `taskID`, `error` | `ack` | Mark task failed, increment retries or dead-letter |
| `QueryState` | `entity`, `filters` | `state` | Query entity state (agents, tasks, workers) |
| `SubscribeStream` | `stream`, `consumer_group` | stream `Event` | Subscribe to Redis stream |
| `PublishEvent` | `event` | `ack` | Publish event to a stream |

## Kernel manager implementation

The `Kernel` struct in `internal/kernel/kernel.go` holds a `sync.RWMutex`-protected map of actor IDs to `Actor` instances. The `Spawn` method acquires a write lock and registers a new actor in the map. The `Send` method acquires a read lock, looks up the target actor by ID, and calls `Receive` on it. If the actor is not found, `Send` returns an error. See `internal/kernel/kernel.go` in the Astra repo.

The kernel is a registry and a dispatcher. It doesn't know what actors do; it just knows where they are.

!!! note "Design note"
    The kernel manager uses a `sync.RWMutex` rather than a channel-based dispatcher. This is a deliberate choice: a mutex gives O(1) actor lookup with negligible contention at normal read rates (most operations are reads). A channel-based dispatcher would add a goroutine per send and create a bottleneck at high message rates.

!!! question "Open"
    At millions of actors, the single `actors` map will become a bottleneck even with RWMutex. Sharded kernel instances (one per CPU or per shard) are the likely solution. Not yet designed.
