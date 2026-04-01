---
title: What electronics taught me about debugging software
date: 2025-11-20
description: Oscilloscopes, multimeters, and tracing signals through a circuit — the hardware debugging mindset that transfers directly to distributed systems debugging.
authors:
  - prashanth
categories:
  - Engineering
tags:
  - electronics
  - debugging
  - distributed-systems
draft: false
---

The most useful debugging skill I have came from a ₹800 multimeter, not a computer science curriculum. I learned it staring at a circuit that wasn't working — a 555 timer that wouldn't oscillate — probing test points, measuring voltage drops, eliminating possibilities one leg at a time until I found the resistor I'd put in backwards. The whole process took 40 minutes. It's the same process I use to debug distributed systems. **The domain changed. The discipline didn't.**

<!-- more -->

## The multimeter is the original console.log

Except it's better, because it forces you to decide where to measure before you measure. You can't probe every wire simultaneously. You have to form a hypothesis — "the signal dies somewhere between the power rail and pin 3" — and then verify it with a physical probe at a physical location. That selectivity is a skill. `console.log("here")` everywhere is not debugging. It's thrashing.

In software, the equivalent discipline is: **before you add any logging or breakpoint, state what you think is wrong and where the evidence should be.** The engineers I've seen who are fast at debugging do this automatically. They walk to the whiteboard, draw the system, and point to two or three places where the failure would be visible if their hypothesis is correct. Then they go look there. They don't grep the entire codebase for likely-looking errors.

## What an oscilloscope taught me about distributed tracing

A multimeter gives you a voltage at a moment in time. An oscilloscope gives you the *shape* of a signal — rising edges, ringing, timing jitter — over a window of time. The difference matters. A PWM signal that looks like 3.3V on a multimeter might be 5V spikes that are destroying your logic chip. You only see it on the scope.

This is exactly the distinction between a log line and a trace span. A log line says "the request arrived" — point in time. A trace span says "here's the full latency profile, here's where it waited, here's where it ballooned." A system that looks healthy in spot-check logs can be silently accumulating tail latency that a histogram would have caught immediately. **The instrument has to match the frequency of the problem.** A slow multimeter cannot tell you about fast transients. A sampling-rate-limited metric cannot tell you about a latency cliff that affects only the 99th percentile.

## Systematic elimination

In a broken circuit, you don't start by replacing chips. You start by checking power — is the supply rail at the right voltage? Then you check the signals flowing into the component you suspect. Then you verify the output. You work from known-good ground toward the failure, narrowing the blast radius. The chip is almost never bad. It's the solder joint, the voltage reference, the capacitor you estimated wrong.

In software, the equivalent protocol:

1. **Check connectivity first.** Is the service reachable? Can it connect to its dependencies? Before you read a single line of business logic code, verify the basic plumbing. I've watched engineers spend three hours debugging application behavior that turned out to be a misconfigured DNS entry.
2. **Check data flow.** Is the right data arriving? Is it in the expected shape? A lot of "logic bugs" are actually schema mismatches one hop back in the pipeline.
3. **Check business logic last.** This is where you expect to spend your time. This is usually not where the problem is.

The instinct to jump straight to "the code is wrong" is the hardware equivalent of "the chip is bad." It's almost never the chip.

## Ground truth is non-negotiable

A multimeter doesn't have opinions. It reports voltage. You can theorize all you want about what the voltage *should* be — the meter reports what it is. This sounds obvious until you watch someone spend an hour arguing with a system based on what they think it's doing, rather than measuring what it's actually doing.

"I think the API is returning 200" is the distributed systems equivalent of "I think the voltage is 3.3V." Measure it. A packet capture, a curl with verbose output, a database query that bypasses the ORM — these are your probes. **The gap between what you believe the system does and what it actually does is exactly where bugs live.** The entire job of debugging is closing that gap, and you close it with measurements, not reasoning.

## Isolation: removing components until it works

Standard technique for a malfunctioning circuit: start removing components. Desolder things. Bypass sections. Find the minimal configuration that either exhibits the fault or doesn't — now you've localized the problem to a known region.

In a distributed system, you disable services. You swap a real dependency for a stub. You replay a failing request against a single service in isolation. Same principle: **shrink the search space until the failure has nowhere to hide.** Engineers who've never done hardware work tend to be reluctant to do this — it feels destructive, or like cheating. It's neither. It's systematic.

## Schematics are architecture diagrams

Reading a schematic is a skill — following power rails, tracing signal paths, understanding what's connected to what and why. It's exactly the skill of reading an architecture diagram. The practice of following a signal from a voltage source through a transistor to a load output is the same cognitive motion as tracing a request from an API gateway through a queue to a worker. You're asking: **where does the data come from, what transforms it, where does it go, where could it get lost?**

The engineers who are good at both tend to have a bias toward *drawing the system* before debugging it. Not because the diagram solves the problem, but because drawing forces you to articulate what you know and where your mental model has gaps. The gaps are where you probe first.

## The thing electronics forces you to give up

You can't `git blame` a resistor. You can't add a retry loop to a broken solder joint. You can't deploy a hotfix to a board that's drawing 400mA when it should draw 40mA. Electronics removes every abstraction ladder you've learned to climb in software and puts you face-to-face with physical reality. Either the circuit works or it doesn't. The multimeter is the referee and it doesn't care what you intended.

That forced humility — *measure, don't guess* — is the most transferable thing I've gotten from hardware. It's also the thing that software development's tooling actively works against, by making it easy to add more logs, more assertions, more observability, without ever requiring you to form a precise hypothesis first.

Every software engineer should own a multimeter. Not because they'll need to debug circuits. Because it teaches you what debugging actually is — and it's not adding print statements until something looks different.
