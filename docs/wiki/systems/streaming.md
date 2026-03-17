---
title: Streaming
---

# Streaming

**Redis Streams** give consumer groups, persistence, and approximate ordering per shard. Astra uses them for **task dispatch** and **worker events**. Compare to **Kafka** when you need longer retention, replay-by-offset, and cross-datacenter replication — Redis wins for **low-latency** work queues with modest retention.

**At-least-once:** consumers must **idempotent** handlers or dedupe by message ID. Task execution uses DB state to reject duplicate completes.
