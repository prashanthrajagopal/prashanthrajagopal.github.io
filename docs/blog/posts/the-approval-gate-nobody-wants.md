---
title: The approval gate nobody wants (until they do)
date: 2026-03-18
description: Building dual-approval and plan gates into an autonomous agent system — the tension between speed and not letting agents terraform destroy prod.
authors:
  - prashanth
categories:
  - Astra
tags:
  - astra
  - security
  - agents
  - governance
draft: false
---

Every team that builds autonomous agents goes through the same arc. First, you're impressed by how much the agent can do on its own. Then, you give it access to a real environment. Then, somewhere between "this is incredible" and "oh no," it does something irreversible — deletes the wrong records, applies a Terraform plan against prod instead of staging, sends an email to a list it shouldn't have touched. And then, immediately, you want an approval gate.

The problem is that approval gates bolted on after the fact are terrible. They're the wrong shape. They interrupt execution at arbitrary points, they don't distinguish between reversible and irreversible actions, and they're usually implemented as a comment in a Slack channel that someone has to read before manually triggering the next step. That's not a governance system. That's hope with a paper trail.

<!-- more -->

## Two kinds of gates, not one

Astra has two distinct approval types, and the distinction matters.

The first is **plan approval** — a gate before the task graph is even created. When an agent receives a goal, the goal-service can require a human to review and approve the *plan* before any execution begins. This is the "show your work before you start" gate. It answers the question: is the approach right, not just is this specific action safe?

The second is **risky task approval** — a gate before a specific tool execution. Some tools are inherently dangerous: `terraform apply`, bulk database writes, anything that sends external communications, any operation that touches billing or access control. When a task is marked `risky`, execution pauses, an approval request is created, and the task waits. No polling, no timeout-and-proceed — it waits until a human says yes or no.

**The reason you need both is that they catch different failure modes.** Plan approval catches architectural problems upstream: an agent that has decided to solve the problem in a way that will technically work but is completely wrong for the context. Risky task approval catches execution-time surprises: a plan that looked fine but contains one step that would be catastrophic in this specific environment.

## The routing and the dual-approval rule

Not every approval goes to the same person. Astra routes approval requests through access-control: first to `agent_admins` (people who run agents and understand their behavior), then escalating to `org_admins` (people who own the environment and bear the consequences).

For high-risk operations, there's a dual-approval requirement — two independent humans must approve before execution proceeds. This is the two-person rule from nuclear launch doctrine, applied to Terraform. It's not paranoia. It's an acknowledgment that one person reviewing an agent-generated plan under time pressure is a single point of failure. **Two people with different contexts catching different things is materially safer than one person catching everything.**

The flow is: goal-service creates an approval request and transitions the task to a waiting state — access-control exposes that request to the appropriate humans — humans approve or reject — goal-service creates the task graph (for plan approval) or releases the task for execution (for risky task approval). The approval is a first-class event in the system, not a side channel.

## The AUTO_APPROVE_PLANS escape hatch

There's an `AUTO_APPROVE_PLANS` environment toggle that bypasses plan approval. I built it because not every environment needs the same governance posture — a development environment where an agent is exploring a sandboxed dataset doesn't need a human in the loop for every plan. A production environment that touches customer data does.

The toggle exists, and I'm somewhat ambivalent about it. The danger is the usual one: you set it for dev, you forget you set it, you promote the config to prod. I've made it explicit in the config surface rather than a buried flag because **the decisions you make about governance posture should be visible, not inferred from environment variable archaeology**.

There's no equivalent escape hatch for risky tasks. That gate is always active if the task is marked risky. The argument for removing it is always "we trust this agent" and the counterargument is always "you trusted the last one too, until the incident."

## Why first-class and not bolted on

The instinct when you first design an agent system is to make it fast and frictionless. You're trying to demonstrate autonomous capability, and approval gates are the opposite of autonomous. They feel like a concession. You're building a system that can do things, and the approval gate is you saying "but not without permission."

The reframe that worked for me: **an approval gate isn't a limitation on autonomy, it's a definition of it**. The agent is fully autonomous within its approved scope. The gate defines that scope. A system with no gates isn't more autonomous — it's more unpredictable. And unpredictable systems don't get access to the things worth automating.

The systems I've seen that called themselves autonomous and had no governance were fine until they weren't. When they weren't, they got shut down — not patched, not gated, *shut down* — because the organization had no mechanism for trust recovery. You can't incrementally restore confidence in a system when the only knob is "on" or "off."

Astra's approval system is designed to be the infrastructure that earns the system more autonomy over time, not to be the ceiling. An agent that operates cleanly within its gates accumulates a record. That record justifies expanding the scope. An agent that needs a gate removed because it's "too slow" has a different kind of record.

Nobody wants approval gates. Right up until they do.
