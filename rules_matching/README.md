# Master's thesis
This is a modifed version of:
> van de Kamp, T., Peter, A., Everts, M. H., & Jonker, W. (2016, October). Private Sharing of IOCs and Sightings. In Proceedings of the 2016 ACM on Workshop on Information Sharing and Collaborative Security (pp. 35-38). ACM.

- encrypt: Get attributes from MISP and transform them into sharable IOCs called rules
- decrypt: Look up for match(es) from arguments or from logstash-redis

# The Idea

We want to create a sharable IOC dataset in which a user cannot retrieve the whole information while beeing able to get the information about IOCs seen on his computer.

The used solution is a modifed version of:
> van de Kamp, T., Peter, A., Everts, M. H., & Jonker, W. (2016, October). Private Sharing of IOCs and Sightings. In Proceedings of the 2016 ACM on Workshop on Information Sharing and Collaborative Security (pp. 35-38). ACM.

We need to create a set of rules, each rule represents an IOC. A rule is composed of a set of attribute types, and an encrypted message. The idea explained by van de Kamp et al is that the secret message is encrypted by a key generated thanks to the values of the attributes. A user possessing the correct attribute values can thus generate the key and then decrypt the message.

But we still have a problem, for an example, a user only interested by IPs' information could create a table with all the possible keys. Even if it would take a lot of time to decrypt each IP rules, as we already have to go through all rules one by one to see if there is a match (on the contrary of a hashstore where we can directly get the message). We can add a different salt for each rules.

Then, the last point is about knowing the origin of a leakage. A simple but efficient solution is to include the misp token in the key generation. (thus needed for encryption and decryption)
