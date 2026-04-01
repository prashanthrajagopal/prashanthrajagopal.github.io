---
title: "Ruby in 2026: still boring, still right"
date: 2026-01-22
description: Rails isn't trendy and it isn't dead. Boring technology choices compound, and the Ruby ecosystem does more right than the hype cycle admits.
authors:
  - prashanth
categories:
  - Rails
tags:
  - ruby
  - rails
  - opinion
draft: false
---

I've been writing Ruby for fifteen years. Not as a hobbyist, not as a nostalgia project — as the primary tool I reach for when I need to ship a web application that works, can be maintained by humans, and doesn't require me to rewrite the build toolchain every eighteen months. The "Ruby is dead" crowd has been saying it since 2015. They're still wrong, and Rails 8 is the best evidence I can point to.

This isn't a comeback story. Ruby never left for the people who were using it seriously.

<!-- more -->

## What Rails 8 actually did

The headline is Solid Queue, Solid Cache, and Solid Cable — three first-party libraries that replace what used to be Redis-flavored middleware dependencies. Background jobs, caching, and websockets, backed by the database you already have. No extra infrastructure to operate, no SLA to manage on a separate service, no "wait, which version of the Redis protocol does this client support?"

Kamal handles deployment — Docker containers pushed to real servers without Kubernetes overhead. Turbo and Hotwire mean you can build reactive UIs without committing to a JavaScript framework that will be deprecated before your next quarterly review.

What Rails did here is the thing it's always done: **identify where accidental complexity is eating developer time and collapse it back into the framework.** The framework is eating its own ecosystem, and that's not a power grab — it's good engineering. Fewer moving parts that you didn't choose are fewer moving parts that can surprise you.

## The compounding argument

Here's the thing I keep coming back to: boring technology choices compound. Every year you're not rewriting your framework is a year you're shipping features. Every year your dependencies stay stable is a year your engineers spend on the product instead of the plumbing.

Compare this to the JavaScript ecosystem, where your build tool has a half-life of eighteen months. Webpack to Parcel to Vite to whatever is current when you're reading this. The features you shipped last year still work — but the scaffolding around them has been replaced twice. That churn has a cost that doesn't show up in benchmarks.

Rails applications I wrote in 2018 run fine today, on newer Rails, with minimal changes. **That's the compounding.** The conventions haven't moved. The patterns are the same. A new engineer can read the code without a guided tour through six layers of custom abstraction.

## Where Ruby still falls short — and I'm not going to lie about it

The type system story is awkward. RBS, Sorbet, Steep — they exist, they work for people who invest in them, and they are not the seamless experience you get from TypeScript or Kotlin. If you want the full "errors at the red squiggly, not at runtime" experience, Ruby is still asking you to meet it more than halfway. This is a genuine weakness. I've worked on large Ruby codebases where a method rename propagated incorrectly because nobody had types on that module, and it was not fun.

YJIT has changed the performance narrative. Ruby 3.3 and 3.4 are genuinely fast for web workloads — not "fast for a scripting language," just fast. The CRuby team has done serious work here and the benchmarks are real. **For the typical Rails app, Ruby's performance is no longer the bottleneck.** The database, the N+1 queries, the network round-trip to an LLM API — those are your constraints, and Ruby is not in the picture.

## Where it doesn't fit

I'm not running a campaign against other languages. Ruby is wrong for systems programming — Go and Rust exist for a reason. It's wrong for ML pipelines — Python owns that space and the ecosystem gap is not closable. It's wrong for mobile. If you're building an embedded system or a compiler, Ruby should not appear in your architecture diagram.

What it's still unmatched for: CRUD web applications, internal tools, prototypes you need running by Thursday, and any domain where developer happiness materially affects what gets built. Convention over configuration isn't a philosophy — it's an observation that most decisions don't need to be decisions. Rails made that observation twenty years ago and has been right ever since.

## The real moat

Performance benchmarks get argued about on social media. The real moat that Ruby has — and that's hard to replicate from scratch — is ecosystem maturity and the decade-level investment in conventions that the community has made. The Rails way exists. It's opinionated, documented, and understood by a large pool of engineers. When you hire someone with five years of Rails experience, you know what they know.

That's worth more than a faster JSON serializer.

If I had to pick one language to ride into the sunset with, it's still Ruby. The others are tools; Ruby is the one I argue about at parties.
