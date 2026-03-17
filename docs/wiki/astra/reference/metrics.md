---
title: Metrics
tags:
  - astra
  - reference
  - observability
---

# Metrics

Observability follows **RED** (rate, errors, duration) and **USE** (utilization, saturation, errors) patterns. **Prometheus**-style metrics cover **tasks**, **workers**, **LLM usage**, **scheduling depth**, and **actors**. Exact **metric names**, **dashboard JSON**, and **alert rule files** are **internal** to the Astra repo (**PRD §17**).

## Themes

| Theme | Examples |
|-------|----------|
| Task path | Latency, success/failure counts |
| Workers | Heartbeats, availability |
| Scheduler | Queue depth per shard |
| LLM | Tokens, cost |
| Inference | Active backend (CPU vs accelerated) |

## Tracing

**Distributed traces** link **requests**, **task runs**, and **tool calls** via shared correlation IDs. Stack details: **PRD §17**.

## Dashboards

**Platform dashboard** (gateway-hosted) and **Grafana** views summarise health, cost, and throughput — see **PRD** for surfaces.
