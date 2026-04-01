---
title: "ESP32, MQTT, and the $4 sensor that replaced a $200 one"
date: 2026-01-05
description: Building DIY air quality and environment sensors with ESP32 and ESPHome — why a ₹450 board beats a ₹15,000 Awair, and what that says about commercial IoT.
authors:
  - prashanth
categories:
  - DIY
tags:
  - esp32
  - mqtt
  - iot
  - home-assistant
draft: false
---

I was looking at an Awair air quality monitor — ₹15,000, sleek, app-connected — and simultaneously looking at the ESP32 sitting in a drawer I bought for ₹300. The Awair measures CO2, VOCs, temperature, humidity, and PM2.5. The ESP32 is a microcontroller with WiFi. One of these requires a subscription to see historical data. The other runs open firmware and publishes to a Mosquitto broker I control. **The math was not close.**

<!-- more -->

## What the $200 one is actually selling

Commercial IoT devices are not sensors. They're sensors bolted to a subscription business. The Awair hardware — the actual CO2 and particulate transducers — costs maybe $15 at component scale. The rest of what you're paying for is the app, the cloud backend, the firmware that calls home, and the brand association with "smart home." The data your sensor collects gets sent to their servers first, and you get to view it through their dashboard — for now, on their terms.

I'm not running a campaign against commercial IoT. For someone who doesn't want to solder anything, an Awair is fine. But for an engineer who can spend a Sunday afternoon and ₹650 in components, **the value proposition inverts completely.**

## The stack

ESPHome is the secret weapon here. It's a firmware framework that takes YAML config and compiles it to something that flashes onto an ESP32 or ESP8266. You describe your sensors declaratively, and ESPHome handles the driver code, WiFi reconnects, OTA updates, and automatic Home Assistant discovery. The first flash is over USB; every update after that is over WiFi. You touch the hardware exactly once.

The sensors I run:

- **BME280** — temperature, humidity, pressure. I2C, ₹150, better accuracy than the ubiquitous DHT22. The DHT22 works fine for ₹80 if you don't care about ±1°C vs ±0.5°C.
- **MQ-135** — air quality (volatile compounds, CO2 proxy). Analog, ₹200, needs a warm-up period and calibration but gives you a meaningful relative reading. Not a lab instrument. Useful for "is the air in this room objectively worse than usual."
- **BH1750** — light level in lux. I2C, ₹100. Useful for automation rules — turn on lights when measured lux drops below threshold, not on a timer.

Total: around ₹750 for a sensor node that covers temperature, humidity, pressure, air quality, and light. Against ₹15,000 for three of those metrics and a cloud dependency.

## MQTT and why it's the right transport

The sensors publish over MQTT to a Mosquitto broker running on the same machine as Home Assistant. Topics look like `home/sensors/bedroom/temperature`. Everything subscribes to everything it cares about. Home Assistant picks up the sensors automatically via the MQTT integration and the ESPHome discovery payload.

MQTT is the right protocol here because it's **fire-and-forget with delivery guarantees you can tune**. QoS 0 for sensor readings that come every 30 seconds — if you drop one packet, the next reading arrives in 30 seconds anyway. QoS 1 for anything that triggers an action. The broker lives on your LAN, latency is sub-millisecond, and nothing requires an internet connection to function.

The data flows into Grafana via the Home Assistant Prometheus exporter or directly via InfluxDB, depending on your setup. Watching your own sensor data populate a Grafana dashboard — CO2 climbing as you've been on a call for two hours, temperature creeping up when you forgot to open a window — is the kind of feedback loop that changes behavior in ways an app notification never did.

## Power and enclosures

Indoor sensors run off USB — a phone charger and a cable, done. Outdoor sensors are the interesting case. The ESP32 supports deep sleep at ~10μA current draw, which means a 3000mAh LiPo lasts months if you sleep between readings. The wake cycle is: wake up, reconnect WiFi, take reading, publish, sleep. About 200ms of active time every 5 minutes. The WiFi reconnect is the expensive part — factoring that in is important if you're actually trying to hit a year on a battery.

Enclosures are function over form. I've used 3D-printed cases from Thingiverse, and I've used cardboard with ventilation holes cut in it. The cardboard outdoor sensor is held together with a rubber band and has been running for four months. I'm not proud of this. I'm also not replacing it.

## The actual engineering lesson

Constraints make you design better. The ₹15,000 Awair removes every constraint and hands you a finished product. The ₹300 ESP32 forces you to understand what you actually need: which metrics matter, how often you need readings, what your acceptable error bound is, where you'll store the data. **Those are better questions than "which app has the nicer UI."**

There's also a privacy argument, and it's not paranoia — it's architecture. A sensor that publishes to your local MQTT broker cannot be bricked by a company going under, cannot have its data harvested, and cannot require a subscription to access data it already collected. The business model of commercial IoT is incompatible with long-term data ownership. Local-first isn't a philosophy, it's an engineering requirement if you want your sensors to still work in five years.

The ESP32 with open firmware and local MQTT is more reliable, more private, and significantly more interesting to build than anything you can buy at a retail markup. That the components cost less is almost beside the point — though it does make the decision easier.
