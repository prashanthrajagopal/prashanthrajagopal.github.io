---
title: Why I didn't use Kubernetes
date: 2026-03-15
description: Kubernetes solves fleet-scale orchestration. I was still deleting wrong ideas. Docker Compose for infra, native Go for services — sequence matters.
authors:
  - prashanth
categories:
  - Infrastructure
tags:
  - kubernetes
  - astra
  - devops
draft: false
---

First clarification: I'm not running a campaign against Kubernetes. I've shipped on it. I've debugged `CrashLoopBackOff` at hours nobody should be awake. I know what it's for. The question isn't whether k8s is good — it's whether it was the **default I wanted while I was still figuring out what I was building**.

For **Astra**, early on, the answer was no.

<!-- more -->

## The actual job

At the start, the job wasn't "orchestrate fifty binaries across three zones." It was: **can I get sixteen services talking to Postgres and Redis without losing the plot**, iterate in a debugger, and change a message shape without redeploying half a cluster. Kubernetes solves a different class of problem — the one where you've already committed to the shape of the system and now you need replicas, rollouts, and network policy at fleet scale.

I wasn't there yet. I was still in the phase where **half the work is deleting wrong ideas**. That phase is faster when your feedback loop is "restart the process" and not "check which pod is lying to you."

## Docker where it helps, native where it hurts

The compromise that stuck: **Postgres, Redis, Memcached, MinIO** — boring infrastructure — in **Docker Compose**. **Services** as **native Go processes** on the machine. One `docker compose up`, then run what you're actually changing. Logs on stdout. Breakpoints that attach to the binary you just built.

It's not prettier on a diagram. It's faster when you're still moving the architecture weekly.

## What I'd have paid for

Kubernetes would have bought me: uniform packaging, health probes everywhere, a story that fits a cloud sales deck. It would also have cost me: **another layer of YAML to reason about** while I was still unsure whether the scheduler belonged in the same deployable as the task service. Premature orchestration is like premature abstraction — you crystallize the wrong boundaries and then you're married to them.

## When I'll use it

When Astra needs **real** multi-node scheduling, **real** isolation between tenants at the network layer, or **real** horizontal scale beyond "one serious machine," Kubernetes (or something in that family) is on the table. The PRD already talks about GKE-style deployment for that world. That's not hypocrisy — that's **sequence**. You don't start with the fleet manager before you've proven the engine turns over.

## The shorter version

I didn't skip Kubernetes because I don't respect it. I skipped it because **the hardest problem wasn't packing processes into pods** — it was getting the kernel, the graph, and the workers to tell a consistent story. I wanted my complexity budget spent there first.

Maybe your project is different. Maybe your team is already three people and production is next Tuesday. In that case, reach for the tool that matches the fire you're standing in. For me, this month, the fire was design clarity — and Kubernetes doesn't help with that. It waits until you're ready to **operationalize** what you already believe.

Thanks for reading.
