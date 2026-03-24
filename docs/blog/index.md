---
title: Blog
hide:
  - toc
---

<div class="blog-layout" markdown="0">
  <header class="blog-header">
    <p>Long-form writing on distributed systems, architecture, and the technology I'm currently pulling apart to understand how it works. Posts are written from experience, not from documentation.</p>
  </header>

  <div class="blog-filter-bar">
    <button type="button" class="pr-filter-chip active" data-filter="all">All</button>
    <button type="button" class="pr-filter-chip" data-filter="astra">Astra</button>
    <button type="button" class="pr-filter-chip" data-filter="architecture">Architecture</button>
    <button type="button" class="pr-filter-chip" data-filter="agents">Agents</button>
    <button type="button" class="pr-filter-chip" data-filter="go">Go</button>
    <button type="button" class="pr-filter-chip" data-filter="rails">Rails</button>
  </div>

  <div class="blog-posts-list">
    <a class="blog-post-row" href="posts/the-10ms-lie-we-all-tell/" data-tags="architecture caching astra">
      <span class="post-date">24 Mar 2026</span>
      <div>
        <h3>The 10ms lie we all tell</h3>
        <p>Every cache is a bet — and the 10ms on the whiteboard only counts the wins. Why cache discipline is architecture, not a tuning pass.</p>
      </div>
      <span class="post-tag tag-architecture">Architecture</span>
    </a>
    <a class="blog-post-row" href="posts/what-rails-taught-me-about-supervision/" data-tags="rails ruby astra actors">
      <span class="post-date">24 Mar 2026</span>
      <div>
        <h3>What Rails taught me about supervision</h3>
        <p>Puma, Sidekiq, and the art of not staying dead — which instincts from fifteen years of Ruby carried straight into Astra's actor tree.</p>
      </div>
      <span class="post-tag tag-rails">Rails</span>
    </a>
    <a class="blog-post-row" href="posts/sandboxes-arent-security-theater/" data-tags="astra security wasm docker">
      <span class="post-date">24 Mar 2026</span>
      <div>
        <h3>Sandboxes aren't security theater</h3>
        <p>WASM, Docker, Firecracker — how you pick the cage when agents run tools you didn't write.</p>
      </div>
      <span class="post-tag tag-astra">Astra</span>
    </a>
    <a class="blog-post-row" href="posts/why-postgres-stays-sacred/" data-tags="postgres databases astra architecture">
      <span class="post-date">24 Mar 2026</span>
      <div>
        <h3>Why Postgres stays sacred</h3>
        <p>Eventual consistency is fine until it isn't. Where I draw the line between "fast read" and "source of truth."</p>
      </div>
      <span class="post-tag tag-architecture">Systems</span>
    </a>
    <a class="blog-post-row" href="posts/scheduling-without-losing-your-mind/" data-tags="astra scheduling distributed-systems">
      <span class="post-date">24 Mar 2026</span>
      <div>
        <h3>Scheduling without losing your mind</h3>
        <p>Shards, heartbeats, and the gap between "works on my laptop" and a graph that has to survive real load.</p>
      </div>
      <span class="post-tag tag-astra">Astra</span>
    </a>
    <a class="blog-post-row" href="posts/kernels-first-10ms/" data-tags="astra go">
      <span class="post-date">19 Mar 2026</span>
      <div>
        <h3>The kernel's first 10ms</h3>
        <p>Lookup, enqueue, done — what belongs on the path from Send to Receive, and what gets kicked out.</p>
      </div>
      <span class="post-tag tag-astra">Astra</span>
    </a>
    <a class="blog-post-row" href="posts/why-i-didnt-use-kubernetes/" data-tags="astra kubernetes devops">
      <span class="post-date">15 Mar 2026</span>
      <div>
        <h3>Why I didn't use Kubernetes</h3>
        <p>Docker for Postgres and Redis, native Go for what moves — orchestration can wait until the architecture stops moving weekly.</p>
      </div>
      <span class="post-tag tag-architecture">Infrastructure</span>
    </a>
    <a class="blog-post-row" href="posts/why-im-building-astra/" data-tags="astra agents">
      <span class="post-date">9 Mar 2026</span>
      <div>
        <h3>Why I'm building Astra</h3>
        <p>Fifteen years of shipping things that break at 2am. Agents everywhere, but nowhere serious for them to run — so I'm building an OS-shaped answer.</p>
      </div>
      <span class="post-tag tag-astra">Astra</span>
    </a>
  </div>

</div>
