---
title: Security
tags:
  - astra
  - security
---

# Security

Astra’s security model is spelled out in **PRD §18** and platform rules. Below is a concise map for contributors and operators.

## Policy themes (S1–S6 style)

| Theme | Requirement |
|-------|-------------|
| **Service-to-service** | **mTLS** on all inter-service gRPC/HTTP — no plaintext between services. |
| **External API** | **JWT** from `identity`; validate expiry and scopes on every external-facing path. |
| **Authorization** | **RBAC / policy** via `access-control` (OPA-style checks on sensitive actions). |
| **Tool execution** | **Sandboxed** (WASM / Docker / Firecracker), resource limits, no secrets in env — ephemeral volumes. |
| **Secrets** | **Vault** (or equivalent) at runtime — nothing long-lived in repo, logs, or events. |
| **Dangerous actions** | **Human approval** for risky tasks and infra-changing operations where required. |

## Where to look in the repo

- **Gateway** — JWT middleware, rate limits, versioning.
- **`pkg/grpc`** — TLS client/server helpers for mTLS.
- **`access-control`** — approval workflows, policy checks.
- **`tool-runtime`** — sandbox lifecycle and caps.

## Related

- [Architecture overview](architecture/overview.md) — data plane and trust boundaries.
- [gRPC contracts](reference/grpc-contracts.md)
- PRD §18 Security, policy, governance
