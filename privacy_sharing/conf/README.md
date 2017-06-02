# Setup

- copy configuration.orig to configuration
- Fill in the values in configuration

Other files are for logstash if needed

# How to use Redis implementation:

## Start Redis
- ./opt/redis-stable/src/redis-server

## start squid3
- sudo service squid start

## Config firefox to access the data
- Preference -> advanced -> network -> connection -> proxy
- localhost or 127.0.0.1 on port 3128

=> logs are created on /var/log/squid/access.log 

## Start logstash with right configuration
- ./opt/logstash/bin/logstash -f /root/thesis/privacy_sharing/conf/logstash_squid.conf

## OR link configuration via the script and start logstash as a service
