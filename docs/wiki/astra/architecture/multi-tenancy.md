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

## Isolation dimensions

| Dimension | Mechanism |
|-----------|-----------|
| **Data** | Org-scoped rows and JWT claims; queries filtered by org membership. |
| **Identity** | `identity` issues tokens with org and role claims. |
| **Policy** | `access-control` enforces RBAC and approvals per agent/org. |
| **Network** | In Kubernetes, network policies can segregate namespaces per environment; production uses private networking to data stores. |

!!! note "Phase 11 status"
    Phase 11 is in progress. The schema (migration 0018) is specified but not all sub-phases are complete. See the PRD Phase 11 / dashboard sections for current scope.

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

## Agent collaborators and admins

- **Collaborators** grant access to private/team agents. A collaborator can be a user or a team. Permission levels: `use`, `edit`, `admin`.
- **Agent admins** receive approve/reject requests for a specific agent's plans and risky tasks. Falls back to org admins if no agent admins are set.

## JWT claims

```
user_id, email, is_super_admin, scopes
```

Login: `POST /users/login` with email + password → JWT. gRPC metadata propagation: `x-user-id`, `x-org-id`, `x-org-role`, `x-team-ids`, `x-is-super-admin`.

## URL structure

| URL | Purpose | Auth |
|-----|---------|------|
| `/` | Landing/login page | None |
| `/login` | Login form | None |
| `/superadmin/dashboard` | Super-admin dashboard | `super_admin` JWT |
| `/superadmin/api/*` | Dashboard API (snapshot, approvals, goals, agents, chat, Slack config) | JWT |
| `/health` | Health check | None |

## Super-admin data redaction

`redactForSuperAdmin()` strips: `system_prompt`, `config`, `payload`, `result`, `goal_text`, code output, file contents, shell output, and chat messages before returning data to super-admin endpoints. Super-admins see names and counts, not execution details.

## Schema

Orgs, teams, memberships, and agent visibility are backed by **additional tables and columns** on core entities. Full DDL is **PRD §11 / §19**.

## Super-admin dashboard

Shows platform-wide **redacted** data: service health, workers (names/status), agents (names/status), goal/task counts, LLM cost totals. **Organizations** section (create/edit/delete, add org admins). **Users** section (paginated table, search/filter, suspend/activate/reset-password/role-change/move-org actions, detail modal). Org filter dropdown.

## Privacy and data isolation

1. **Authentication:** All dashboard and agent APIs require a valid JWT.
2. **Super-admin redaction:** `redactForSuperAdmin()` strips `system_prompt`, `config`, `payload`, `result`, `goal_text`, code, file contents, shell output, and chat messages.
3. **Single platform:** All services operate on one platform. Agent-service `QueryState` returns all agents. Service queries use `WHERE org_id = $orgID` for isolation.
4. **Workspace isolation:** `WORKSPACE_ROOT/_global/{goal_id}/` for global agents; `WORKSPACE_ROOT/{org_slug}/{goal_id}/` for org agents.

!!! warning "Tradeoff"
    Single-platform architecture means services query across the full dataset unless `WHERE org_id = $orgID` is consistently applied. This is a correctness requirement, not a performance hint. Missing an `org_id` filter in any service query is a data isolation bug.
