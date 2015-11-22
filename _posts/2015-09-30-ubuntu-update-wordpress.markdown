---
layout: post
title:  "Ubuntu Update Wordpress"
date:   2015-09-30 21:43:54
categories: wordpress update
---

Writing this just to keep track of things for the future

{% codeblock lang:bash title:"Update wordpress without entering credentials everytime" %}
#!/bin/bash

sudo adduser wp-user
cd /var/www/html
sudo chown -R wp-user:wp-user /var/www/html
sudo mkdir -p /home/wp-user/.ssh/
sudo chmod 0640 /home/wp-user/.ssh
sudo su -l wp-user -c "ssh-keygen -f /home/wp-user/.ssh/id_rsa -t rsa -b 4096 -N ''"
sudo chown wp-user:www-data /home/wp-user/.ssh/id_rsa*
sudo chmod 0700 /home/wp-user/.ssh/authorized_keys
sudo cp /home/wp-user/.ssh/id_rsa.pub /home/wp-user/.ssh/authorized_keys
sudo chown wp-user:wp-user /home/wp-user/.ssh/authorized_keys
sudo chmod 0644 /home/wp-user/.ssh/authorized_keys
sudo apt-get update
sudo apt-get install php5-dev libssh2-1-dev libssh2-php
read -r -d '' APPEND_DATA << EOM
define('FTP_PUBKEY','/home/wp-user/.ssh/id_rsa.pub');
define('FTP_PRIKEY','/home/wp-user/.ssh/id_rsa');
define('FTP_USER','wp-user');
define('FTP_PASS','');
define('FTP_HOST','127.0.0.1:22');
EOM
echo $APPEND_DATA >> /var/www/html/wp-config.php
sudo service apache2 restart
{% endcodeblock %}
