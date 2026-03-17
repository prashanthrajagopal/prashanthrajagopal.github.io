---
title: Rails philosophy
---

# Rails philosophy

**Convention over configuration** means defaults work for 80% of apps; escape hatches exist but are visible. Astra inverts part of that: the **kernel is minimal** and everything else is explicit **gRPC contracts** and **migrations**. Both approaches reduce surprise — Rails via naming, Astra via small surface area.

**Active Record** encourages fat models; Astra pushes **fat services** with a **thin kernel**. The common thread: **one obvious place** for a given behaviour.
