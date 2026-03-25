---
title: Sandboxes aren't security theater
date: 2026-03-24
description: WASM, Docker, Firecracker — the spectrum of sandboxing when agents run tools you didn't write. Deny by default, allow by exception.
authors:
  - prashanth
categories:
  - Astra
tags:
  - security
  - wasm
  - docker
  - sandboxing
draft: false
---

The first time someone tells you "we sandbox the tools," your follow-up should be: **how?** Because the distance between "we run it in a container" and "we run it in a process that shares the host network and mounts `/var/run/docker.sock`" is the distance between security and a blog post you'll regret.

<!-- more -->

## The spectrum nobody talks about

Sandboxing isn't a binary. It's a spectrum, and most of it is more honest than people admit:

- **No sandbox:** Your agent's tool runs as your process, with your permissions, on your machine. This is fine for local dev. It's negligent for multi-tenant production.
- **Container (Docker/OCI):** Process isolation, filesystem isolation, network namespace. Better. But the container runtime is a shared surface, the kernel is shared, and if you're mounting host paths or running privileged, you've built a sandbox with the door open.
- **microVM (Firecracker, Cloud Hypervisor):** Separate kernel, minimal device model, fast boot. This is where isolation starts to feel real. You're not sharing a kernel with the workload. The blast radius of a compromised VM is the VM.
- **WASM (Wasmtime, WasmEdge):** Capability-based, no filesystem by default, no network by default, millisecond startup. The sandbox is the *absence* of permissions, not a wall built around them. You opt *in* to what the guest can do.

Each step trades convenience for isolation. The question isn't which is "best" — it's which matches the threat model you actually have.

## Astra's position

Agents run tools. Tools run code. Code that an LLM decided to run, based on input that a user provided, in a context that changes per request. If that sentence doesn't make you nervous, read it again.

In Astra, tool execution is designed with the assumption that **the tool is untrusted.** Not because every tool is malicious — because the combination of LLM-generated arguments and arbitrary code execution is a surface area that deserves respect.

The current architecture supports Docker-based sandboxing with a path toward WASM for lightweight tools and Firecracker for heavier workloads. The choice depends on what the tool needs:

- **Pure computation, no I/O?** WASM. Fast, locked down, disposable.
- **Needs filesystem, network, or specific runtimes?** Container with a restrictive security profile. No host mounts. No privileged mode. Ephemeral.
- **Needs full OS, untrusted provenance?** microVM. Burn it after use.

## Why "just use Docker" isn't enough

Docker is a packaging format that happens to provide isolation. The isolation is real but conditional — it depends on your configuration, your kernel version, your seccomp profile, whether someone added `--privileged` to the compose file six months ago and nobody noticed.

I've seen production systems where the "sandboxed" container could:

- Read the host's environment variables (including database credentials)
- Connect to the Docker socket and spawn sibling containers
- Write to shared volumes that other services read from

That's not a sandbox. That's a suggestion.

The fix isn't to abandon containers. It's to treat the container configuration as a security boundary and review it like one. Seccomp profiles. AppArmor or SELinux. Read-only root filesystem. No new privileges. Drop all capabilities, add back only what's needed. This is boring work. It's also the work.

## The WASM promise (and its current limits)

WASM is the closest thing we have to a sandbox that's secure by default. A WASM module starts with nothing — no filesystem, no network, no system calls. You grant capabilities explicitly through WASI. The mental model is right: **deny by default, allow by exception.**

The limits are real: WASI is still maturing, language support varies, and if your tool needs to `pip install` something at runtime, WASM isn't your answer today. But for a defined set of tools — data transformation, validation, formatting, lightweight computation — it's compelling. Millisecond cold starts, tiny memory footprint, and an isolation boundary that doesn't depend on getting your Linux kernel configuration right.

Astra is betting that more tools will fit this profile over time, not fewer.

## Security theater vs security engineering

Security theater is a checkbox. "Do we sandbox? Yes." Filed, forgotten, breached.

Security engineering is asking uncomfortable questions. What can escape this boundary? What happens if it does? Who reviews the configuration? How do we know it hasn't drifted?

Sandboxes aren't theater when they're built with the same discipline as the rest of the system. They're theater when they exist to satisfy an audit rather than to contain a failure.

The agent ecosystem is young enough that we get to set these norms. I'd rather set them honestly than optimistically.
