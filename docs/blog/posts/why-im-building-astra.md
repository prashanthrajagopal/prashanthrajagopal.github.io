---
title: Why I'm building Astra
date: 2026-03-09
authors:
  - prashanth
categories:
  - Astra
tags:
  - astra
  - agents
  - architecture
draft: false
---

I'm Prashanth. I've been building software for north of fifteen years — mostly the kind that has to work when you're asleep. Rails paid a lot of my rent. I've written Go, Python, Java, TypeScript, Rust, and whatever else the problem demanded. If I had to pick one language to ride into the sunset with, it's still Ruby. The others are tools; Ruby is the one I argue about at parties.

This blog exists because I got tired of only *thinking* in commits. Too many apps, too many 2am incidents, and nowhere near enough written down. So here we are.

<!-- more -->

## What I'm actually building

**Astra** is a personal project. Not a side hustle with a pitch deck — the kind of thing you build because you can't stop thinking about the shape of the problem.

The observation that stuck: we've got agents everywhere now. Clever ones, dumb ones, ones that write code and ones that summarize your inbox. What we *don't* have is a serious place for them to *run*. A real substrate. Something that treats agents like processes, schedules work like an OS schedules threads, and doesn't fall over the moment you want more than a demo.

So Astra is that gap, filled in. Microkernel-style core: actors, messages, a task graph that actually behaves like a DAG under load, sandboxes for tools, memory and routing layered on top. The bar I'm holding it to is almost unfair — hot-path reads in single-digit milliseconds, scheduling that doesn't embarrass itself at scale, room to extend without rewriting the world.

**Quick.** Not "fast enough for a slide deck" — fast enough that you don't redesign your product around latency.

**Scalable.** Planet-scale is a phrase people throw around. I'm building like I mean it: sharded queues, state that doesn't live in one sad Postgres row, the boring distributed-systems homework.

**Extensible.** Kernel does a small set of things well; everything else plugs in. That's the point. If your agent platform is a monolith with a JSON API, you don't have an OS — you have a server with opinions.

## Why personal

Because nobody was going to fund "operating system for agents" as a weekend curiosity, and because I wanted the design to stay honest. No roadmap theater. If Astra ships something, it's because the architecture demanded it, not because a quarter needed a feature bullet.

I'll write here as I go — architecture calls, things that broke, things that surprised me. If you're building in the same neighborhood, maybe it'll save you an all-nighter. If not, at least the record's on paper.

Thanks for reading. More soon.
