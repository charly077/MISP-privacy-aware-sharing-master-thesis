# Privacy Preserving Sharing in MISP

Nowadays, in computer security, we need more than simple malware detectors or antiviruses. 
New security threats suddenly appear and we have to react as soon as possible. 
This is why a new kind of security levels appeared and is called threat sharing.

The idea behind is to share a threat when we discover one, we allow then,
every other member of the sharing organization to defend themselves against it 
but also to put in common all information they have. This results in fast recoveries 
and protections.

A lot of sharing platforms emerged from this idea. One of them is called MISP,
Malware Information Sharing Platform and Threat Sharing [2]. 
One of its specificities is of being an open source project [1]. 
We can also find a set of tools on the same repository [2].

This platform is maintained by the Computer Incident Response Center Luxembourg (CIRCL [3])
which is one of the companies helping me in my work. The second one is Conostix [4] 
which provides security and system services in Luxembourg.

IOCs are commonly considered as sensitive data. This induces companies with confidential data to be
unwilling to share IOCs. Especially when in some case, a user needs to have these IOCs on a file that
he can bring with him to check a computer.

Nevertheless, they have no problems to share data if, the user already knows it. 
Which means that a user that has seen the IOC on his computer could be able to discover 
that another organization have seen it and then, to get back information they have, but never otherwise.

And this is on this specific challenge that we are attempting to find a solution.

# Starting point
The starting point was this article with their prove of concept implementation:
> van de Kamp, T., Peter, A., Everts, M. H., & Jonker, W. (2016, October). Private Sharing of IOCs and Sightings. In Proceedings of the 2016 ACM on Workshop on Information Sharing and Collaborative Security (pp. 35-38). ACM.

The basic idea is to transform and IOC (indicator of compromise) into something sharable but that does not leak any information.
Of course, as we want data to be retrievable from a user it is thus possible for an attacker to brute force the data. But we want it to be as difficult as possible.

The general concept is thus :

Rule(sharable IOC) creation
```python
for each misp attribute:
    create a "secret message"
    derive a key from the values of the attributes, the user token and a salt
    encrypt the secret message with this derived key
    save it as a "rule"
```

Matching
```python
for each rule:
    Try to decipher the secret message
    if it matches:
        return the value
```

Then, I've tried to make a code modular to be able to add new crypto systems on it.

# Structure
conf/ contains all configurations in the configuration file (= configuration.orig)

src/ contains all the source files

# Setup
- Install python3 and pip3
- apt-get install libmysqlclient-dev build-essential libssl-dev libffi-dev python-dev libpng-dev libfreetype6-dev pkg-config
- pip3 install -r requirements.txt

# Setup Misp Virtual Machine (testing purpose)
- Image available on : https://circl.lu/services/misp-training-materials/

if we need to access the database from an other host, add remove sql access: (on the vm)
```
- vim /etc/mysql/my.cnf (/etc/mysql/mysql.conf.d/mysql.cnf in new virtual machines)
- replace line "bind-address = 127.0.0.1" by "# bind-address = 127.0.0.1"
- mysql -uroot -pPassword1234
- CREATE USER 'user'@'%' IDENTIFIED BY 'Password1234';
- GRANT ALL ON *.* TO 'user'@'%';
```


# Examples
- cd conf
- cp configuration.orig configuration
- nano configuration
- fill in misp/rules/pbkdf2 sections and save it
- cd ..
- ./readMisp.py -v
- ./matchRules.py ip-dst=192.168.1.1


[1]https://github.com/MISP/MISP

[2] https://github.com/MISP/

[3] https://www.circl.lu/

[4] http://conostix.lu/

