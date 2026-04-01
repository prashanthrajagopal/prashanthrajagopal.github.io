---
title: Dead letters are a feature, not a failure
date: 2026-03-11
description: Designing for task exhaustion with dead-letter queues and retry budgets makes your system more honest than pretending everything succeeds.
authors:
  - prashanth
categories:
  - Astra
tags:
  - astra
  - reliability
  - distributed-systems
draft: false
---

I've worked on systems that swallowed failures whole. Job would fail, get retried, fail again, and somewhere around retry number forty the queue processor would quietly stop complaining and move on — or it wouldn't, and you'd come back on Monday to find a queue depth in the millions and a team meeting nobody wanted to have. Both outcomes were presented as *normal*. "Eventual consistency," one team called it. What they meant was "we don't know where the bodies are."

Astra does it differently. When a task exhausts its retry budget, it goes to `dead_letter` status — explicitly, permanently, and visibly. That's not a failure mode. That's the system being honest.

<!-- more -->

## The lie retrying forever tells

Most distributed systems have two unofficial failure modes: retry until it works, or drop it and pretend it never happened. The first one masquerades as resilience. The second one masquerades as fire-and-forget.

Both are lies. Retrying forever isn't resilience — it's *denial*. You're asserting, with each retry, that this task will eventually succeed, even as you accumulate zero evidence for that belief. At some point the thing failing is not experiencing a transient error. It's hitting a permanent condition: malformed input, a downstream service that no longer exists, a permission that was revoked, a schema that changed. **No amount of waiting turns a structural failure into a transient one.**

Dropping it silently is worse. At least infinite retry tells you something is stuck. Silent drop tells you nothing. You ship code, watch your success metrics, and wonder why customer data keeps going missing. The failure happened — you just don't have a record of it.

## What Astra does instead

Every task in Astra has a per-message retry count. The scheduler tracks how many times a given message has been delivered without successful acknowledgment. When that count exceeds the budget, the task doesn't retry — it transitions to `dead_letter` status and gets written to the `astra:dead_letter` Redis stream.

The `XAck` only happens on handler success. This is the critical part. A handler that panics, returns an error, or times out does not acknowledge the message. Redis Streams' `XAUTOCLAIM` picks it back up for reassignment. If a worker dies mid-execution — process crash, OOM, someone tripping on a power cable — the message stays in the pending entries list until the claim timeout expires, then gets claimed again. The at-least-once guarantee is enforced by the stream mechanics, not by optimistic hoping.

When the retry budget is exhausted, the task doesn't just get marked and forgotten. The `astra:dead_letter` stream exists specifically for two things: **alerting** and **repair**. A subscriber to that stream can notify on-call, write to a dashboard, trigger a human review workflow, or feed the dead letter back into the live queue once the underlying problem is fixed. The dead letter is data. It tells you what broke, how many times, and approximately when.

## Why explicit dead-letter status matters

There's a design instinct that says: only surface failures that need immediate action. Hide the rest. Keep the dashboard green. This instinct feels like product polish and is actually just delayed pain.

When I introduced explicit `dead_letter` status in Astra's task model, the temptation was to call it something softer. "Exhausted." "Parked." Something that didn't make it sound like the task had failed irrecoverably. I kept `dead_letter` because the word is accurate. **The task is dead. It's in a letter box. Someone needs to read it.**

Naming it correctly changes how you operate it. "Dead letter" implies a queue, a reader, an action. "Eventually consistent" implies waiting. One of those produces engineers who fix root causes; the other produces engineers who shrug and say it'll probably sort itself out.

## The comparison that stings

I've seen message queue setups where the retry policy was effectively infinite, implemented as an exponential backoff with a max delay of twenty-four hours and no max attempt count. The team defended it because "eventually the downstream service comes back up." Which is true, sometimes. But some of those messages were malformed on day one. They'll be retrying in a queue somewhere, slowly, for as long as the service runs — **contributing zero value while consuming scheduler cycles and queue capacity**.

I've also seen the other extreme: a task runner that silently discarded jobs after three failures, with no logging beyond the initial error. The system *looked* healthy. The queue was clear. We discovered the problem six weeks later when someone noticed the derived data it was supposed to generate had been stale for a month and a half. No alerts. No dead-letter stream. No trace.

Neither of those systems was honest. They were just misconfigured in opposite directions.

## The operational posture this enables

Having an explicit dead-letter stream means you can answer questions you couldn't answer before:

- What percentage of tasks are exhausting their retry budget in a given hour?
- Is the dead-letter rate spiking after a deploy? (Probably a schema change.)
- Which task types are dying at the highest rate? (Probably a leaky abstraction downstream.)
- Can I replay these dead letters after the fix ships?

That last one matters more than it sounds. If your dead letters are gone — either because you swallowed the error or because your system had no concept of permanent failure — you've lost the work. If they're in a stream, you can fix the root cause, write a replay consumer, and recover. The dead letter is a checkpoint, not a tombstone.

Designing for task exhaustion isn't pessimism. It's acknowledging that some tasks will fail for reasons outside your control, that you want a record when they do, and that "we'll know about it when the data goes missing" is not a monitoring strategy.

The honest system admits what it doesn't know. The dead-letter queue is where it puts those admissions.
