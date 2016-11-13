# The Idea

We want to create a sharable IOC dataset in which a user cannot retrieve the whole information while beeing able to get the information about IOCs seen on his computer.

The used solution is a modifed version of:
> van de Kamp, T., Peter, A., Everts, M. H., & Jonker, W. (2016, October). Private Sharing of IOCs and Sightings. In Proceedings of the 2016 ACM on Workshop on Information Sharing and Collaborative Security (pp. 35-38). ACM.

We need to create a set of rules, each rule represent an IOC. A rule is composed of a set of attributes, and an encrypted message. The idea explained by van de Kamp and al is that the secret message is encrypted by a key generated thanks to the values of the attributes. Then, a user possessing the correct attribute values can generate the key and then decrypt that secret message.

But we still have a problem, for an example, a user only interested by IPs' information could create a table with all the possible keys. Even if it would take a lot of time to decrypt each IP rules, as we already have to go through all rules one by one to see if there is a match (on the contrary of a hashstore where we can directly get the message). We can add a different salt for each rules.

Then, the last point is about leakage, we want to know where does it comes from. A simple but efficient solution is to include the misp token in the key generation. (thus needed for encryption and decryption)

# simple utilization with the arguments
./match_rule.py filename=6b6e92be036b1a67c383d027bafc7eb63cf515006bb3b3c6ca362a2332542801 sha1=dd3a61eed9c454cf96d882f290abc86108ffeea5


# try to pipe log files => logstash => redis => match rules

First I implemented a test in the frontend (encrypt) but what takes a lot of time is to get all rules in memory. So the idea is to get data in memory only once to check the whole set of possible IOCs.

- logstash: used to parse files and send json in a string format to redis via a rpush on "logstash"
- redis: Used like a in-memory queue
- match rules: see what rules are matched by the computer system

# installation step for squid3

- install squid3: sudo apt-get install squid3
- configure squid3: /etc/squid/squid.conf
- restart squid3: sudo systemctl restart squid.service or sudo service squid3 restart

# installation step for logstash

- https://www.elastic.co/guide/en/logstash/current/getting-started-with-logstash.html
- put the logstash_squid.conf in /etc/logstash/conf.d/
- fix squid3 permission : chmod 644 /var/log/squid/access.log
- permanent fix explained in https://miteshshah.github.io/linux/elk/how-to-monitor-squid3-logs-on-elk-stack/
- running logstash as a service : sudo systemclt start logstash.service or sudo service logstash start
- Or just to start a process : logstash/bin/logstash -f ~/thesis/frontend_try/logstash_squid.conf 

# start matching IOCs
- ./match_rule --input_redis something (something has no use but is compulsory for now) 


# TODO
- improve the speed with cache (for rules)
- improve squid matching with sub www https and get the port number! 
- parallelise rules checking
