---
title: Blog — Prashanth Rajagopal
description: Long-form writing on distributed systems, agent infrastructure, Rails, Go, and Astra by Prashanth Rajagopal at prashanthr.net.
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
    <button type="button" class="pr-filter-chip" data-filter="security">Security</button>
    <button type="button" class="pr-filter-chip" data-filter="diy">DIY</button>
    <button type="button" class="pr-filter-chip" data-filter="iot">IoT</button>
    <button type="button" class="pr-filter-chip" data-filter="electronics">Electronics</button>
  </div>

  <div class="blog-posts-list">
    <a class="blog-post-row" href="posts/the-100kmph-build-list/" data-tags="diy rc-cars electronics india">
      <span class="post-date">2 Apr 2026</span>
      <div>
        <h3>The 100km/h build list: every part, every reason</h3>
        <p>A full custom 1/8 scale RC buggy built entirely by hand — Tekno EB48 2.2 chassis kit, Hobbywing 6S power, every bolt chosen individually.</p>
      </div>
      <span class="post-tag tag-diy">DIY</span>
    </a>
    <a class="blog-post-row" href="posts/litellm-and-the-trust-chain-nobody-audits/" data-tags="security supply-chain astra agents sandboxing">
      <span class="post-date">26 Mar 2026</span>
      <div>
        <h3>LiteLLM and the trust chain nobody audits</h3>
        <p>A compromised security scanner, stolen PyPI credentials, and a .pth file that ran on every Python startup. Three hours, 3.4 million daily downloads.</p>
      </div>
      <span class="post-tag tag-architecture">Security</span>
    </a>
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
    <a class="blog-post-row" href="posts/chat-is-the-easy-part/" data-tags="astra chat websocket architecture">
      <span class="post-date">20 Mar 2026</span>
      <div>
        <h3>Chat is the easy part</h3>
        <p>What it actually took to bolt WebSocket streaming onto Astra — and why the session model matters more than the protocol.</p>
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
    <a class="blog-post-row" href="posts/the-approval-gate-nobody-wants/" data-tags="astra security agents governance">
      <span class="post-date">18 Mar 2026</span>
      <div>
        <h3>The approval gate nobody wants (until they do)</h3>
        <p>Building dual-approval and plan gates into an autonomous agent system — the tension between speed and not letting agents terraform destroy prod.</p>
      </div>
      <span class="post-tag tag-astra">Astra</span>
    </a>
    <a class="blog-post-row" href="posts/why-astra-runs-on-a-mac-mini/" data-tags="astra macos deployment">
      <span class="post-date">16 Mar 2026</span>
      <div>
        <h3>Why Astra runs on a Mac Mini</h3>
        <p>macOS as a production deployment target for an agent OS — Metal acceleration, native binaries, no emulation. When Kubernetes isn't the answer.</p>
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
    <a class="blog-post-row" href="posts/agent-memory-is-not-a-vector-database/" data-tags="astra memory pgvector architecture">
      <span class="post-date">13 Mar 2026</span>
      <div>
        <h3>Agent memory is not a vector database</h3>
        <p>Working memory, episodic memory, and semantic search are three different things. pgvector is one layer, not the whole story.</p>
      </div>
      <span class="post-tag tag-astra">Astra</span>
    </a>
    <a class="blog-post-row" href="posts/dead-letters-are-a-feature/" data-tags="astra reliability distributed-systems">
      <span class="post-date">11 Mar 2026</span>
      <div>
        <h3>Dead letters are a feature, not a failure</h3>
        <p>Designing for task exhaustion with dead-letter queues and retry budgets makes your system more honest than pretending everything succeeds.</p>
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
    <a class="blog-post-row" href="posts/rc-cars-and-the-india-parts-problem/" data-tags="diy rc-cars electronics india">
      <span class="post-date">8 Feb 2026</span>
      <div>
        <h3>My first RC car build: an engineer's guide to pain in India</h3>
        <p>Approaching RC cars like a software person — choosing a platform, brushless ESCs, LiPo safety, and the uniquely Indian challenge of getting parts at all.</p>
      </div>
      <span class="post-tag tag-diy">DIY</span>
    </a>
    <a class="blog-post-row" href="posts/ruby-in-2026/" data-tags="ruby rails">
      <span class="post-date">22 Jan 2026</span>
      <div>
        <h3>Ruby in 2026: still boring, still right</h3>
        <p>Rails isn't trendy and it isn't dead. Boring technology choices compound, and the Ruby ecosystem does more right than the hype cycle admits.</p>
      </div>
      <span class="post-tag tag-rails">Rails</span>
    </a>
    <a class="blog-post-row" href="posts/esp32-mqtt-and-the-4-dollar-sensor/" data-tags="diy esp32 mqtt iot home-assistant">
      <span class="post-date">5 Jan 2026</span>
      <div>
        <h3>ESP32, MQTT, and the $4 sensor that replaced a $200 one</h3>
        <p>Building DIY air quality and environment sensors with ESP32 and ESPHome — why a ₹450 board beats a ₹15,000 Awair, and what that says about commercial IoT.</p>
      </div>
      <span class="post-tag tag-diy">IoT</span>
    </a>
    <a class="blog-post-row" href="posts/home-assistant-ruined-my-light-switches/" data-tags="diy home-assistant iot zigbee mqtt">
      <span class="post-date">14 Dec 2025</span>
      <div>
        <h3>Home Assistant ruined my light switches</h3>
        <p>From smart bulbs to a full Home Assistant setup — MQTT, Zigbee, automations that work, and the ones that spectacularly don't.</p>
      </div>
      <span class="post-tag tag-diy">DIY</span>
    </a>
    <a class="blog-post-row" href="posts/what-electronics-taught-me-about-debugging/" data-tags="electronics debugging distributed-systems">
      <span class="post-date">20 Nov 2025</span>
      <div>
        <h3>What electronics taught me about debugging software</h3>
        <p>Oscilloscopes, multimeters, and tracing signals through a circuit — the hardware debugging mindset that transfers directly to distributed systems.</p>
      </div>
      <span class="post-tag tag-architecture">Engineering</span>
    </a>
  </div>

  <div class="blog-queue-section">
    <h2 class="blog-queue-heading">Coming up</h2>
    <p class="blog-queue-intro">Posts I'm working on. No dates — they ship when they're honest.</p>
    <div class="blog-posts-list">
      <div class="blog-post-row pr-blog-soon" data-tags="astra agents memory">
        <span class="post-date">Soon</span>
        <div>
          <h3>Agents don't need memory — they need amnesia</h3>
          <p>Everyone's building "memory for agents" as append-only context stuffing. The harder problem is forgetting — deliberately.</p>
        </div>
        <span class="post-tag tag-astra">Astra</span>
      </div>
      <div class="blog-post-row pr-blog-soon" data-tags="astra task-graph dag distributed-systems">
        <span class="post-date">Soon</span>
        <div>
          <h3>The task graph is not a pipeline</h3>
          <p>You hear "DAG" and think Airflow. Astra's task graph is dynamic, runtime-mutable, and evaluated under scheduling pressure. The pipeline metaphor breaks.</p>
        </div>
        <span class="post-tag tag-astra">Astra</span>
      </div>
      <div class="blog-post-row pr-blog-soon" data-tags="astra llm routing architecture">
        <span class="post-date">Soon</span>
        <div>
          <h3>Routing LLM calls like you'd route traffic</h3>
          <p>Cost caps, response caching, provider failover — the same instincts from load balancing HTTP apply, and the same mistakes show up again.</p>
        </div>
        <span class="post-tag tag-architecture">Architecture</span>
      </div>
      <div class="blog-post-row pr-blog-soon" data-tags="astra multi-tenancy security architecture">
        <span class="post-date">Soon</span>
        <div>
          <h3>Multi-tenancy is a trust boundary, not a database column</h3>
          <p>Adding org_id to every query is where multi-tenancy starts, not where it ends. Real isolation survives a confused-deputy attack.</p>
        </div>
        <span class="post-tag tag-astra">Astra</span>
      </div>
      <div class="blog-post-row pr-blog-soon" data-tags="go ruby astra languages">
        <span class="post-date">Soon</span>
        <div>
          <h3>What Go took from me (and what it gave back)</h3>
          <p>A Ruby loyalist's honest trade ledger after building a kernel in Go. Not a language war — an accounting.</p>
        </div>
        <span class="post-tag tag-architecture">Architecture</span>
      </div>
    </div>
  </div>

</div>
