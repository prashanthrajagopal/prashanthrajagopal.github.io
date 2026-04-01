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
| **Service-to-service** | **mTLS** on all inter-service gRPC/HTTP — no plaintext between services. Validated in `scripts/validate.sh` (S1). |
| **External API** | **JWT** from `identity`; validate expiry and scopes on every external-facing path. |
| **Authorization** | **RBAC / policy** via `access-control` (OPA-style checks on sensitive actions). |
| **Tool execution** | **Sandboxed** (WASM / Docker / Firecracker), resource limits, no secrets in env — ephemeral volumes. |
| **Secrets** | **Vault** at runtime — nothing long-lived in repo, logs, or events. Validated in `scripts/validate.sh` (S5). |
| **Dangerous actions** | **Human approval** for risky tasks and infra-changing operations where required. |

## Approval system

Two distinct approval types exist.

### Plan approval

When `AUTO_APPROVE_PLANS=false`, goal-service creates an `approval_requests` record for the implementation plan **before** the task graph is created. Access-control calls `POST /internal/apply-plan` on goal-service when the approval decision is made.

### Risky task approval

Dangerous tool execution (e.g. `terraform apply`, `shell_exec`) creates `approval_requests` with `request_type=’risky_task’`. tool-runtime polls or subscribes and waits for an approved decision before proceeding.

### Dual-approval (two-person rule)

`approval_requests.required_approvals` sets the minimum number of approvers needed. Individual approver decisions are tracked in the `approvals` JSONB array. Both plan and risky-task approvals support this.

### Approval routing

Requests route to **agent_admins** first (users designated for a specific agent). Falls back to **org_admins** if no agent_admins are configured.

## Roles

| Role | Scope |
|------|-------|
| **super_admin** | Platform-wide visibility; sees metrics and agent/worker metadata but never execution content (see redaction below). |
| **org_admin** | Manages org members, teams, agents within their org. Fallback approver for risky tasks and plans. |
| **agent_admin** | Designated per-agent; receives approve/reject requests for that agent’s plans and risky tasks. |
| **member** | Normal user within an org. |

## Super-admin data redaction

`redactForSuperAdmin()` strips the following fields before returning data to super-admin API callers:

- `system_prompt`, `config` — agent configuration
- `payload`, `result` — task I/O
- `goal_text` — goal content
- `code`, file contents, shell output — tool artifacts
- `chat_messages` — chat session content

Super-admins **see**: agent names, worker names, counts, cost totals, platform-wide aggregate metrics.
Super-admins **never see**: execution details, prompts, results, or any content produced by tool execution.

## Audit & compliance

- **Immutable event log** (`events` table) records: `TaskScheduled`, `TaskStarted`, `TaskCompleted`, `TaskFailed`, `PhaseStarted`, `PhaseCompleted`, `PhaseFailed`, `PhaseSummary`, `LLMUsage`.
- **Per-request LLM usage** is returned in API responses and persisted async to the `llm_usage` table via the `astra:usage` Redis stream.
- Security compliance checks S1 (mTLS) and S5 (Vault) are automated in `scripts/validate.sh`.

## Where to look in the repo

- **Gateway** — JWT middleware, rate limits, versioning.
- **`pkg/grpc`** — TLS client/server helpers for mTLS.
- **`access-control`** — approval workflows, policy checks.
- **`tool-runtime`** — sandbox lifecycle and caps.

## Related

- [Architecture overview](architecture/overview.md) — data plane and trust boundaries.
- [gRPC contracts](reference/grpc-contracts.md)
- PRD §18 Security, policy, governance
