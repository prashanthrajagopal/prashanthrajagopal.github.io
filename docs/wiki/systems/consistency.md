---
title: Consistency
---

# Consistency

**Postgres** is the **source of truth** for tasks and agents. **Redis** may lag briefly after writes. APIs that promise **10ms** reads accept **eventual consistency** on cached fields; authoritative reads that need fresh data must be explicitly designed (often not on the hot path).

**Linearizable** updates for task state use **single-row transactions** with optimistic checks (`WHERE status = expected`).
