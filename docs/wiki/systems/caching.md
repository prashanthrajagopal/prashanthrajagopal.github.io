---
title: Caching
---

# Caching

**Read-through:** miss loads from origin then populates cache — common for Astra's actor/profile keys. **TTL** bounds staleness; **invalidation on write** keeps correctness for mutable entities.

**Cache stampede:** many clients miss at once after expiry — mitigate with **single-flight** locking, staggered TTL jitter, or short-lived negative cache. At Astra scale, stampedes on hot agent keys are a real risk during incidents (Redis flap).

**Memcached vs Redis:** Memcached for **large blob** LLM responses; Redis for **structured** keys and **streams** — different eviction and data models.
