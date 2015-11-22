---
layout: post
title:  "Faster SSH"
date:   2013-05-03 11:43:54
categories: SSH
---

to speedup ssh connect time a little,

`ssh -o GSSAPIAuthentication=no user@host`

or add it to your ssh config

`GSSAPIAuthentication no`
