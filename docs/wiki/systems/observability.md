---
title: Observability
---

# Observability

**Metrics (RED):** rate, errors, duration per service. **USE:** utilization, saturation, errors for nodes. **Logs:** structured, correlation IDs (`trace_id` in message meta). **Traces:** OTel from gateway through workers.

On-call value comes from **dashboards + runbooks** wired to the same metric names — see Astra [Metrics](../astra/reference/metrics.md) and [Operations](../astra/operations/index.md).
