# The Idea

We want to share all information we have about IOCs as a data set that we can share. At the same time, even if we also a user to get the whole information, we don't him to be able to discover this information but only the information for which he has already seen the IOC.

The solution used here, comes from:
> van de Kamp, T., Peter, A., Everts, M. H., & Jonker, W. (2016, October). Private Sharing of IOCs and Sightings. In Proceedings of the 2016 ACM on Workshop on Information Sharing and Collaborative Security (pp. 35-38). ACM.

We need to create a set of rules, each rule represent an IOC. A rule is composed of a set of attribute, and an encrypted message. The idea explained by van de Kamp and al is the secret message is encrypted by a key that have been generated by the values of the attributes, one that has these attributes can generate the key and then decrypt that secret message (which is the interesting inforamtion).

But we still have a problem, for an example, a user that is only interested by IPs inforamtion, he could create a table with the key for each possible IPs. This is, in this way already difficult but, with this technique, we already have to go through all rules one by one to see if there is a match (contrary of a hashstore where we can directly get the data). Thus, in order to avoid an attacker to create a table, we can add a salt for each rules.

Then, if there is a leak, we want to know where does it comes from. In order to do so, a simple but efficient solution is to include the misp token in the key generation. With this idea, every user that requests the set of rules gets a different one.

# try to pipe log files => logstash => kafka => cache => match rules

First I implemented a test in the frontend (encrypt) but what takes a lot of time is to get all rules in memory. So the idea is to get data in memory only once to check the whole set of possible IOCs.\\

- logstash: easy to configure and can parse a lot of different log files
- kafka: queue the elements
- cache: (depend on the output of logstash to be able to compare rules with more than one attribute)
- match rules: see what rules are matched by the computer system