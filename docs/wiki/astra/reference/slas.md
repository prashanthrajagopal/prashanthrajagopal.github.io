---
title: SLAs & Acceptance Criteria
tags:
  - astra
  - reference
  - sla
  - performance
---

# SLAs & Acceptance Criteria

## Production SLAs

| SLA | Target | Measurement |
|-----|--------|-------------|
| Control plane API availability | 99.9% | Uptime checks + gateway health |
| API read response time (p99) | ≤ 10ms | Histogram on cached read paths |
| Task scheduling latency (median) | ≤ 50ms | Ready detection → dispatch |
| Task scheduling latency (p95) | ≤ 500ms | End-to-end scheduling path |
| Task execution correctness | ≥ 99% pass rate | Task success / (success + failure) |
| Worker failure detection | ≤ 30s | Heartbeat stream gap |
| Event durability | ≤ 1s | Async path to durable audit log |

The 10ms read SLA is the hardest constraint in the system. It is the reason the cache architecture exists. Any code path that reads from Postgres synchronously on a hot API endpoint is a bug — not a performance issue, a correctness issue.

## MVP functional acceptance

| Criterion | Phase delivered |
|---|---|
| Spawn and run a persistent agent | Phase 1 |
| Planner produces task DAGs from a goal | Phase 4 |
| Scheduler detects ready tasks and dispatches to workers | Phase 1 |
| Worker executes tasks and returns results persisted in Postgres | Phase 1/2 |
| Task state transitions emit events to `events` table | Phase 1 |
| Observability traces visible for each task execution | Phase 5 |
| Tool runtime can run sandboxed command and return artifact | Phase 2 |

## Scale targets

| Target | Value |
|---|---|
| Concurrent agents | Millions |
| Tasks per day | 100M+ |
| No single API call > | 10ms |
| Worker failure detection | ≤ 30s |

These are **design targets**. Load-testing procedures live **in the Astra repo**.
