---
layout: post
title: "Play 5.1 Audio(AC3, DTS) in iTunes"
date: 2015-12-17T13:41:42+05:30
categories: OSX
---

Yes, it is possible to get a 5.1 audio output from iTunes if you have a compatible receiver. There are a few posts floating online, but this is the easiest way i could get it working. This method was proposed by [Graham Broker](http://www.macworld.com/article/1150554/itunes_surround.html).

* Install [Perian](http://www.perian.org) ([download link](http://perian.cachefly.net/Perian_1.2.3.dmg)).
* Connect your digital audio receiver. I use an optical connection to my Logitech receiver.
* Change to audio output to 48000.0Hz, 2ch-16bit.
* Enable DTS and AC3 passthrough from terminal
  * Enable AC3 passthrough
`defaults write com.cod3r.a52codec attemptPassthrough 1`
  * Enable DTS passthrough
`defaults write org.perian.Perian attemptDTSPassthrough 1`
  * Disable AC3 passthrough
`defaults delete com.cod3r.a52codec attemptPassthrough`
  * Disable DTS passthrough
`defaults delete org.perian.Perian attemptDTSPassthrough`
* Restart iTunes if already running and play the file with 100% volume.
* Verify chanel layout - Quicktime Player->Show Movie Properties->Select audio track->Audio Settings
