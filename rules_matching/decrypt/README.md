# Utilization with the arguments
./match_rule.py filename=6b6e92be036b1a67c383d027bafc7eb63cf515006bb3b3c6ca362a2332542801 sha1=dd3a61eed9c454cf96d882f290abc86108ffeea5


# Pipe log files => logstash => redis => match rules
- logstash: Parse log files and send json in a string format to redis via a rpush on "logstash"
- redis: Used like a in-memory queue (rpop and rpush on key="logstash")
- match rules: Check for matching attributes

## Following installation steps can vary on the distribution used
### Installation step for squid3
- install squid3: sudo apt-get install squid3
- configure squid3: /etc/squid/squid.conf
- restart squid3: sudo systemctl restart squid.service or sudo service squid3 restart

### Installation step for logstash

- https://www.elastic.co/guide/en/logstash/current/getting-started-with-logstash.html
- put the logstash_squid.conf in /etc/logstash/conf.d/
- fix squid3 permission : chmod 644 /var/log/squid/access.log
- permanent fix explained in https://miteshshah.github.io/linux/elk/how-to-monitor-squid3-logs-on-elk-stack/
- running logstash as a service : sudo systemclt start logstash.service or sudo service logstash start
- Or just to start a process from the logstash folder: ./bin/logstash -f ~/thesis/rules_matching/decrypt/logstash_squid.conf

## Start matching (It can be parallelized into different processes)
- ./match_rule --input redis
- To improve the speed: ./match_rule --input_redis --multiprocess n (max n is the computer core number minus one)
