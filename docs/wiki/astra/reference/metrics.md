---
title: Metrics
tags:
  - astra
  - reference
  - observability
---

# Metrics

Observability follows **RED** (rate, errors, duration) and **USE** (utilization, saturation, errors) patterns. Metrics are **Prometheus**-style. Dashboard JSON and alert rule files are internal to the Astra repo (**PRD §17**).

## Metric catalog

| Metric | Type | Description |
|--------|------|-------------|
| `astra_task_latency_seconds` | Histogram | End-to-end task execution duration |
| `astra_task_success_total` | Counter | Tasks completed successfully |
| `astra_task_failure_total` | Counter | Tasks that failed or timed out |
| `astra_events_processed_total` | Counter | Events processed by the event loop |
| `astra_actor_count` | Gauge | Active actor / agent count |
| `astra_worker_heartbeat_total` | Counter | Worker heartbeat signals received |
| `astra_llm_token_usage_total` | Counter | Total LLM tokens consumed (label: `model`) |
| `astra_llm_cost_dollars` | Counter | Cumulative LLM cost in USD (label: `model`) |
| `astra_scheduler_ready_queue_depth` | Gauge | Tasks waiting in the ready queue (per shard) |

## Alert thresholds

| Alert | Condition |
|-------|-----------|
| High task failure rate | `astra_task_failure_total / (astra_task_success_total + astra_task_failure_total) > 5%` over 5 min |
| High queue depth | `astra_scheduler_ready_queue_depth > 10000` pending tasks |
| Low worker availability | Registered workers < 50% of expected pool |
| LLM cost spike | Daily `astra_llm_cost_dollars` rate > 2× rolling daily average |

## Tracing

**Distributed traces** link **requests**, **task runs**, and **tool calls** via shared correlation IDs. Stack details: **PRD §17**.

## Dashboards

**Platform dashboard** (gateway-hosted) and **Grafana** views summarise health, cost, and throughput — see **PRD** for surfaces.
