---
layout: post
title:  "Password Management Using Ccrypt"
date:   2014-03-16 11:43:54
categories: "Pawssword Management"
---

For a long time I have been searching for a safe and secure way to store my passwords. There have been a number of free apps that I have tried out and somehow ended up dis-satisfied with everything else till I stumbled upon ccrypt.

{% codeblock lang:bash %}
| www.example1.com | username | PASSWORD | tag1 |
| www.example2.com | username | PASSWORD | tag2 |
{% endcodeblock %}

Encrypt the passwords file using the command

`ccrypt -e passwds`

Once the file is encrypted, the extension .cpt is appended.

View contents of the file

`cat passwds.cpt | ccat | grep tag`


To copy the password to the clipboard,

`ccat passwds.cpt | grep tag1 | cut -d "|" -f 4 | sed -e 's/^ *//' -e 's/*$//`
