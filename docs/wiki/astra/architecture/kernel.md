---
title: Kernel Design
tags:
  - astra
  - architecture
  - kernel
---

# Kernel Design

The Astra kernel is intentionally **minimal**. It focuses on actors, task graphs, scheduling, messaging, and transactional state — not product or LLM logic.

## Responsibilities

1. **Actor runtime** — many concurrent actors with mailboxes and message delivery.  
2. **Task graph** — DAG persistence, dependencies, lifecycle.  
3. **Scheduler** — ready-task detection and dispatch to workers.  
4. **Message bus** — stream-based coordination between components.  
5. **State** — durable writes and event history aligned with task transitions.

## Non-responsibilities

The kernel does **not** own HTTP ingress, user-facing dashboards, OAuth, or prompt design. Those sit in **services** and the **SDK**. Long-term semantic memory orchestration is a **memory service** concern on top of kernel primitives, not inside the kernel.

## Message path (conceptual)

```mermaid
flowchart LR
  S[Sender] --> K[Kernel]
  K --> M[Mailbox]
  M --> R[Actor]
```

| Interaction | Role of kernel |
|-------------|----------------|
| **Spawn** | Register and start an actor |
| **Send** | Deliver a message to an actor’s mailbox |
| **Tasks** | Coordinate graph state and scheduling with the database and streams |
| **Events** | Align durable events with state changes |

## Invariants

- The kernel stays **small and stable**; growth requires explicit design review.  
- Services talk to the kernel through **published APIs**, not by reaching into implementation details.  
- **Durable task state** and **event history** stay consistent with the transactional model described in the PRD.

## Platform stability (P0–P2)

Completed hardening across three priority tiers. All items are implemented and validated.

### P0 — Core correctness

| Feature | Behavior |
|---------|----------|
| **Agent restore on startup** | `agent-service` loads all agents with `status = 'active'` from DB at startup, spawns into kernel via `NewFromExisting`. No manual re-spawn needed after restart. |
| **Dead-letter tasks** | When `retries >= max_retries`, task transitions to `dead_letter` status. Optionally published to `astra:dead_letter` stream for alerting/repair. |
| **Redis consumer retry** | `XAck` only on handler success. Per-message retry count in Redis hash (1h TTL). After N failures, publish to `astra:dead_letter` then `XAck`. `XAutoClaim` reclaims pending messages after 30s `MinIdle`. |

### P1 — Resilience

| Feature | Behavior |
|---------|----------|
| **Readiness vs liveness** | `GET /health` = liveness. `GET /ready` = DB + Redis ping. Helm `readinessProbe` uses `/ready`; LB stops traffic on failure. |
| **Gateway circuit breakers** | Protects goal-service, agent-service, access-control (gRPC). 5 failures in 30s opens circuit → 503 + optional `Retry-After`. 10s half-open cooldown. |
| **Goal idempotency** | `Idempotency-Key` header on `POST /goals`. Redis-backed, 24h TTL. Duplicate key returns same `goal_id`. |

### P2 — Scale and clarity

| Feature | Behavior |
|---------|----------|
| **Shard ownership** | Configurable `TASK_SHARD_COUNT`. Streams: `astra:tasks:shard:{0..N-1}`. Hash: `FNV-1a(agent_id) % count`. Workers consume all shards. |
| **Supervision wiring** | Supervisor connected to agent actors in `agent-service`. Handler wrapper recovers panics → `HandleFailure`. On `Terminate`, `kernel.Stop(agentID)`. |
| **Mailbox full handling** | `ErrMailboxFull` returned on overflow. gRPC `ResourceExhausted` status with `retry-after` trailer (seconds). Client backs off. |

## API surface

Kernel-oriented RPCs (spawn, send, task lifecycle, streams) are specified in **PRD §10**. This wiki does not reproduce full protobuf definitions.

!!! note
    For exact messages and service boundaries, use **`docs/PRD.md`** in the Astra repository.
