---
title: "My first RC car build: an engineer's guide to pain in India"
date: 2026-02-08
description: Approaching RC cars like a software person — choosing a platform, brushless ESCs, LiPo safety, and the uniquely Indian challenge of getting parts at all.
authors:
  - prashanth
categories:
  - DIY
tags:
  - rc-cars
  - electronics
  - india
  - hobby
draft: false
---

Every engineer I know has a version of this story: you spend years building things that exist entirely as state in someone else's datacenter, and eventually the itch to make something *physical* — something that moves, crashes, and requires a screwdriver — becomes impossible to ignore. For me it was RC cars. Specifically, a 1/10 scale short course truck that I decided to source, build, and run in India, which turns out to be its own distributed systems problem.

<!-- more -->

## The import situation is exactly as bad as you think

Let me start with the thing nobody mentions in the YouTube build videos: **Traxxas, Arrma, and Team Associated do not have official distribution in India.** Hobby-grade RC — as opposed to the toy-grade stuff that runs on AA batteries and tops out at 15 km/h — is a niche import market. Your local hobby shop, if one exists near you at all, stocks boat models and maybe some airplane kits. The good stuff arrives in a suitcase or through customs.

Customs is where the adventure begins. Import duty on RC equipment lands somewhere between 30% and 80% depending on how it gets classified — "toys," "electronic components," and "motor vehicle parts" are all plausible categories, and the outcome varies by shipment, by port, by the customs officer's disposition that morning. A $300 Traxxas Slash, before you've touched a wheel to pavement, can become a ₹35,000 problem. I have seen this happen to people. I decided not to test it.

The practical options for an Indian hobbyist in 2026: AliExpress (3-6 week shipping, reasonable duty most of the time), Banggood (similar), and HobbyKing's India warehouse (spotty inventory but air-shipped pricing without the import lottery). Amazon India has RC equipment at markups that suggest the sellers have factored in three years of warehouse rental into the price.

My starting platform was the Wltoys 104001 — a 1/10 scale brushed short course truck available domestically, designed for upgrade, and cheap enough that learning to crash it doesn't sting. Not a competition rig. A sensible first chassis.

## Brushless, brushed, and why it matters

The first upgrade decision everyone faces: brushed motor or brushless. Brushless is faster, more efficient, and more controllable at high speed. It's also — once you factor in a brushless motor, a compatible ESC, and Indian import pricing — roughly twice the cost of a brushed setup.

I started brushed. This was the right call. Brushed motors fail gracefully and are simple to diagnose. **A good ESC matters more than a fast motor** — the ESC is doing the actual work of converting your trigger input into three-phase current management, and a cheap ESC with a fast motor is how you get thermal shutdowns on the second run. The Hobbywing Quicrun series is the standard recommendation for a reason: programmable, reliable, and available through channels that don't require a customs gamble.

When I eventually move to brushless — and I will, probably on a 1/10 buggy build — I'll spend the money on the ESC first and let the motor be the variable.

## LiPo: the part where it gets serious

LiPo batteries cannot be shipped by air. This is not a suggestion — airlines refuse them above a certain capacity. Which means your LiPo sourcing options in India are: local RC hobby shops (Bangalore and Mumbai have a few), domestic online sellers with inconsistent quality, or NiMH in the interim.

The quality variance in local LiPos is real. I've seen cells that puff after three charge cycles and cells that are still performing a year in. **A LiPo bag is not optional** — it's the cheapest insurance you can buy against a battery failure becoming a room-on-fire situation. Storage charge is also not optional: leaving a LiPo at full charge kills capacity faster than any number of discharge cycles. These are the two rules that experienced hobbyists will repeat until you're tired of hearing them, and they're right.

My charger is an iSDT Q6 Plus. It's programmable, it does balance charging, and it was imported — but it's small enough that it arrived without triggering anyone's interest.

## The spare parts lesson

Software engineers are used to dependency resolution happening instantly. `gem install` or `npm install` and you have the thing in seconds. Hardware doesn't work like that, and India makes it slower.

When a $4 steering link snaps on a Saturday afternoon — and it will, because that's what steering links do — you cannot Amazon Prime a replacement. The nearest shop that stocks it might be in another city. The AliExpress order is three weeks out. **You learn to order spares before you need them.** Two steering links, two servo savers, a spare pinion, a spare spur gear. The redundancy that distributed systems people build into infrastructure, applied to a box of small plastic parts.

This is actually the most useful mental shift the hobby forced on me: planning for failure as a steady state rather than an exceptional event.

## The PID parallels nobody warned me about

I was not expecting RC car tuning to feel like control systems work. It does. Throttle curves, steering trim, ABS braking threshold, punch control — a programmable ESC gives you more dials than you'd expect, and the interaction between them is non-obvious.

The experience of tuning a throttle curve to eliminate wheel spin off the line maps almost exactly to tuning a PID controller: you know the desired behavior, you can observe the actual behavior, and there's a set of parameters between them that you adjust iteratively. Overshoot, oscillation, underdamped response — the vocabulary is the same. **The car behaves like a system,** which shouldn't surprise anyone, but did surprise me.

The community helps here. The RC hobbyist groups in India — WhatsApp groups, a few dedicated forums, weekend meetups in Bangalore and Chennai — are small but generous with knowledge. Someone has already hit every tuning problem you're going to hit, and they'll tell you the answer if you ask.

## Why it's worth it

I could buy a pre-built car. I could also use a managed Kubernetes service and never think about what's underneath. Both are valid choices, and both involve giving up something.

What the build gives you is the same thing it always gives you: the satisfaction of understanding the system end to end. Every part I sourced, every servo I replaced, every LiPo I safely charged and stored — it's earned in a way that `git push` never quite captures.

The hobby is rewarding *because* it's hard. The India parts problem is part of the hobby.
