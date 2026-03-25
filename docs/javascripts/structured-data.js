// JSON-LD structured data for prashanthr.net
// Establishes entity identity for Google Knowledge Graph
(function () {
  var defined = [];

  // Person + WebSite — disambiguates "prashanthr.net" from "prashanth.net"
  defined.push({
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "prashanthr.net",
    "alternateName": "Prashanth Rajagopal",
    "url": "https://prashanthr.net",
    "description":
      "Prashanth Rajagopal's blog and wiki on distributed systems, agent infrastructure, and Astra.",
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
        "Ruby on Rails",
        "Go",
        "Kubernetes",
        "PostgreSQL"
      ]
    }
  });

  // Blog schema
  if (
    window.location.pathname === "/blog/" ||
    window.location.pathname.startsWith("/blog/")
  ) {
    defined.push({
      "@context": "https://schema.org",
      "@type": "Blog",
      "name": "Prashanth Rajagopal's Blog",
      "url": "https://prashanthr.net/blog/",
      "description":
        "Long-form writing on distributed systems, architecture, and agent infrastructure by Prashanth Rajagopal.",
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

  defined.forEach(function (schema) {
    var el = document.createElement("script");
    el.type = "application/ld+json";
    el.textContent = JSON.stringify(schema);
    document.head.appendChild(el);
  });
})();
