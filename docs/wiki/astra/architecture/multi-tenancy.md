---
title: Multi-Tenancy
tags:
  - astra
  - architecture
  - multi-tenancy
  - rbac
  - security
---

# Multi-Tenancy

Multi-tenancy is being added in Phase 11. The platform is a single shared platform with organisations (tenants), teams, users, and role-based access control. One org's data is never visible to another org.

!!! note "Phase 11 status"
    Phase 11 is in progress. The schema (migration 0018) is specified but not all sub-phases are complete. See [Phase 11 roadmap](../roadmap/phase-11.md).

## Entity model

| Entity | Description |
|---|---|
| **Platform** | Single shared platform. Users and agents share one system. |
| **Organization** | Tenant. Has its own agents, goals, tasks, workers, cost tracking, and approvals. |
| **Team** | Group within an org. Teams can own agents and be granted collaborator access. |
| **Org Membership** | Links a user to an org with a role (`admin` or `member`). |
| **Team Membership** | Links a user to a team with a role (`admin` or `member`). |

## Role model

| Role | Scope | Permissions |
|---|---|---|
| `super_admin` | Platform | Manage ALL orgs and users. See platform-wide metrics (redacted). **Cannot** see execution details, code, goal text, payloads, results, prompts, or chat. |
| `org_admin` | Organization | Full access to 100% of org data: agents, goals, tasks, workers, execution details, code, chat. Manage teams and members. |
| `org_member` | Organization | Use agents per visibility rules. Create private/public agents. Submit goals. |
| `team_admin` | Team | Manage team membership. Create team-scoped agents. |
| `team_member` | Team | Use team-scoped agents. |
| `agent_admin` | Agent | Approve/reject plans and risky task requests for that specific agent. |

## Agent visibility

| Visibility | Who can access |
|---|---|
| `global` | Every user in every org. Only super-admins can create/modify. Existing pre-Phase-11 agents are global. |
| `public` | Every member of the org. |
| `team` | Team members and org admins only. |
| `private` | Only the owner and explicitly added collaborators. |

## JWT claims

The `Claims` struct (defined in the identity/auth package) embeds `jwt.RegisteredClaims` and adds `user_id`, `email`, `is_super_admin` (boolean), and `scopes` (string slice). Post-Phase-11 claims will also carry `org_id`, `org_role`, and `team_ids`. These propagate via gRPC metadata headers (`x-user-id`, `x-org-id`, `x-org-role`, `x-team-ids`, `x-is-super-admin`) to all downstream services. See `internal/identity/` in the Astra repo.

## Super-admin data redaction

`redactForSuperAdmin()` strips: `system_prompt`, `config`, `payload`, `result`, `goal_text`, code output, file contents, shell output, and chat messages before returning data to super-admin endpoints. Super-admins see names and counts, not execution details.

## Key schema additions (migration 0018)

New tables: `users`, `organizations`, `org_memberships`, `teams`, `team_memberships`, `agent_collaborators`, `agent_admins`.

Columns added to existing tables: `org_id` on `agents`, `goals`, `tasks`, `workers`, `events`, `memories`, `llm_usage`, `approval_requests`, `chat_sessions`. Also `owner_id`, `team_id`, `visibility` on `agents`.

## Workspace isolation

- Global agents: `WORKSPACE_ROOT/_global/{goal_id}/`
- Org agents (Phase 11+): `WORKSPACE_ROOT/{org_slug}/{goal_id}/`

!!! warning "Tradeoff"
    Single-platform architecture means services query across the full dataset unless `WHERE org_id = $orgID` is consistently applied. This is a correctness requirement, not a performance hint. Missing an `org_id` filter in any service query is a data isolation bug.
