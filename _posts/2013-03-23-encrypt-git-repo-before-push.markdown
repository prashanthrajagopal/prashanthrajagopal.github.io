---
layout: post
title:  "Encrypt Git Repo Before Push"
date:   2013-03-23 11:43:54
categories: Git
---

Here is how you encrypt your git repo before you push to remote.

{% codeblock lang:bash %}
cd ~/; mkdir .gitencrypt
cd ~/.gitencrypt; touch openssl_clean openssl_smudge openssl_diff
{% endcodeblock %}

Add this to your clean file

{% codeblock lang:bash %}
PASS=[pass_phrase_for_encryption] openssl enc -base64 -aes-256-ecb -S $SALT -k $PASS openssl_smudge
{% endcodeblock %}

{% codeblock lang:bash %}
#!/bin/bash
PASS=[the_pass_phrase_used_for_encryption]
openssl enc -d -base64 -aes-256-ecb -k $PASS 2> /dev/null || cat
git_diff
{% endcodeblock %}

{% codeblock lang:bash %}
#!/bin/bash
PASS_FIXED=>your-passphrase>
openssl enc -d -base64 -aes-256-ecb -k $PASS_FIXED -in "$1" 2> /dev/null || cat "$1"
{% endcodeblock %}

Now to our git repo.

{% codeblock lang:bash %}
mkdir ~/gitrepo; cd ~/gitrepo
git init
touch .gitattributes
{% endcodeblock %}

Add the lines to .gitattributes

`filter=openssl diff=openssl [merge] renormalize = true`

add the following to .git/config

`[filter "openssl"] smudge = ~/.gitencrypt/openssl_smudge clean = ~/.gitencrypt/clean`

`textconv = ~/.gitencrypt/git_diff`

Now git add the files you want to commit. The clean filter is applied and the files are encrypted before they are checked into the repo. Git diff will work as usual as it first decrypts before displaying the diff.

If the repo has to be cloned to another box, ~/.gitencrypt, repo/.gitattributes and repo/.git/config has to be exactly the same as that of the first box.

AES ECB with a fixed salt may not be the most secure but it solves the purpose of encrypting the codebase atleast a little. You can choose to use any algorithm for use.
