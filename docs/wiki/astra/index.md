---
title: Astra
tags:
  - astra
  - overview
---

# Astra

Astra is an operating system for autonomous agents. Not a framework. Not a wrapper. An actual OS — microkernel, actor runtime, distributed task graph, sandboxed tool execution, layered memory, LLM routing as infrastructure.

**Target:** Millions of persistent agents, 100M+ tasks/day, no hot-path API call over 10ms.

The kernel/SDK/application boundary is strict by design. The kernel does exactly four things: run actors, execute task DAGs, route messages, manage state. Everything else lives outside it via well-defined APIs. Tight kernel = composable system.

!!! warning "Under construction"
    This wiki is a work in progress. Astra is being actively built — content will be expanded and made public as the project matures.

---

## Sections

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg } **Getting Started**

    ---

    Local setup, quickstart, and what you need to know before touching any code.

    [:octicons-arrow-right-24: Getting started](getting-started/index.md)

-   :material-layers:{ .lg } **Architecture**

    ---

    Kernel design, actor framework, task graph engine, scheduler, services, memory, and LLM routing.

    [:octicons-arrow-right-24: Architecture](architecture/index.md)

-   :material-book-open-variant:{ .lg } **Reference**

    ---

    gRPC contracts, database schema, Redis keys, message types, REST API surface, metrics.

    [:octicons-arrow-right-24: Reference](reference/index.md)

-   :material-monitor-eye:{ .lg } **Operations**

    ---

    Runbooks, oncall rotations, incident lifecycle, alerts.

    [:octicons-arrow-right-24: Operations](operations/index.md)

-   :material-cloud-upload:{ .lg } **Deployment**

    ---

    Local dev, Kubernetes/Helm, GCP managed services, macOS production.

    [:octicons-arrow-right-24: Deployment](deployment/index.md)


</div>

---

## At a glance

| Dimension | Value |
|---|---|
| Language | Go (84%), Python tooling |
| Kernel model | Microkernel + actor runtime |
| Task model | Distributed DAG with transactional state |
| Message bus | Redis Streams with consumer groups |
| Source of truth | Postgres (primary + replicas) |
| Hot-path cache | Redis (actor state, profiles, locks), Memcached (LLM/embedding responses) |
| Tool sandboxing | WASM / Docker / Firecracker |
| Memory | Redis (working), Postgres + pgvector (episodic/semantic) |
| LLM routing | Cost-aware model selection, Memcached response cache |
| Deployment targets | macOS (Metal/ANE) + Linux (CUDA/k8s) |
| Services | 16 canonical microservices |
| API latency SLA | ≤ 10ms (p99) for all reads |

!!! note "PRD is the source of truth"
    These wiki pages are derived from `docs/PRD.md` in the Astra repo. When there's a conflict, the PRD wins. Update the PRD in the same PR as the code change.
