---
layout: post
title:  "Remove and Disable Apparmor in Ubuntu"
date:   2013-03-23 11:43:54
categories: Ubuntu
---

If you want to disable and remove apparmor, run the following commands.

This has been tested on Ubuntu 14.04.

{% codeblock lang:bash %}
sudo /etc/init.d/apparmor stop
sudo /etc/init.d/apparmor teardown
sudo update-rc.d -f apparmor remove
{% endcodeblock %}
