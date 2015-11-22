---
layout: post
title:  "Faster WordPress with Varnish 3"
date:   2014-10-24 21:43:54
categories: wordpress update
---

* Note: This post has not been updated for Varnish 4 yet.

This post is a guide to increase responsiveness and page load times for those who host WordPress on their own machines. Caching helps reduce page load times dramatically and handle traffic spikes to a certain extent.

Varnish is a reverse caching proxy which I use to cache all static content and my pages. This returns cached pages from instead of asking php to render the pages for us each time which can bring down the server at high loads.

**Installing Varnish**

I run the entire setup on Ubuntu 14.04.

Varnish runs on port 80 which is exposed to the web. Apache listens to Varnish on port 8888. Only port 80 and my SSH port are exposed to the outside world(refer AWS Security Groups).

{% codeblock lang:bash title:"Install Varnish" %}
sudo apt-get install varnish
{% endcodeblock %}

**Varnish Config Files:**
{% gist 9791d4bc3993a6eeebce title:"/etc/varnish/default.vcl" %}
{% gist 4df711376369972a37ff title:"/etc/default/varnish" %}

Configure Apache to listen to a different port

In the file,
`/etc/apache2/ports.conf`, edit the Listen line the following line to `Listen 8888`

You will need to update your Virtual Hosts file. In my case, the file is `/etc/apache2/sites-enabled/100-default.conf`
