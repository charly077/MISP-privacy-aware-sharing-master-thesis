#Encrypted backend
Get data from misp, encrypt them like explained in
> van de Kamp, T., Peter, A., Everts, M. H., & Jonker, W. (2016, October). Private Sharing of IOCs and Sightings. In Proceedings of the 2016 ACM on Workshop on Information Sharing and Collaborative Security (pp. 35-38). ACM.

# Installation

- sudo apt-get install libmysqlclient-dev
- for configuration, I've installed the misp virtualmachine
- then, I've reconfigured the vm to have a remote access to sql:
	- vim /etc/mysql/my.cnf
	- replace line "bind-address          = 127.0.0.1" by "# bind-address          = 127.0.0.1"
	- mysql -uroot -pPassword1234
	- CREATE USER 'user'@'%' IDENTIFIED BY 'Password1234';
	- GRANT ALL ON *.* TO 'user'@'%';
- One of the VM address is 192.168.56.50 thus I've configured my machine in the same subnetwork:
	- ip addr add 192.168.56.10/24 dev eth0 (for example)


# Topology

- update.py: download some elements and store it in res/(soon better used)
- readMisp.py: convert misp attributes into rules/

# Working
- Add your misp token in configuration.py
- mkdir res rules
- run ./update.py
- run ./readMisp

# TODO
- Add the ability to create the rules directly from the mysql misp database
