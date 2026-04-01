---
title: Why Astra runs on a Mac Mini
date: 2026-03-16
description: macOS as a production deployment target for an agent OS — Metal acceleration, native binaries, no emulation. When Kubernetes isn't the answer.
authors:
  - prashanth
categories:
  - Astra
tags:
  - astra
  - macos
  - deployment
  - metal
draft: false
---

The question I get most often about Astra's hardware setup — after "why not just use AWS" — is some variant of "are you serious about the Mac Mini." Yes. **I'm serious about the Mac Mini.** Not as a dev box that happens to run server code, but as an intentional production deployment target with concrete technical advantages over the alternatives I actually considered.

This isn't contrarianism. It's arithmetic.

<!-- more -->

## What the hardware actually gives you

Apple Silicon is a different proposition from a cloud VM. The M-series chips have **unified memory** — no PCIe bus separating CPU from GPU, no copying tensors back and forth across lanes that exist because the memory hierarchy was designed forty years ago for a different set of problems. When Astra runs an embedding model or routes inference through a local LLM, the data stays in the same physical memory pool the Go runtime uses. That's not a footnote — it changes the latency profile.

The Mac Mini M4 Pro with 24GB costs $1299 one time. The equivalent cloud configuration — a GPU-capable instance with enough RAM to run a vector model alongside sixteen services and a Postgres instance — runs north of $400/month before you add managed services, egress, and the tax for "availability." The Mac Mini is paid off in three months and doesn't send you a bill when you forget to set a budget alert.

A Mac Studio with 64GB unified memory is $1999. That's running the whole stack — inference, embeddings, orchestration, storage — and you still have budget headroom. Do the math on what that costs as an EC2 instance over two years.

## Metal, Core ML, and the graceful fallback

Astra uses `ASTRA_USE_METAL=true` as the signal to enable GPU-accelerated paths. The implementation is straightforward: **build tags** (`//go:build darwin`) isolate platform-specific code, and the runtime checks `runtime.GOOS` for anything that can't be expressed statically. One codebase. No forks.

When Metal is available, embedding generation and inference routing use it. When it's not — Linux CI, a dev container, someone's Ubuntu box — the same code falls through to a CPU path. The fallback isn't an afterthought; it's load-bearing. I can't accept a codebase where the production fast path and the development path diverge so far that bugs only appear in one of them.

The Neural Engine via Core ML is more situational. For models that can be compiled to a `.mlpackage`, the ANE is genuinely fast and miserly on power. For models that can't, it's not worth the conversion overhead. I treat ANE as an optimization to reach for when the model fits, not a deployment requirement.

## Infrastructure adjacent, not inside

Postgres and Redis run in Docker on the same machine. Not because containers are philosophically necessary here, but because **boring infrastructure should be boring** — versioned, isolated, easy to snapshot, easy to blow away. The services themselves are native `darwin/arm64` binaries. No Rosetta, no emulation layer, no Docker Desktop eating memory to virtualize Linux on ARM.

The process supervisor is `launchd` for persistent daemons, with a lighter process manager for the service mesh during development. It's not elegant on a diagram. It restarts dead processes and logs to a place I can find with `tail`. That's the job.

## The honest limitations

Single point of failure. No horizontal scaling. If the Mac Mini has a hardware problem, Astra is down until I fix it.

For a solo builder or a small team proving out an architecture, this is an acceptable trade. **You don't solve fleet reliability problems before you have a fleet.** The design keeps the door open — the service interfaces are the same regardless of deployment target, the Go binaries cross-compile cleanly to Linux, and nothing in the architecture requires Metal. When Astra needs to run on GKE or bare metal in a colo, the code is ready. The deployment target changes; the system doesn't.

## The real reason

The cloud pitch is: pay for compute as you need it, scale horizontally, never touch hardware. The reality for a project at this stage is: **pay a fixed rate for someone else's margin, fight NAT and egress and cold starts, and get configuration management as a service instead of a config file**.

A Mac Mini on a desk gives you hardware you can trust, a memory architecture that makes local inference not embarrassing, and a monthly bill that is zero dollars. The complexity I don't want is "distributed systems before I've earned them." A single serious machine with unified memory and a Metal backend is not a consolation prize. It's the right tool for the problem I'm currently solving.

Kubernetes solves fleet problems. I have a desk problem.

Thanks for reading.
