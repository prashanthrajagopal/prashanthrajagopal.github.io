---
title: Architecture
tags:
  - astra
  - architecture
---

# Architecture

Astra's architecture is a strict layered system with a minimal kernel at the centre. Every design decision flows from one constraint: **the kernel must stay small so the system stays composable.**

## Pages

| Page | What it covers |
|---|---|
| [Overview](overview.md) | High-level architecture, key principles, component diagram |
| [Kernel](kernel.md) | Kernel responsibilities, invariants, gRPC API surface |
| [Actor Framework](actor-framework.md) | `Actor` interface, `BaseActor`, mailbox, supervision tree |
| [Task Graph Engine](task-graph.md) | DAG model, Go types, state machine, transactional transitions |
| [Scheduler](scheduler.md) | Ready-task detection, sharding, dispatch algorithm, heartbeats |
| [Services](services.md) | All 16 canonical microservices, namespaces, responsibilities |
| [Memory](memory.md) | Working memory (Redis), episodic/semantic (Postgres + pgvector) |
| [LLM Routing](llm-routing.md) | Model tiers, cost controls, Memcached caching, async audit |
| [Multi-Tenancy](multi-tenancy.md) | Org/team/user model, roles, agent visibility, JWT claims |

## Design principles

**1. Strict kernel/SDK/application separation.** Application code never imports kernel internals. The kernel exposes four APIs: actor, task, message, state. That's it.

**2. Postgres is the source of truth.** All durable state transitions write to Postgres in a transaction and append to the `events` table atomically. Redis is a performance layer, not the source of truth.

**3. All reads serve from cache.** No hot-path API call hits Postgres synchronously. Redis for structured reads (actor state, agent profiles, task reads via `CachedStore`), Memcached for LLM/embedding responses. The 10ms SLA is enforced by this rule.

**4. Write → stream → cache.** The write path is: persist to Postgres → publish event to Redis Stream → async cache update. Cache misses fall through to Postgres and populate for subsequent reads.

**5. Event sourcing for task state.** Every task state transition appends to the `events` table in the same transaction as the state update. This gives a complete audit trail and the ability to reconstruct graph state from events.

**6. Convention over configuration in the actor model.** BaseActor handles mailbox, goroutine lifecycle, and stop mechanics. Implementors override `Receive()`. This is the Rails instinct applied to concurrent systems design.
