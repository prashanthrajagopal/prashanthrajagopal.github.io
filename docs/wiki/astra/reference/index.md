---
title: Reference
tags:
  - astra
  - reference
---

# Reference

Authoritative technical specifications. When code and these pages diverge, the PRD (`docs/PRD.md` in the Astra repo) wins, then the code, then these pages.

## Pages

| Page | Contents |
|---|---|
| [gRPC Contracts](grpc-contracts.md) | `kernel.proto` and `task.proto` — full message and service definitions |
| [Database Schema](database-schema.md) | All migrations 0001–0024, table definitions, indexes, triggers |
| [Redis Keys](redis-keys.md) | All Redis key patterns, types, TTLs, and purposes |
| [Message Types](message-types.md) | All message types, stream schemas, and payload formats |
| [API Endpoints](api-endpoints.md) | Full REST API surface served by api-gateway |
| [Metrics](metrics.md) | All Prometheus metrics, their types, labels, and alert thresholds |
| [SLAs](slas.md) | Production SLA targets and MVP acceptance criteria |
