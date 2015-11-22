---
layout: post
title:  "Mysql Dealyed Replication"
date:   2013-12-12 11:43:54
categories: SSH
---

Something I have been wanting to do for a long time. This works only for mysql 5.5 and above

{% codeblock lang:sql %}
STOP SLAVE;
CHANGE MASTER TO MASTER_DELAY = 3600;
START SLAVE;
{% endcodeblock %}
