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

## API surface

Kernel-oriented RPCs (spawn, send, task lifecycle, streams) are specified in **PRD §10**. This wiki does not reproduce full protobuf definitions.

!!! note
    For exact messages and service boundaries, use **`docs/PRD.md`** in the Astra repository.
