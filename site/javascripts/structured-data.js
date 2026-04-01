// JSON-LD structured data for prashanthr.net
// Person, WebSite, Blog, BlogPosting schemas for Google
(function () {
  var defined = [];
  var path = window.location.pathname;

  // Person + WebSite — always present
  defined.push({
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "prashanthr.net",
    "alternateName": "Prashanth Rajagopal",
    "url": "https://prashanthr.net",
    "description":
      "Prashanth Rajagopal — software architect building Astra, an autonomous agent OS. Blog on distributed systems, Go, Rails, IoT, and agent infrastructure.",
    "inLanguage": "en",
    "author": {
      "@type": "Person",
      "name": "Prashanth Rajagopal",
      "url": "https://prashanthr.net",
      "sameAs": [
        "https://github.com/prashanthrajagopal",
        "https://twitter.com/prashanthrajagopal"
      ],
      "jobTitle": "Software Architect",
      "knowsAbout": [
        "Distributed Systems",
        "Agent Infrastructure",
        "Autonomous Agents",
        "Ruby on Rails",
        "Go",
        "PostgreSQL",
        "IoT",
        "Home Automation",
        "Electronics"
      ]
    },
    "potentialAction": {
      "@type": "SearchAction",
      "target": "https://prashanthr.net/search/?q={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  });

  // Blog listing page
  if (path === "/blog/" || path === "/blog") {
    defined.push({
      "@context": "https://schema.org",
      "@type": "Blog",
      "name": "Prashanth Rajagopal's Blog",
      "url": "https://prashanthr.net/blog/",
      "description":
        "Long-form writing on distributed systems, architecture, agent infrastructure, Rails, Go, IoT, and electronics.",
      "inLanguage": "en",
      "author": {
        "@type": "Person",
        "name": "Prashanth Rajagopal",
        "url": "https://prashanthr.net"
      },
      "publisher": {
        "@type": "Person",
        "name": "Prashanth Rajagopal",
        "url": "https://prashanthr.net"
      }
    });
  }

  // Individual blog post — extract from page meta
  if (path.match(/^\/blog\/posts\/[^/]+\/?$/) || path.match(/^\/blog\/\d{4}\/\d{2}\/\d{2}\/[^/]+\/?$/)) {
    var title = document.querySelector("h1");
    var desc = document.querySelector('meta[name="description"]');
    var dateEl = document.querySelector(".md-source-date, time, .post-date");
    var post = {
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": window.location.href
      },
      "headline": title ? title.textContent.trim() : document.title,
      "url": window.location.href,
      "inLanguage": "en",
      "author": {
        "@type": "Person",
        "name": "Prashanth Rajagopal",
        "url": "https://prashanthr.net"
      },
      "publisher": {
        "@type": "Person",
        "name": "Prashanth Rajagopal",
        "url": "https://prashanthr.net"
      }
    };
    if (desc) post.description = desc.content;
    if (dateEl) {
      var dateText = dateEl.getAttribute("datetime") || dateEl.textContent.trim();
      post.datePublished = dateText;
    }
    defined.push(post);
  }

  // BreadcrumbList for all pages
  var crumbs = path.split("/").filter(Boolean);
  if (crumbs.length > 0) {
    var items = [{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://prashanthr.net/"
    }];
    var built = "https://prashanthr.net";
    for (var i = 0; i < crumbs.length; i++) {
      built += "/" + crumbs[i];
      items.push({
        "@type": "ListItem",
        "position": i + 2,
        "name": crumbs[i].replace(/-/g, " ").replace(/\b\w/g, function(l){ return l.toUpperCase(); }),
        "item": built + "/"
      });
    }
    defined.push({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": items
    });
  }

  defined.forEach(function (schema) {
    var el = document.createElement("script");
    el.type = "application/ld+json";
    el.textContent = JSON.stringify(schema);
    document.head.appendChild(el);
  });
})();
