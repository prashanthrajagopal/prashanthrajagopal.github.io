---
title: Scheduling without losing your mind
date: 2026-03-24
authors:
  - prashanth
categories:
  - Astra
tags:
  - scheduling
  - distributed-systems
  - astra
  - architecture
draft: false
---

Scheduling is the part of a system where optimism goes to die. On paper, it's simple: you have work, you have workers, assign the former to the latter. In practice, it's a swamp of partial failures, stale heartbeats, uneven load, and the quiet dread of realizing your scheduler just assigned a task to a node that died forty seconds ago but hasn't been declared dead yet.

<!-- more -->

## The problem is not assignment

Most people think scheduling is the assignment problem. It's not. Assignment is a function call: given work W and workers {A, B, C}, pick one. You can round-robin it, hash it, score it, or throw a dart. The assignment itself is cheap.

The hard parts are everything around the assignment:

- **Liveness.** Is worker B actually alive, or is it just slow? Heartbeats tell you what was true a few seconds ago. The gap between "last heartbeat received" and "actually dead" is where duplicate execution lives.
- **State after assignment.** You assigned task T to worker B. B acknowledged. Then B's process died between acknowledgment and execution. Who knows? Who retries? How do you avoid running the task twice?
- **Load awareness.** Worker A has three tasks. Worker C has three hundred. Your round-robin doesn't know and doesn't care. Now A is idle and C is backpressuring into the queue.
- **Ordering and dependencies.** Task T2 depends on T1. T1 is running. Do you enqueue T2 now and let the worker block? Or do you hold T2 in the scheduler until T1 completes? Both answers are wrong in different ways.

## Heartbeats: necessary, insufficient, annoying

Astra uses heartbeats because there is no alternative that's both simple and honest. Workers send periodic pings. The scheduler tracks last-seen timestamps. If a worker misses enough heartbeats, it's presumed dead and its tasks are eligible for reassignment.

The tuning is where you lose your mind:

- **Heartbeat interval too short?** You're generating noise. Network hiccups look like deaths. The scheduler spends more time processing heartbeats than scheduling work.
- **Heartbeat interval too long?** A dead worker holds tasks hostage for seconds or minutes. The system looks alive in the dashboard but work isn't moving.
- **Threshold too aggressive?** Healthy-but-busy workers get declared dead because they were 200ms late on a heartbeat while processing a heavy task.
- **Threshold too generous?** Actually-dead workers keep their task assignments while the scheduler politely waits for a response that will never come.

There's no perfect setting. There's a setting that matches your tolerance for false positives (unnecessary reassignment) vs false negatives (stuck tasks). I've landed on a heartbeat interval that's short enough to detect real failures within a few seconds and a threshold that tolerates brief network jitter without panicking.

## Sharding the scheduler

A single scheduler is a single point of failure and, eventually, a bottleneck. Astra's design shards scheduling by partition — each shard owns a subset of the work and the workers assigned to it. Shards are independent; a failure in shard 2 doesn't affect shard 1.

The tricky part is rebalancing. When a shard fails, its work needs to be redistributed. When a new shard comes online, it needs to pick up a portion of the load. This is a consensus problem wearing a scheduling costume, and I've treated it as such — shard assignment is coordinated through Postgres (the source of truth, as always) rather than through a gossip protocol that might eventually agree.

Is it slower than gossip? Yes. Do I wake up at 3am because two shards both think they own the same partition? No.

## At-least-once is the only honest guarantee

You will run a task twice. Accept it.

The question isn't whether duplicates happen — it's whether your system handles them gracefully. Astra's task execution is designed for at-least-once delivery with idempotency at the handler level. The scheduler might assign a task that's already running if a heartbeat was late. The task runner checks execution state before starting, and the handler is expected to tolerate being called again.

Exactly-once is a distributed systems unicorn. People claim it in whitepapers and disclaim it in production postmortems. At-least-once with idempotent handlers is less elegant on a slide and more honest in an incident review.

## Load shedding is not optional

A scheduler that accepts all work unconditionally is a scheduler that will eventually drown. Astra implements backpressure at the queue level — when a shard's pending queue reaches capacity, new submissions get a explicit rejection rather than a silent enqueue into an ever-growing list.

This feels wrong the first time you implement it. Rejecting work? Sending back errors? But the alternative is worse: accepting work you can't process, growing memory unboundedly, and eventually crashing — at which point you've rejected *all* work, not just the overflow.

Backpressure is honesty. "I can't do this right now" is a better answer than "sure" followed by silence.

## The part where you don't lose your mind

Scheduling becomes manageable when you stop pretending it's a solved problem and start treating it as an ongoing negotiation between your system and reality. The scheduler doesn't know the future. It doesn't know if a worker will die in three seconds. It doesn't know if the next task will take 10ms or 10 minutes.

What it can do is make reasonable decisions with current information, detect when those decisions were wrong, and correct them quickly. That's it. That's the whole job.

Build for that, and you'll keep your mind. Build for perfection, and the 3am pages will take it from you.
