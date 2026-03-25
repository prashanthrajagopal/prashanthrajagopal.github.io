---
title: What Rails taught me about supervision
date: 2026-03-24
description: Puma, Sidekiq, and the art of not staying dead — how a decade of Rails taught me that restart is the first answer, not the last resort.
authors:
  - prashanth
categories:
  - Rails
tags:
  - ruby
  - rails
  - astra
  - actors
draft: false
---

I wrote Ruby professionally for years. Rails paid rent, taught me opinions, and — this is the part nobody puts on their resume — taught me what happens when processes die and something has to decide what to do about it. Before I ever read an Erlang paper or typed the word "supervisor," Rails had already shown me the shape of the problem. It just called it something else.

<!-- more -->

## Puma, Sidekiq, and the art of not staying dead

Here's what Rails gets right that most frameworks never think about: the assumption that your code *will* crash. Not might. Will. Puma forks workers and watches them. Sidekiq runs jobs and retries them. The whole ecosystem is built on the premise that **failure is a runtime event, not an engineering failure.**

That sounds obvious in 2026. It wasn't obvious to me in my first year writing Rails. I thought the goal was to write code that didn't crash. Rails taught me the goal is to write *systems* that handle crashes as business logic. A Sidekiq retry isn't a bug — it's a policy.

## The supervisor pattern was hiding in plain sight

When I started building Astra's actor model, I needed a supervision strategy: what happens when an actor panics? What happens when it wedges on a bad message? Do you restart it? Kill it? Escalate?

I went and read the OTP documentation. I looked at Akka. Both are good. But the intuition — the *feel* for how supervision should work — came from years of watching Rails processes get bounced by Puma, watching Sidekiq move jobs to the dead queue after five retries, watching Capistrano restart a deploy that timed out.

None of that is formally a supervisor tree. All of it is supervision. Rails taught me:

- **Restart is the first answer**, not the last resort. If a worker dies and the state is recoverable, bring it back. Don't page someone. Don't log an alert that nobody reads. Restart.
- **Bounded retries are a kindness.** Infinite retries are a denial-of-service attack you run on yourself. Sidekiq's dead queue exists because some failures are not transient — they're a conversation you need to have with the code.
- **Isolation between workers is non-negotiable.** One slow Puma worker doesn't block the others. One stuck Sidekiq job doesn't hold the queue. The workers don't share fate. This is the entire point.

## From workers to actors

Astra actors are not Rails workers, but they rhyme. An actor has a mailbox (a channel), a processing loop (the handler), and a lifecycle that something else manages. When I designed how the kernel supervises actors, I kept asking a very Rails question: **what would Sidekiq do?**

Actor panics on a message? Catch the panic, log it, keep the actor alive. That's a retry without the retry — the actor doesn't re-process the bad message, but it doesn't die either. The mailbox keeps moving.

Actor is stuck — hasn't processed a message in longer than its timeout? That's a wedged worker. Kill it, restart it, let the next message have a clean goroutine. Don't wait for a human.

Actor hits a fatal state — database gone, credentials expired, something structural? Escalate. Stop restarting. That's Sidekiq's dead queue: an admission that automation has limits and someone with a keyboard needs to look at this.

## The thing Rails got wrong (and Erlang got right)

Rails supervision is *flat*. Puma watches workers. Sidekiq watches jobs. Nobody watches Puma watching workers — that's systemd's problem. There's no hierarchy.

Erlang showed me that supervision trees are the right idea: supervisors that watch supervisors, with restart strategies at every level. Astra borrows that structure. The kernel supervises actors. A higher-level orchestrator can supervise groups of actors. If an entire agent (which might be multiple actors) enters a bad state, the orchestrator can tear it down and rebuild it without touching anything else.

I couldn't have designed that without OTP's influence. But I wouldn't have *trusted* it without Rails teaching me, year after year, that restarting things is fine. Better than fine. It's the default.

## Why this matters for agent infrastructure

Agents are going to crash. Your LLM call will timeout. Your tool sandbox will OOM. Your planner will produce a graph that references an actor that doesn't exist anymore. This is not speculation — it's Tuesday.

The systems that survive are the ones where crashing is a handled case, not a surprise. Rails knew this about web requests twenty years ago. Erlang knew it about telecom switches forty years ago. Agent infrastructure is just now learning it, and too many platforms treat a crashed agent as a fatal error instead of a restart opportunity.

Astra doesn't pretend agents won't fail. It gives them supervisors. That decision traces back, through a decade of Erlang reading, through OTP design docs, all the way to watching a Puma worker segfault at 2am and come back three seconds later like nothing happened.

Thanks, Rails. I owe you more than I usually admit.
