---
title: Metrics
tags:
  - astra
  - reference
  - observability
  - prometheus
---

# Metrics

All Prometheus metrics exposed by Astra services. Scraped by Prometheus, visualised in Grafana (`deployments/grafana/dashboards/`).

## Metric catalogue

| Metric | Type | Labels | Description |
|---|---|---|---|
| `astra_task_latency_seconds` | Histogram | `task_type`, `status` | Task execution latency from queued to completed |
| `astra_task_success_total` | Counter | `task_type` | Successful task completions |
| `astra_task_failure_total` | Counter | `task_type`, `error_type` | Failed task executions |
| `astra_events_processed_total` | Counter | `stream`, `consumer_group` | Events processed by stream consumers |
| `astra_actor_count` | Gauge | `actor_type` | Currently running actors |
| `astra_worker_heartbeat_total` | Counter | `worker_id` | Worker heartbeats received |
| `astra_llm_token_usage_total` | Counter | `model`, `agent_id` | LLM tokens consumed |
| `astra_llm_cost_dollars` | Counter | `model`, `agent_id` | LLM cost in USD |
| `astra_scheduler_ready_queue_depth` | Gauge | `shard` | Tasks waiting to be scheduled per shard |

## Dashboards

| Dashboard | URL | Contents |
|---|---|---|
| Platform Dashboard | `/superadmin/dashboard/` | Service health, workers, agents, goals, approvals, cost, Slack config |
| Cluster Overview | Grafana | Capacity, active agents, task throughput, error rate |
| Agent Health | Grafana | Per-agent throughput, avg latency, failure rate |
| Cost | Grafana | LLM token usage and cost per agent, per model, per day |
| Task Graph Viewer | Dashboard modal | Interactive DAG visualisation per goal |

## Alert rules

Prometheus alert rules in `deployments/prometheus/rules/astra-alerts.yaml`:

| Alert | Condition | Severity |
|---|---|---|
| `HighTaskFailureRate` | >5% task failures over 5min window | critical |
| `HighTaskQueueDepth` | >10,000 pending tasks | warning |
| `LowWorkerAvailability` | <50% of registered workers healthy | critical |
| `LLMCostSpike` | >2x daily average cost | warning |
| `ReadLatencySLOBreach` | p99 read latency > 10ms | critical |
| `SchedulingLatencySLOBreach` | p95 scheduling latency > 500ms | warning |

## Tracing

- Stack: OpenTelemetry SDK → OTLP exporter → collector → Jaeger/Tempo
- Each `Task` execution creates a root span
- Tool calls are child spans with resource attributes: `tool.name`, `sandbox.type`, `cpu.time`
- `trace_id` ties logs ↔ traces ↔ events
- `trace_id` is propagated in actor messages via `meta.trace_id`

## Inference backend observability

When hardware acceleration is active, the active backend is logged and exposed as a metric label:

```
inference_backend=metal|cuda|cpu
```

This makes it debuggable in production: if Metal is supposed to be active and you're seeing `cpu` in the metrics, something is wrong with the detection path.
