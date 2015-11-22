---
layout: post
title:  "SEO for Octopress Pages"
date:   2014-03-16 11:43:54
categories: Octopress
---

Octopress has some hidden features for better SEO.

Adding Meta tags for each blog post

When a blog post is created with the command rake new_post[“SEO for octopress pages”], a few default keys(layout, title, comments, categories) are added to the begingin of the markdown page generated.

To add Meta Tags to the page, you need to add keywords and description.

{% codeblock lang:bash %}
---
layout: post
title: "SEO for octopress pages"
date: 2014-03-16 15:53:36 +0530
comments: true
categories: ["SEO","octopress"]
keywords: seo,octopress
description: How to attract SEO for octopress blog posts
---
{% endcodeblock %}

The following HTML is generated
{% codeblock lang:html %}
<title>SEO for Octopress Pages - Prashanthr.net</title>
<meta name="author" content="Prashanth Rajagopal">
<meta name="description" content="How to attract SEO for octopress blog posts">
<meta name="keywords" content="seo,octopuses">
{% endcodeblock %}
