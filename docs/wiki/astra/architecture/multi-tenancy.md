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

## JWT and context

Tokens carry **user identity**, **org/team context**, and **roles** as described in **PRD §18–19**. Downstream services receive that context through **standard internal headers** — exact header names and claim layouts are **not** documented on this wiki.

## Super-admin data redaction

`redactForSuperAdmin()` strips: `system_prompt`, `config`, `payload`, `result`, `goal_text`, code output, file contents, shell output, and chat messages before returning data to super-admin endpoints. Super-admins see names and counts, not execution details.

## Schema

Orgs, teams, memberships, and agent visibility are backed by **additional tables and columns** on core entities. Full DDL is **PRD §11 / §19**.

## Workspace isolation

On-disk workspace layout is **partitioned** so org-scoped work does not collide with other tenants; paths follow **PRD §19**.

!!! warning "Tradeoff"
    Single-platform architecture means services query across the full dataset unless `WHERE org_id = $orgID` is consistently applied. This is a correctness requirement, not a performance hint. Missing an `org_id` filter in any service query is a data isolation bug.
