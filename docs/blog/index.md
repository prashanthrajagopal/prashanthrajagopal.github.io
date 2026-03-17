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
    <a class="blog-post-row" href="posts/kernels-first-10ms/" data-tags="astra go">
      <span class="post-date">19 Mar 2026</span>
      <div>
        <h3>The kernel's first 10ms</h3>
        <p>Lookup, enqueue, done — what belongs on the path from Send to Receive, and what gets kicked out.</p>
      </div>
      <span class="post-tag tag-astra">Astra</span>
    </a>
    <a class="blog-post-row" href="posts/why-im-building-astra/" data-tags="astra agents">
      <span class="post-date">9 Mar 2026</span>
      <div>
        <h3>Why I'm building Astra</h3>
        <p>Fifteen years of shipping things that break at 2am. Agents everywhere, but nowhere serious for them to run — so I'm building an OS-shaped answer.</p>
      </div>
      <span class="post-tag tag-astra">Astra</span>
    </a>
    <div class="blog-post-row pr-blog-soon" data-tags="architecture">
      <span class="post-date">Coming soon</span>
      <div>
        <h3>Why I didn't use Kubernetes</h3>
        <p>Orchestrators solve deployment. I needed something that solves runtime. The distinction matters.</p>
      </div>
      <span class="post-tag tag-architecture">Architecture</span>
    </div>
  </div>
</div>
