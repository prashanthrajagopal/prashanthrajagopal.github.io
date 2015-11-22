---
layout: post
title:  "Exploring Trusty Tahr(Ubuntu 14.04): Setup Ruby on Rails"
date:   2014-04-22 11:43:54
categories: ["Ubuntu", "Rails"]
---

This is a guide to setting up a Rails Development environment in Ubuntu 14.04 LTS.

Pre-requisutes

{% codeblock lang:bash %}
sudo apt-get update
sudo apt-get install curl libgdbm-dev libncurses5-dev automake libtool bison libffi-dev git-core
{% endcodeblock %}

I will be install Ruby via 3 different methods. You can choose one among these

 - **Installing via RVM**
{% codeblock lang:bash %}
curl -sSL https://get.rvm.io | sudo bash -s stable
echo "source /etc/profile.d/rvm.sh" >> ~/.bashrc
rvm install 2.1.1
rvm use 2.1.1 --default
{% endcodeblock %}

 - **Using rbenv**
{% codeblock lang:bash %}
git clone git://github.com/sstephenson/rbenv.git .rbenv
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
exec $SHELL
 
git clone git://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
echo 'export PATH="$HOME/.rbenv/plugins/ruby-build/bin:$PATH"' >> ~/.bashrc
exec $SHELL
 
curl -fsSL https://gist.github.com/mislav/a18b9d7f0dc5b9efc162.txt | rbenv install --patch 2.1.1
rbenv global 2.1.1
{% endcodeblock %}

 - **From source**
{% codeblock lang:bash %}
wget http://ftp.ruby-lang.org/pub/ruby/2.0/ruby-2.1.1.tar.gz
tar -xzvf ruby-2.1.1.tar.gz
cd ruby-2.1.1/
./configure
make
sudo make install
{% endcodeblock %}


**Installing Rails**

`gem install rails`

**Installing Mysql**

`sudo apt-get install mysql-server mysql-client libmysqlclient-dev1`
 
**Getting a new Rails app up**

`rails new sample_app`
