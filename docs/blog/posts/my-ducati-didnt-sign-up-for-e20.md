---
title: "My Ducati didn't sign up for E20, and neither did I"
date: 2026-09-15
description: India went E20 at nearly every pump — premium grades included. The only ethanol-free petrol left is 100-octane, costs ₹168 a litre, and is out of stock across most of Bengaluru.
authors:
  - prashanth
categories:
  - Motorcycles
tags:
  - motorcycles
  - ducati
  - e20
  - india
draft: false
---

Somewhere in a government office, someone decided that every litre of petrol sold in India should be 20% ethanol. From 1 April 2026, that's what comes out of nearly every nozzle in the country. Nobody asked the bikes.

My Ducati certainly wasn't consulted. The owner's manual is unambiguous: petrol with **a maximum of 10% ethanol**. Not 20. Not "close enough." Ten.

<!-- more -->

## The manual says ten for a reason

Ducati didn't write that line for fun. Ethanol is hygroscopic — it pulls water out of the air. It eats rubber seals and swells fuel lines. It corrodes aluminium over time. And it carries less energy per litre than petrol, so you burn more of it to go the same distance.

On a fuel-injected, high-compression Italian engine with a fuel system that costs more than some cars, none of that is a rounding error. It's a slow-motion warranty argument I'd rather not have.

Put it in software terms. The owner's manual is the interface contract. The fuel is the input. Someone upstream changed the input format — no versioning, no deprecation window, no migration path — and pushed it to every consumer at once. **That's a breaking change, shipped straight to production, for every vehicle in the country.**

## "Premium" is a label, not a spec

Here's the part that still makes me angry. Every standard grade of petrol in India is now E20. Not just the cheap stuff. XP95, Speed 95, Speed 97, Power 95, Shell V-Power — all of it.

The premium sticker on the pump means higher octane. It does not mean less ethanol. You can pay extra for a nicer number and still pour 20% ethanol into a tank that was designed for half that.

## The E0 that's left

Exactly one category of petrol in India is still ethanol-free: the 100-octane stuff. Three brands, three very different levels of confidence:

- **XP100 (Indian Oil)** — the best documented. IOCL confirmed via an RTI reply that it has no ethanol blending, and Autocar India's gas-chromatography test found under 0.2% ethanol. The government's 2026 clarification exempts 100-octane fuels from the blending programme because they're niche, low-volume products.
- **Speed 100 (Bharat Petroleum)** — independently tested ethanol-free, and BPCL itself has said Speed 97 is E20 while Speed 100 is E0.
- **Power 100 (Hindustan Petroleum)** — the shaky one. Lab tests have found it clean, but HPCL's own social channel has said it may contain up to 4.5% ethanol. When the vendor hedges in its own documentation, I don't fully trust the product.

So the fuel my bike was built for still exists. It's just been rebranded as an exotic performance product and priced to match — roughly ₹167–169 a litre, near double what regular petrol costs.

I'm not paying for 100 octane. My engine doesn't need 100 octane. **I'm paying a ransom to *not* have ethanol.**

## Finding it in Bengaluru is a part-time job

You'd think a city with this many superbikes and German sedans would have XP100 on every corner. It doesn't. About 36 pumps across all three brands are mapped as selling ethanol-free petrol in Bengaluru, and only 14 of those are Indian Oil XP100 outlets. On paper.

In practice, it's worse. The last time I checked the crowdsourced tracker, most of the city's XP100 pumps had been reported out of stock within the previous two weeks: HSR Layout, Koramangala, KR Puram, Malleswaram, Old Madras Road, Mysore Road, Vidyaranyapura, 80 Feet Road. All listed. All dry.

The ones actually confirmed in stock recently:

- **Bowring Service Station**, near St Mark's Road
- **Swathi Enterprises**, 8th Mile, Tumkur Road
- **Sri Ekadantha**, Gottigere

Three pumps. For a city of 14 million people. If you're willing to gamble on HPCL, Vijay Gasoline on the Outer Ring Road at KR Puram is the single most-confirmed E0 pump in the city.

So the pre-ride ritual now goes like this: open e0fuel.in or xp100finder.com, check who's been confirmed in the last 48 hours, call the pump, hope the attendant knows what "XP100" is, ride across town, and pray the tank hasn't run dry since the phone call.

Indian Oil's official answer is "use the IndianOil ONE app." Which would be great if the app's data were ever current. A registry nobody updates isn't a registry — it's a rumour with a UI.

Nationally, the picture is the same. The three companies' official lists add up to around 230 outlets across the entire country, heavily clustered in Delhi, Mumbai, Bengaluru, Pune and Chennai. If you own an older bike in a tier-two city, you're on your own.

## The bit nobody in charge wants to say out loud

E20 is being sold as a win for farmers, for the import bill, for the environment. Fine. Argue those on their merits.

But there's a quiet cost being pushed onto millions of vehicle owners: every carburetted commuter bike, every pre-2023 car, every classic, every imported motorcycle whose manufacturer capped it at E10. They were sold fuel that fit their engines. Then the fuel changed underneath them, and the only opt-out is a ₹168 boutique grade sold at three pumps in the city.

And here's what should worry everyone. Ethanol blending happens at the big depots. XP100 stays clean only because it's too small a batch to bother blending. **That's not a policy. That's an accident we're all relying on.** Anyone who's inherited a legacy system knows how that story ends: the undocumented behaviour everybody depends on is exactly the thing that quietly disappears in the next cleanup.

## Until then

I'll keep hunting for XP100. I'll keep calling Bowring before every ride. And I'll keep wondering why doing right by my engine has to feel like scoring contraband.

If you're in the same boat:

- **Check e0fuel.in before you ride.** Recent confirmations matter more than the pin on the map.
- **Ask for the fuel by its exact name.** XP100. Speed 100. Power 100. Not "premium," not "the good one."
- **Don't let anyone tell you the premium nozzle is the same thing.** It isn't.

The manual says ten. The pump says twenty. Only one of them was written with my engine in mind.
