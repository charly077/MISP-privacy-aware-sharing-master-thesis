#!/bin/bash
echo starting squid3 service
sudo service squid restart

echo start redis server
cd /opt/redis-stable/src
./redis-server &

echo stop logstash service for now
sudo service logstash stop

echo start logstash
cd /opt/logstash/bin
./logstash -f ~/thesis/encrypted_rules_implem/decrypt_frontend/logstash_squid.conf &

echo if no error, everything started, do not close this terminal
cd /opt/redis-stable/src
./redis-cli
