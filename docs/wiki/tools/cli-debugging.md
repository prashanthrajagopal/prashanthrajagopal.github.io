---
title: CLI debugging
---

# CLI debugging

Quick recipes useful for Astra and web ops:

| Tool | Use |
|------|-----|
| **curl** | `curl -sS -H "Authorization: Bearer $JWT" http://localhost:8080/agents` |
| **grpcurl** | Reflection-enabled gRPC: list services, invoke RPCs against local tasks |
| **redis-cli** | `PING`, `XREAD COUNT 5 STREAMS astra:tasks:shard:0 0` |
| **psql** | `\dt`, explain plans on slow scheduler queries |
| **kubectl** | logs, exec, rollout status for k8s deployments |

Always **redact tokens** when pasting output. Prefer read-only queries in production.
