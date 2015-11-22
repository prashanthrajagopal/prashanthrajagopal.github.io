---
layout: post
title:  "Setting Up an Ubuntu Mirror: Rsync"
date:   2014-04-23 11:43:54
categories: ["Ubuntu", "Mirror"]
---

A local Mirror is useful for Ubuntu if a number of workstations keep hitting the internet mirrors a number of times. By setting up a local mirror, you will be able to control the updates that are delivered. There are a number of ways of setting up a mirror.

 - Rsync
 - apt-cacher
 - Proxy
 - Debmirror
 - apt-mirror

We will be covering the Rsync way of setting up the mirror.

Please note that we will need a lot of free space, probably around 2TB keeping the future in mind. However the current size of the mirror is around 900GB. It will be good if the file system used us XFS, the tried and tested FS for file storage.

The disk is to be mounted at /mirror

{% codeblock lang:bash title:"Install the necessary packages" %}
sudo apt-get update
sudo apt-get install mailutils postfix rsync
{% endcodeblock %}

Make sure the disk is mounted right and you have /mirror in place. This can be verified with df -kh

Start the Rsync manually for the first time.

{% codeblock lang:bash title:"If you have bandwidth constraints" %}
rsync -ah --bwlimit=512 rsync://archive.ubuntu.com/ubuntu /mirror/ubuntu
{% endcodeblock %}

{% codeblock lang:bash title:"if not" %}
rsync -ah rsync://archive.ubuntu.com/ubuntu /mirror/ubuntu
{% endcodeblock %}

You can check the progress of the download with --progress

{% gist 11212269 title:"sync script" %}
