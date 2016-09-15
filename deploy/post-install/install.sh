#!/usr/bin/env bash

apt-get -y -q install apache2
apt-get -y -q install python-pip
yes | pip install -r /var/www/hwserver/requirements.txt
apt-get -y -q install libapache2-mod-wsgi
a2enmod wsgi

cp /var/www/hwserver/code_deploy/apache2/easydns.conf /etc/apache2/sites-available/hwserver.conf
a2dissite 000-default.conf
a2ensite hwserver.conf

service apache2 restart