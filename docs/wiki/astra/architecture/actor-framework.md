---
title: Actor Framework
tags:
  - astra
  - architecture
  - actors
  - concurrency
---

# Actor Framework

Astra's actor model is the concurrency primitive everything else builds on. Each actor is a goroutine with a mailbox. Actors communicate by message-passing, never by shared memory. This is the Erlang model — adapted to Go and to the constraint of running millions of actors on one platform.

## Core types

`internal/actors/actors.go` defines two core types. `Message` carries an ID, type, source, target, JSON payload, string metadata map, and timestamp. The `Actor` interface is minimal: implementors provide `ID()` (returns the actor's string identifier), `Receive(ctx, msg)` (the message handler), and `Stop()` (shutdown). See `internal/actors/actors.go` in the Astra repo.

The `Actor` interface is minimal by design. Implementors provide `ID()`, a message handler (`Receive`), and a shutdown method (`Stop`). Everything else — goroutine lifecycle, mailbox buffering, backpressure — is handled by `BaseActor`.

## BaseActor

`BaseActor` in `internal/actors/base.go` provides the standard goroutine-backed actor implementation. It holds an actor ID, a buffered message channel (mailbox of capacity 1024), a stop channel, and a `sync.WaitGroup`. `NewBaseActor` constructs it. `Start` launches the message loop in a goroutine, selecting between incoming messages and the stop signal. `Receive` is non-blocking: it attempts a channel send and returns `ErrMailboxFull` immediately if the mailbox is at capacity. `Stop` closes the stop channel and waits for the goroutine to exit. See `internal/actors/base.go` in the Astra repo.

!!! warning "Tradeoff"
    Mailbox capacity is fixed at 1024 messages. `Receive` is non-blocking and returns `ErrMailboxFull` if the mailbox is full. This means senders must handle backpressure — they cannot assume delivery. The alternative (blocking sends) risks deadlock and hidden latency in callers. We chose explicit failure over silent blocking.

## Actor communication

| Mode | Mechanism | Latency | When to use |
|---|---|---|---|
| Local | Direct channel send to in-process mailbox | ~1μs | Same-node actors |
| Cross-node | Publish via Redis Streams → kernel proxies `SendMessage` | ~1-5ms | Actors on different nodes |

Cross-node routing: the kernel maps actor ID to node location. If the target actor is not local, the kernel publishes to the actor's node via Redis Streams. The target node's kernel picks it up and delivers to the local mailbox.

## Supervision tree

The supervision hierarchy is structured as follows: a `SystemSupervisor` at the root owns one or more `AgentSupervisor` instances, each of which manages a `PlannerActor`, a `MemoryActor`, and an `ExecutorActor`.

Each actor tree has a supervisor that manages the lifecycle of its children. Supervisors implement restart policies:

| Policy | Behaviour |
|---|---|
| `RestartImmediate` | Restart child immediately on failure |
| `RestartBackoff` | Exponential backoff: 100ms → 200ms → ... → 30s cap |
| `Escalate` | Propagate failure to parent supervisor |
| `Terminate` | Stop child permanently |

Circuit breaker: if a child exceeds `maxRestarts` within a sliding time window, the supervisor escalates or terminates rather than entering a restart storm.

This is OTP's supervision tree philosophy ported to Go. The Erlang influence is explicit and intentional.

## Actor persistence

Actors managing durable state (e.g. `AgentActor`) snapshot to Postgres periodically. On restart, state is restored from the latest snapshot. Snapshots are stored as JSONB in the `events` table or a dedicated snapshot table.

!!! question "Open"
    Snapshot frequency and retention policy are not yet defined. A snapshot every N messages vs. every T seconds is the tradeoff — more frequent snapshots = faster restart but higher write pressure. Needs profiling at real load.
