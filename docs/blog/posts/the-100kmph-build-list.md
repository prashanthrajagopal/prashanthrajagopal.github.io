---
title: "The 100km/h build list: every part I'm buying"
date: 2026-04-02
description: Follow-up to my first RC car post — the complete component list for a 1/8 scale brushless desert buggy that should hit 100km/h, sourced entirely from India.
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

I wrote about [the pain of getting RC car parts in India](../rc-cars-and-the-india-parts-problem/) a couple of months ago. The response was surprisingly warm — turns out a lot of engineers in India have the same itch and the same frustration with sourcing. Since then, I've gone deep. Research phase is over. I've picked every component for a **1/8 scale desert buggy that should touch 100km/h**, and I'm publishing the full list here because nobody else seems to have written this down for the Indian market.

<!-- more -->

## The platform: FS Racing ATOM 6S

After weeks of comparing the Arrma Typhon 6S (₹45,000+ imported, spares nonexistent in India), the ZD Racing 9116 (affordable but the drivetrain is made of hopes), and various WLtoys options (toy-grade dressed as hobby-grade), I landed on the **FS Racing ATOM 6S 1/8 4WD Desert Buggy**.

**Why this one:**

- **100km/h rated out of the box** with its stock Hobbywing 4274 2000KV motor and 150A ESC — no immediate electronics upgrade needed
- **AL6061-T6 aluminum chassis** — not plastic pretending to be metal
- **Hobbywing electronics from the factory** — the motor and ESC are legitimate, not white-label clones. Same 4274 motor the Arrma Typhon uses
- **Oil-filled aluminium shocks** — critical at speed; cheap shocks at 100km/h is how you break everything at once
- **Umbrella gear differentials** — better durability under load than bevel gears
- **Available in India** via [Bharat Hobby](https://www.bharathobby.com/) and [AliExpress](https://www.aliexpress.com/) — Bharat Hobby is a legitimate Indian RC retailer with actual customer support

The ATOM 6S ships RTR (ready to run) but **without batteries** — which is actually what you want, because the stock battery connector situation is always worth replacing anyway.

## Power: 6S LiPo

100km/h on 1/8 scale requires **6S voltage (22.2V)**. You can run two 3S packs in series or a single 6S pack. I'm going with two 3S packs because they're easier to source, charge, and replace in India.

**Batteries: 2× Gens Ace 3S 5000mAh 60C LiPo (Hard Case)**

- [Available on Amazon.in](https://www.amazon.in/Gens-ace-5000mAh-Battery-T-REX550/dp/B06Y4BRD2B) — Gens Ace has decent India distribution
- **Hard case is non-negotiable** — a pouch LiPo at 100km/h in a crash is a fire waiting to happen
- **60C continuous discharge** means 300A burst capacity — more than the 150A ESC will ever draw
- **XT90 connectors** — I'm re-soldering everything to XT90 for the current handling. XT60 is marginal at 6S loads
- Two packs wired in series via an XT90 series adapter

**Why Gens Ace:** Consistent quality, available in India without import roulette, and the hard case packs have proper balance leads. I looked at CNHL (cheaper, decent reviews) but availability on Amazon.in is spotty and I don't want to wait 6 weeks for AliExpress shipping on something that can catch fire.

## Radio system: RadioLink RC6GS V3

The stock radio that comes with the ATOM 6S works, but it's basic. I'm upgrading to the **RadioLink RC6GS V3**.

- [Available on Robu.in](https://robu.in/brand/radiolink/) — Robu is the most reliable Indian RC electronics retailer I've found
- **6-channel, 2.4GHz FHSS** — overkill for a car, but the extra channels are useful later for lights, winch, etc.
- **Built-in gyro receiver** — stability assist at high speed is not cheating, it's survival
- **400m range** — you'll never need this, but the signal quality at closer range is what matters
- **Ergonomics** — the pistol grip is genuinely comfortable, which matters when you're trimming throttle curves

**Why not FlySky:** The GT5 is cheaper but the firmware update process is painful, and RadioLink's gyro receiver (R7FG) is better integrated. At this speed, the radio is the last thing you want to cheap out on.

## Servo upgrade: Savox SV-1270TG

The stock 15kg servo on the ATOM 6S is adequate for bashing but marginal at speed. At 100km/h, steering response needs to be instant.

- Available on [Amazon.in](https://www.amazon.in/) — search "Savox SV-1270TG"
- **35kg torque at 7.4V** — massively over-specced, which means it won't struggle
- **0.11s/60° transit time** — fast enough that the car responds before your brain does
- **Titanium gears** — steel strips under shock loads; titanium handles the impact cycles
- **Coreless motor** — smoother, more precise centering than brushed servos

**Why not a cheaper servo:** I've already broken one ₹800 servo on a WLtoys at 40km/h. At 100km/h, a servo failure means the car goes straight — into whatever is in front of it. The Savox is insurance.

## Charger: SkyRC B6neo

You cannot run 6S LiPo without a proper balance charger. Period.

- [Available on Amazon.in](https://www.amazon.in/) — search "SkyRC B6neo"
- **200W output** — charges a 5000mAh 3S pack in about 45 minutes at 2C
- **Balance charging** — monitors each cell individually, stops if any cell drifts
- **Discharge function** — for storage voltage (3.85V/cell), which is how you keep LiPos alive
- **Supports 1S-6S** — handles both 3S packs and any future 6S single-pack upgrade
- **DC input** — you'll need a 12V power supply (I'm using an old laptop brick)

**Why this matters:** A ₹500 charger from Amazon that "supports LiPo" will overcharge a cell, swell the pack, and eventually cause a thermal event. The B6neo is ₹4,000. Your house is worth more.

## Tires: Louise RC 1/8 GT Belted

Stock tires on the ATOM are fine for off-road bashing but **balloon at speed**. At 80+ km/h, an unbelted tire expands from centrifugal force, throws off the balance, and causes violent wobble.

- Available on AliExpress — search "Louise RC 1/8 GT belted tires"
- **Internal Kevlar belt** prevents expansion at high RPM
- **Road-compound rubber** — softer than off-road knobby tires, more grip on tarmac
- **Pre-glued on rims** — saves the nightmare of gluing tires with CA glue (I've glued my fingers together twice)

**Why belted is mandatory:** Unbelted tires at 100km/h is like running unbalanced wheels on a car at highway speed. The physics don't care that it's a toy.

## Gearing: steel pinion set

The stock gearing on the ATOM 6S is tuned for a balance of speed and torque. For 100km/h, I need to gear up — larger pinion or smaller spur.

- **Steel pinion set (18T, 19T, 20T, 21T)** — available on AliExpress for the 32-pitch standard
- Start with stock gearing, measure actual speed with GPS, then step up one tooth at a time
- **Steel, not aluminium** — aluminium pinions wear out in a weekend at this power level
- Monitor motor temperature after each gearing change — if it exceeds 80°C, you've gone too far

## Safety and consumables

This is the stuff nobody lists but everyone needs:

| Item | Why | Source |
|------|-----|--------|
| **2× LiPo safety bags** | Charging and storage containment | [Amazon.in](https://www.amazon.in/) |
| **XT90 connectors (5 pairs)** | Series wiring + replacements | [Robu.in](https://robu.in/) |
| **14AWG silicone wire (2m red, 2m black)** | Re-wiring battery leads | [Robu.in](https://robu.in/) |
| **Hex driver set (1.5, 2.0, 2.5, 3.0mm)** | Every screw on the car is hex | [Amazon.in](https://www.amazon.in/) |
| **Thread-lock (blue, medium)** | Vibration loosens everything at speed | [Amazon.in](https://www.amazon.in/) |
| **CA glue (medium viscosity)** | Tire repairs, body shell fixes | Local hobby shop |
| **GPS speed meter** | Verify actual speed, not motor RPM estimates | [Amazon.in](https://www.amazon.in/) — search "RC GPS speed meter" |

## Spare parts strategy

This is the lesson from [my first post](../rc-cars-and-the-india-parts-problem/): **order spares before you need them**. When something breaks at 100km/h (not if — when), you don't want to wait 4-6 weeks for AliExpress.

First-break parts to pre-order:

- **2× front and rear suspension arms** — the first thing that snaps on impact
- **1× steering assembly** — tie rods and steering links bend on hard crashes
- **1× set of drive shafts** — the drivetrain absorbs crash energy through these
- **2× sets of bearings** — they wear fast at high RPM; cheap and easy to replace
- **1× spur gear** — gearing experiments will wear these out

All available on AliExpress by searching "FS Racing ATOM 6S parts" or the FS Racing part numbers. Order the day you order the car.

## The approach

I'm treating this like a phased rollout — because that's apparently how my brain works now.

1. **Stock run** — assemble, charge, run at stock gearing. Measure baseline speed with GPS.
2. **Tire swap** — belted tires first, re-measure. This alone might add 10-15km/h.
3. **Servo upgrade** — swap in the Savox before pushing speed further.
4. **Gear up** — one tooth at a time, monitor motor temps, re-measure.
5. **Radio upgrade** — once I trust the car, swap the radio for better control feel.
6. **100km/h attempt** — find a long, straight, smooth surface. Probably a disused airstrip or industrial road on a Sunday.

The software engineer in me wants to instrument everything — motor temp, battery voltage under load, GPS traces. The RC car will probably disagree with this plan by cartwheeling into a ditch on run three.

I'll write about how it goes. Or how it went wrong.
