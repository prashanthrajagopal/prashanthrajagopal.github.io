---
title: "The 100km/h build list: every part, every reason"
date: 2026-04-02
description: A full custom 1/8 scale RC buggy built entirely by hand — chassis kit, motor, ESC, batteries, and every bolt chosen individually. The complete parts list for a 100km/h build sourced from India.
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

I wrote about [the pain of getting RC car parts in India](../rc-cars-and-the-india-parts-problem/) a couple of months ago. The conclusion was clear: if you want anything beyond toy-grade, you're importing. Since then I've gone deeper — and in the opposite direction from what most people do. No ready-to-run car. No pre-built electronics. I'm building the entire thing by hand, bolt by bolt, solder joint by solder joint, from a competition chassis kit and individually chosen components.

This is the full parts list for a **1/8 scale 4WD electric buggy that should touch 100km/h**.

<!-- more -->

## Why build from a kit, not buy RTR

An RTR (ready-to-run) car gets you driving in 30 minutes. A kit gets you *understanding* in 30 hours. Every differential you shim, every shock you fill with oil, every gear mesh you set by feel — that's knowledge you'll need the first time something breaks at speed. And at 100km/h, things break.

The other reason: component quality. RTR cars make compromises to hit a price point. A kit lets me choose the motor, ESC, servo, and radio independently — each the best I can get for that slot, not whatever was cheapest in bulk for the manufacturer.

## The chassis: Tekno EB48 2.2

