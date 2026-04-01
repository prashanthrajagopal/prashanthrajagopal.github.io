---
title: Home Assistant ruined my light switches
date: 2025-12-14
description: From smart bulbs to a full Home Assistant setup — MQTT, Zigbee, automations that work, and the ones that spectacularly don't.
authors:
  - prashanth
categories:
  - DIY
tags:
  - home-assistant
  - iot
  - zigbee
  - mqtt
draft: false
---

It started with a single Philips Hue bulb. "I'll just automate the bedroom light," I said, with the confidence of someone who had not yet understood that *just* is the most dangerous word in engineering. Two years later I have a Zigbee mesh, an MQTT broker, a Raspberry Pi running Home Assistant with eleven add-ons, a drawer full of ESP32 boards, and a genuine inability to walk past a physical light switch without feeling mild contempt for it.

This is a story about scope creep. The protagonist loses nothing and regrets nothing.

<!-- more -->

## The gateway drug

Philips Hue is a good product. It's also a product that teaches you, very quickly, that you are renting your own lights. The bridge calls home. Automations live in Philips' cloud. If Signify decides to end-of-life the v2 bridge — which they are doing, in stages — your automations go with it. **You paid for hardware. You got a subscription to a lighting company's continued goodwill.**

That realization is the moment most people either shrug and accept it or start reading Home Assistant documentation. I started reading Home Assistant documentation.

## Why Zigbee won

The protocol decision took about a week of research and about three hours of regretting I hadn't done it differently before I landed somewhere stable. The options are roughly: **WiFi** (every device is on your LAN, easy setup, murder on a crowded 2.4GHz band, battery life is a joke), **Z-Wave** (good mesh, expensive hardware, proprietary history that still shows up in weird ways), **Zigbee** (mesh network, sub-GHz-equivalent interference profile at 2.4GHz but low duty cycle, cheap hardware, open enough that you can buy sensors for six dollars).

I went Zigbee. A Sonoff Zigbee 3.0 USB dongle on the Pi, Zigbee2MQTT as the translation layer, and Mosquitto as the broker. The mesh means every mains-powered device is a router — plug in a smart plug in the hallway and your sensors in the back bedroom suddenly have better signal. It compounds.

## MQTT is just messaging, and that's the point

Once Zigbee2MQTT is running, every sensor and switch in the house publishes to MQTT topics. Temperature sensor in the bathroom: `zigbee2mqtt/bathroom-temp`. Motion sensor by the front door: `zigbee2mqtt/front-door-motion`. The broker doesn't care what the device is. Home Assistant subscribes to the topics it needs. Node-RED subscribes to the ones that need logic.

`mosquitto_pub -t home/lights/bedroom -m "OFF"` turning off a light the first time hits different than it should for a grown adult. I'm not going to pretend otherwise.

**The payoff of MQTT as the lingua franca** is that nothing is coupled to anything else. The HA instance can restart without losing sensor state — the broker holds the last-will messages. A new automation is a new subscription, not a new integration to install. You're building a message bus for your house, and once you see it that way, adding a new device is just publishing to a new topic.

## The automations that actually work

Motion-activated lights are the canonical example because they're the canonical example for a reason: they work, they save real energy, and once you've had them for a month you cannot understand how you tolerated manually switching lights. My setup:

- Motion sensor detects presence → light turns on at the lux level appropriate for time of day
- No motion for N minutes → light turns off
- N is different at midnight than at noon

Temperature-based fan control is the other one. BME280 sensor on an ESP32 via ESPHome, publishing to MQTT. When the bedroom hits 26°C and it's past 10pm, the fan turns on. **One rule. Works every time. Survives reboots.** This is the automation bar everything else should be held to.

Presence detection via phone WiFi scanning works well enough that I use it for "is anyone home" logic but not for "which room is someone in" logic. The granularity isn't there without more hardware than the use case justifies.

## The ones that don't

Anything involving voice assistants and Indian accents is — diplomatically — an ongoing calibration exercise. The recognition accuracy on certain phonemes is optimistically described as "improving." Automation by voice is fine for simple commands with no ambiguity. "Turn off the living room lights" is fine. Anything with a room name that contains a retroflex consonant is a dice roll.

Smart curtains. I tried. The motor is loud enough that it defeats the purpose of automating a bedroom window. The position feedback drifts over time and requires recalibration that is not, in fact, automated. The WAF — whatever your household equivalent is — for "the curtains are doing something unexpected at 6am" is approximately zero. I reverted to manual curtains with no shame.

## ESPHome and the custom sensor rabbit hole

ESPHome is what happens when someone decides that firmware for microcontrollers should be YAML-configured and OTA-updatable and they're right about both things. ESP32 with a DHT22 for temperature and humidity. ESP32 with a PIR sensor in a room too far from the Zigbee mesh. Flash once, configure in YAML, updates push over WiFi.

The custom sensor path is where home automation stops being a smart home product category and starts being **embedded systems work with a consumer use case**. You're writing device configs, thinking about sampling intervals and deep sleep and battery budgets, checking whether your sensor's pull-up resistor is causing a voltage divider issue. It's the same engineering it's always been, just with LED strips.

## What this is actually about

The reason I find this genuinely interesting — beyond the practical convenience — is that it's **distributed systems in miniature**. You have devices that go offline unexpectedly. You have message delivery guarantees you have to think about. You have state that needs to survive restarts and be consistent across consumers. You have failure modes that only appear under specific timing conditions at 3am.

Every problem I've debugged in production backend systems shows up here, scaled to a house instead of a datacenter. The zigbee mesh has partition scenarios. MQTT has exactly-once delivery semantics to reason about. The automations have race conditions. Home Assistant's state machine has the same eventual-consistency headaches as any distributed state store — just with a UI that shows you a light bulb icon instead of a Grafana dashboard.

It's a toy system that isn't a toy. That's the best kind.

Thanks for reading.
