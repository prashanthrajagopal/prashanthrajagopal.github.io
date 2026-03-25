---
title: LiteLLM and the trust chain nobody audits
date: 2026-03-26
description: A compromised security scanner led to malicious LiteLLM PyPI packages that harvested credentials and spread through Kubernetes clusters in three hours.
authors:
  - prashanth
categories:
  - Security
tags:
  - security
  - supply-chain
  - astra
  - agents
  - sandboxing
draft: false
---

On Monday, someone pushed two compromised versions of `litellm` to PyPI. They were live for about three hours. In that window, any `pip install litellm` — or any CI pipeline that didn't pin versions — pulled a package that harvested SSH keys, cloud credentials, Kubernetes configs, crypto wallets, database passwords, and anything else worth stealing from the machine it landed on. Then it encrypted the haul, exfiltrated it to a spoofed domain, installed a systemd backdoor, set up C2 beaconing, and — if it found Kubernetes service account tokens — spawned privileged pods on every node in the cluster.

Three hours. 3.4 million daily downloads. That's the math.

<!-- more -->

## How the trust chain broke

The attack didn't start at PyPI. It started in a security scanner — Trivy, the tool you run *to find vulnerabilities* — compromised via stolen credentials in late February. A poisoned Trivy GitHub Action shipped as v0.69.4 on March 19. That action ran in LiteLLM's CI/CD pipeline. The attacker harvested PyPI publisher credentials from the CI environment, then used those credentials to publish two malicious versions of `litellm` on March 24.

Read that again: **the security tool was the attack vector.** The thing you install to audit your dependencies was itself a compromised dependency. The trust chain here is: you trust PyPI, which trusts the publisher, whose credentials came from CI, which trusted a GitHub Action, which trusted its maintainer's credentials, which were stolen. Five links. Nobody audits the full chain.

## The .pth trick deserves its own paragraph

Version 1.82.7 hid the payload in `proxy_server.py` — base64-encoded, executed on import. Ugly but at least you had to import the package. Version 1.82.8, published thirteen minutes later, escalated. It dropped a `.pth` file — `litellm_init.pth` — into `site-packages`.

Here's the thing about `.pth` files: Python executes them automatically during interpreter initialization. Not on import. On *startup*. Running `pip install something-else` would trigger it. Running `python --version` would trigger it. The payload ran before your code did. And it passed pip's hash verification because it was signed with legitimate stolen credentials. The package was *authentic*. It was also hostile.

## Six stages of "we're fine, this is fine"

The payload wasn't a smash-and-grab. It was a six-stage operation:

1. **Harvest everything.** SSH keys, AWS/GCP/Azure credentials, kubeconfigs, Docker configs, shell history, `.env` files, even AWS Secrets Manager and SSM Parameter Store. If it was on disk and worth stealing, it was collected.
2. **Encrypt.** AES-256 with RSA-4096 key wrapping. The attacker's operational security was better than most companies'.
3. **Exfiltrate.** Encrypted payload sent to `models.litellm.cloud` — a domain that looks like it belongs to the project. Header: `X-Filename: tpcp.tar.gz`. Subtle.
4. **Persist.** Wrote `~/.config/sysmon/sysmon.py`, installed a systemd service. Survives reboots. Survives "we removed the bad package."
5. **Beacon.** Polled `checkmarx.zone/raw` for follow-up payloads. Downloaded to `/tmp/pglog`, executed. The initial compromise was the door; C2 was the hallway.
6. **Spread.** If Kubernetes service account tokens were available, spawned privileged `node-setup-*` pods on every node. One compromised CI runner becomes an entire cluster.

This wasn't a script kiddie. This was TeamPCP — the same group that hit 45+ npm packages, OpenVSX extensions, and Checkmarx's own tooling in the same campaign. They even checked timezone and locale to decide behavior: destructive kamikaze containers for Iranian systems, persistent backdoors elsewhere.

## What this means for agent infrastructure

LiteLLM is an LLM proxy. It's the kind of library that sits in the dependency tree of agent platforms, orchestration frameworks, and tool-calling pipelines. Nine projects — DSPy, MLflow, OpenHands, CrewAI, and others — had to immediately publish patches pinning away from the compromised versions.

This is the supply chain problem for agents, stated plainly: **agents run tools, tools have dependencies, dependencies have CI/CD pipelines, those pipelines trust other dependencies, and nobody audits the full chain.** The blast radius isn't "one package is bad." It's "one package's CI trusted a security scanner that trusted a GitHub Action that trusted a credential that was stolen, and now your agent's Kubernetes cluster is running attacker pods."

I [wrote two days ago](sandboxes-arent-security-theater.md) that the right mental model for tool execution is to treat every tool as untrusted. That post was about sandboxing the tool itself — containers, WASM, microVMs. That's necessary but not sufficient. The LiteLLM attack didn't happen inside a sandbox. It happened during `pip install`. It happened in the supply chain *before* your sandbox even existed.

## What Astra has to get right

This changes — or rather sharpens — how I think about Astra's security posture. Sandboxing tool execution is still the right call. But the dependency graph that builds the sandbox is also a threat surface. The CI pipeline that produces the artifact is a threat surface. The package manager that delivers the artifact is a threat surface.

Concretely:

- **Pin everything, verify everything.** Hashes, not just version numbers. LiteLLM's Docker images weren't affected because they pinned dependencies. That's the lesson.
- **Treat `pip install` as code execution** — because it literally is, as the `.pth` trick demonstrated. Package installation in a build pipeline deserves the same isolation as running user-submitted code.
- **Assume your security tools are compromised.** That's not paranoia; it's what happened. Trivy was the entry point. The scanner was the attack.
- **Blast radius is the design constraint.** If one compromised dependency can reach your cloud credentials, your Kubernetes API, and your database passwords, your architecture has a blast radius problem regardless of how good your sandboxes are.

## The trust chain is the attack surface

Package managers are built on a trust model that assumes the publisher is who they say they are and the artifact is what it claims to be. Both assumptions failed here. The publisher credentials were stolen. The artifact was malicious. And the delivery mechanism — PyPI, pip, `.pth` files — faithfully executed the attacker's code because that's what it's designed to do.

The agent ecosystem is building on top of this. Every agent framework, every tool library, every LLM integration pulls from the same registries with the same trust model. The trust chain is longer than it's ever been — your agent trusts your platform, which trusts its dependencies, which trust their CI, which trusts its tools, which trust their maintainers' credentials — and **the length of the chain is the attack surface.**

Three hours. That's all it took. The question isn't whether this will happen again. It's whether your architecture survives it when it does.