**What:** [Tekno RC EB48 2.2 4WD Competition 1/8 Electric Buggy Kit](https://www.teknorc.com/shop/tkr9005-eb48-2-2-1-8th-4wd-competition-electric-buggy-kit/)

**Why this one:**

- **Comes as a bag of parts** — literally hundreds of pieces. Chassis plates, suspension arms, shock towers, turnbuckles, differentials, drive shafts, bearings, hardware. You build every subassembly.
- **Competition-grade engineering** — this is the eighth iteration of the EB48 platform, refined over a decade of racing. The geometry, weight distribution, and durability are proven at World Championship level.
- **7075-T6 aluminum chassis** and **hard-anodized shock bodies** — not the pot-metal castings you get in budget cars.
- **Three sealed differentials** (front, center, rear) with separate oil weights — tunable for speed vs cornering. I'll start with thinner oil for speed runs.
- **Massive parts ecosystem** — every Tekno part is individually available. When a suspension arm snaps (it will), I order one arm, not a "suspension kit."
- **16mm big-bore shocks** — oil-filled, threaded aluminum bodies. Tuneable spring preload, rebound, and damping.

**Where to buy:** [AMain Hobbies](https://www.amainhobbies.com/tekno-rc-eb48-2.2-4wd-competition-1-8-electric-buggy-kit-tkr9005/p1573353) or [Tekno RC direct](https://www.teknorc.com/shop/tkr9005-eb48-2-2-1-8th-4wd-competition-electric-buggy-kit/). Both ship internationally to India. Also available on [eBay](https://www.ebay.com/sch/i.html?_nkw=tekno+eb48+2.2+kit) from US sellers.

**Important note on AMain Hobbies:** They ship to India but [cannot ship transmitters or vehicles that include transmitters](https://www.amainhobbies.com/shipping-restrictions/i50) — Indian customs refuses them. This is fine for a kit build. The radio system ships separately from an Indian retailer.

## Motor: Hobbywing XeRun 4268 SD G3 2200KV

**What:** [Hobbywing XeRun 4268 SD G3 Sensored Brushless Motor](https://www.hobbywingdirect.com/products/xerun-4268-motor-g3)

**Why this motor:**

- **4-pole sensored brushless** — smooth startup, precise throttle control at low speed, and violent acceleration when you ask for it
- **2200KV on 6S (22.2V)** gives a theoretical no-load RPM of ~48,840 — more than enough for 100km/h with the right gearing
- **Hardened steel shaft, sintered NdFeB magnets** — built for the current and heat of 6S racing
- **Sensor port** — the ESC reads rotor position for buttery-smooth throttle response at all speeds, not just wide open
- **Proven in 1/8 racing** — this is what competition racers run. It's not overkill; it's the baseline.

**Where to buy:** [Hobbywing Direct](https://www.hobbywingdirect.com/products/xerun-4268-motor-g3) ships internationally. Also on [Amazon US](https://www.amazon.com/s?k=hobbywing+4268+G3) with forwarding services.

## ESC: Hobbywing XeRun XR8 Plus G2S

**What:** [Hobbywing XeRun XR8 Plus G2S Brushless ESC](https://www.hobbywingdirect.com/products/xerun-xr8-plus-g2s)

**Why this ESC:**

- **200A burst, 6S max** — handles the full current draw of the 4268 motor without flinching
- **Sensored operation** — pairs with the 4268's sensor port for precise low-speed control
- **Bluetooth programmable** via the Hobbywing app — throttle curves, brake force, drag brake, punch level, timing. No programming card needed.
- **Built-in capacitor module** — voltage spike suppression that cheaper ESCs add externally (or skip)
- **Data logging** — records voltage, current, RPM, and temperature. Engineer brain loves this.
- **Aluminum heat sink with fan** — active cooling matters when you're pulling 150A+ at full throttle on 6S

**Alternative:** The [EZRun Max8 G2S](https://www.hobbywingdirect.com/products/ezrun-max8-esc-g2s) at $120 is a solid budget option — same 6S support, 150A burst, but less tuneable and no sensored mode. If the XR8 Plus is hard to source, the Max8 G2S is the fallback.

**Combo option:** The [XR8 Plus G2S + 4268 G3 Combo](https://www.hobbywingdirect.com/products/xr8-plus-g2s-combo-2-6s) saves money over buying separately and guarantees compatibility.

## Batteries: 2× Gens Ace 3S 5000mAh 60C

**What:** [Gens Ace 5000mAh 11.1V 3S 60C LiPo — Hard Case](https://www.amazon.in/Gens-ace-5000mAh-Battery-T-REX550/dp/B06Y4BRD2B)

Two packs wired in series for **6S (22.2V)**.

**Why this setup:**

- **Two 3S packs instead of one 6S** — easier to source in India, easier to charge, and if one pack degrades you replace half the cost
- **Hard case is mandatory** — at 100km/h, a crash puts enormous force on the battery. Pouch packs deform. Hard case packs survive.
- **60C continuous = 300A burst** — well above what the ESC will pull
- **5000mAh** — enough for 15-20 minutes of mixed driving, or 5-8 speed runs with cool-down between
- **XT90 connectors** — I'm re-soldering both packs and the series harness to XT90. The stock XT60 connectors are marginal at 6S current. This means cutting the factory leads, stripping, tinning, and soldering new connectors — first soldering job of the build.

**Where to buy:** [Amazon.in](https://www.amazon.in/Gens-ace-5000mAh-Battery-T-REX550/dp/B06Y4BRD2B) — one of the few quality LiPo brands with reliable India stock.

## Radio: RadioLink RC6GS V3

**What:** RadioLink RC6GS V3 with R7FG Gyro Receiver

**Why this one:**

- **Must be bought in India** — AMain and most US retailers cannot ship transmitters to India (customs blocks them). RadioLink has Indian distribution.
- **6-channel, 2.4GHz FHSS** — more channels than I need for a car, but the signal quality is what matters
- **R7FG receiver with built-in gyro** — stability assist at 100km/h is not optional, it's the difference between a speed run and a cartwheel
- **Programmable throttle curves** — I can tame the initial throttle response while keeping full power at the top end
- **400m range** — irrelevant for the range itself, but the signal strength at 50-100m (where the car actually is) is rock-solid

**Where to buy:** [Robu.in](https://robu.in/brand/radiolink/) — India's most reliable RC electronics retailer in my experience. Also available on Amazon.in.

## Servo: Savox SV-1270TG

**What:** Savox SV-1270TG High-Voltage Digital Servo

**Why this one:**

- **35kg torque at 7.4V** — massively over-specced for a buggy, which means it won't struggle or burn out under load
- **0.11s/60° transit time** — the car reacts to steering input before your brain finishes the thought
- **Titanium gears** — steel strips under repeated shock loads. Titanium absorbs impact cycles without developing play.
- **Coreless motor** — smoother centering, more precise positioning than brushed servo motors
- **This is the insurance policy.** A servo failure at 100km/h means the car goes straight into whatever is ahead. I broke an ₹800 servo at 40km/h on a WLtoys. Never again.

**Where to buy:** Amazon.in — search "Savox SV-1270TG". Also available via AMain Hobbies (shippable, since it's not a transmitter).

## Charger: SkyRC B6neo

**What:** SkyRC B6neo 200W Balance Charger

- **Balance charges 1S-6S** — monitors every cell individually, stops if any cell drifts
- **200W output** — charges a 5000mAh 3S at 2C in about 45 minutes
- **Storage charge mode** — brings cells to 3.85V for safe long-term storage. This is how you keep LiPos alive.
- **Discharge function** — useful for breaking in new packs
- **DC input** — runs from a 12V power supply (old laptop brick works)

**Where to buy:** Amazon.in — search "SkyRC B6neo".

## Tires: Pro-Line Positron 1/8 Belted

**What:** Pro-Line Positron 1/8 Buggy Belted Tires, Pre-mounted

**Why belted:**

- At 80+ km/h, unbelted tires **balloon** from centrifugal force — the rubber expands outward, throws off the balance, and causes violent speed wobble
- **Internal Kevlar belt** prevents expansion at high RPM — the tire holds its shape
- **Road-compound rubber** — softer than off-road knobby tires, more grip on tarmac where speed runs happen
- **Pre-mounted on rims** — saves the CA glue nightmare (I've bonded my fingers together more than once)

**Where to buy:** [AMain Hobbies](https://www.amainhobbies.com/) — ships to India. Also on AliExpress by searching "1/8 buggy belted tires."

## Body shell: Tekno EB48 clear body

The kit doesn't include a body shell — you buy one separately, then **cut, drill, and paint it yourself**.

- **Clear polycarbonate** — you cut the wheel wells and body posts with curved scissors, drill mounting holes, then paint the inside with Tamiya PS spray paint
- **Painting the inside** means the exterior stays glossy even after scratches
- This is one of the most satisfying parts of the build — the car becomes *yours*, not a factory color

**Where to buy:** AMain Hobbies or Tekno RC direct. Any 1/8 buggy body fits the EB48 mounting pattern.

## Gearing

The Tekno EB48 2.2 kit includes a spur gear but you need to buy a pinion separately. Speed tuning happens here.

- **Steel pinion set (15T-21T, Mod 1)** — start with the mid-range pinion from the kit manual, measure speed with GPS, then step up one tooth at a time
- **Steel, not aluminum** — aluminum pinions wear out in a weekend at 6S power
- **Monitor motor temperature** after each gearing change. If it exceeds 80°C after a run, you've geared too tall.

**Where to buy:** AMain Hobbies — search "Tekno pinion Mod 1" or "1/8 buggy Mod 1 pinion set".

## The stuff nobody lists

| Item | Why | Where |
|------|-----|-------|
| **2× LiPo safety bags** | Charging and storage fire containment | Amazon.in |
| **XT90 connectors (5 pairs)** | Series wiring + replacements | [Robu.in](https://robu.in/) |
| **14AWG silicone wire (2m red, 2m black)** | Battery leads, ESC wiring | [Robu.in](https://robu.in/) |
| **Hex driver set (1.5, 2.0, 2.5, 3.0mm)** | Every screw on the car is hex | Amazon.in |
| **Ball-end hex drivers** | For turnbuckle adjustment — standard hex rounds off the ball cups | AMain Hobbies |
| **Shock oil set (25wt, 30wt, 35wt, 40wt)** | Fill the shocks during assembly; different weights for different damping | AMain Hobbies |
| **Diff oil set (3K, 5K, 7K, 10K cSt)** | Fill the three differentials; thinner = faster rotation, thicker = more traction | AMain Hobbies |
| **Thread-lock (blue, medium strength)** | Vibration loosens every screw at speed | Amazon.in |
| **CA glue (thin + medium)** | Tire repairs, body fixes, thread reinforcement | Amazon.in |
| **Tamiya PS spray paint (2-3 cans)** | Paint the body shell interior | Amazon.in or AMain |
| **Curved Lexan scissors** | Cut the body shell cleanly | AMain Hobbies |
| **GPS speed meter** | Verify actual speed — motor RPM estimates lie | Amazon.in — search "RC GPS speedometer" |
| **Soldering iron (60W adjustable)** | Connector swaps, wire repairs | [Robu.in](https://robu.in/) |

## Spare parts — order before you need them

The lesson from [the first post](../rc-cars-and-the-india-parts-problem/): **when something breaks at 100km/h, you cannot wait 4-6 weeks for shipping**. Order spares with the kit.

- **2× front A-arms, 2× rear A-arms** — first thing that snaps
- **1× steering rack assembly** — tie rods bend on hard impacts
- **1× set of CVD drive shafts** — absorbs drivetrain crash energy
- **2× sets of bearings (full car)** — they wear at high RPM; cheap per set
- **1× spur gear** — gearing experiments wear these
- **1× body shell** — because the first one will be shattered before you perfect the livery

All available on [AMain Hobbies](https://www.amainhobbies.com/) by searching "Tekno EB48 2.2 parts" or on [Tekno RC's parts page](https://www.teknorc.com/shop/?swoof=1&product_cat=eb48-2-2-parts) directly.

## The build plan

This is a build, not an unboxing. My plan:

1. **Differentials first** — assemble all three diffs, shim the gears, fill with oil. This takes hours and requires patience. Rushing shims means noisy, inefficient diffs.
2. **Shocks** — build all eight shocks, fill with oil, bleed air bubbles. Each one is a tiny hydraulic system.
3. **Chassis assembly** — suspension arms, hubs, steering, bulkheads. The manual is 40+ pages. Follow it exactly.
4. **Drivetrain** — install diffs, drive shafts, center drive. Check every gear mesh by hand.
5. **Electronics** — mount motor, ESC, servo, receiver. Solder battery connectors. Route wires clean.
6. **Body** — cut, drill, paint. Let it cure 48 hours.
7. **Shakedown** — first runs at low speed. Check everything tightens, nothing binds, steering is centered.
8. **Speed tuning** — gear up one tooth at a time. GPS speed checks. Motor temp checks. Repeat until 100.

I'll document the build as I go. Probably with more profanity than technical precision, but the data will be clean.
