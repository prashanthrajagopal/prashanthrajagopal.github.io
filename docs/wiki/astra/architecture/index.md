---
title: Architecture
tags:
  - astra
  - architecture
---

# Architecture

Astra is a **layered** system: a **small kernel**, **services**, and **infrastructure**. Start with **[Overview](overview.md)** for diagrams and end-to-end flow.

## Doc map

| Page | Question |
|------|----------|
| [Overview](overview.md) | Layers? Goal → task flow? |
| [Kernel](kernel.md) | What belongs in the kernel? |
| [Actor framework](actor-framework.md) | Mailboxes, supervision? |
| [Task graph](task-graph.md) | DAG, task states? |
| [Scheduler](scheduler.md) | Dispatch, shards, latency? |
| [Services](services.md) | The 16 services? |
| [Memory](memory.md) | Memory tiers? |
| [LLM routing](llm-routing.md) | Models, cost, cache? |
| [Multi-tenancy](multi-tenancy.md) | Isolation, roles? |

## Design principles (summary)

1. **Kernel stays small** — product logic lives in services and the SDK.  
2. **Database is source of truth** for durable agent/task state; caches accelerate reads.  
3. **Hot-path reads** target strict latency goals (**PRD §25**).  
4. **Writes** are durable first, then **events**, then **cache refresh**.  
5. **Audit trail** supports recovery and compliance.  
6. **Actors** favour clear message boundaries over shared mutable state.

!!! note
    Implementation specifics are intentionally **not** on this public wiki.
