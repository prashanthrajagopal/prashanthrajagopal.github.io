---
title: "Runbook — LLM Cost Spike"
tags:
  - astra
  - operations
  - runbook
  - cost
---

# Runbook — LLM cost spike

**Trigger:** LLM **cost** or **token** rate far above baseline (dashboard / alert).

## Symptoms

- Sudden jump in **premium** model usage or **token** volume.  
- Specific **agents** or **workloads** dominating spend.

## What operators do (summary)

1. **Identify** whether traffic is **legitimate** (launch, batch job) or **abuse / bug**.  
2. **Throttle:** apply **tier downgrade**, **concurrency limits**, or **per-agent quotas** per **internal ops guide** (env / config changes not listed here).  
3. **Cache:** confirm **response cache** is healthy so repeat prompts aren’t re-billed.  
4. **Verify** spend returns to baseline; **escalate** product if policy change is needed.

!!! note
    **Exact env vars and kubectl commands** are internal-only.
