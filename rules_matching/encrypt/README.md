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
- One of the VM address is 192.168.56.50 thus I've configured my machine in the same subnetwork by adding a new ip address (for example):
	- ip addr add 192.168.56.10/24 dev eth0 


# Topology

- readMisp.py: convert misp attributes into rules/ for help you can simply call ./readMisp.py -h
