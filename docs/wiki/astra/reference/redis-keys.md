---
title: Redis Keys
tags:
  - astra
  - reference
  - redis
  - cache
---

# Redis Keys

Redis is used for **caches**, **locks**, **streams**, and **ephemeral coordination**. Exact key strings and TTLs evolve — **PRD §12–13** is authoritative.

## Families (purpose-level)

| Family | Purpose |
|--------|---------|
| Actor / agent | Working state, profiles, document list cache |
| Task / graph | Short-lived read cache, claim coordination |
| Worker | Liveness / heartbeat |
| User / org | Membership caches where used |
| Streams | Task dispatch, worker events, usage fan-out |
| Cost / quota | Token or budget counters |

## Streams

**Task dispatch** uses **sharded streams** so workers scale horizontally. **Heartbeats** and **usage** events use separate streams. Consumer groups process messages with **ack** semantics; **retries** and **dead-letter** behaviour follow platform policy in the PRD.

## Caching

Cache entries have **TTLs**; writes **invalidate** relevant keys so users don’t see stale profile/doc data indefinitely.

!!! note
    **Exact key patterns, MAXLEN, and lock algorithms** are internal — see PRD / private ops docs.
