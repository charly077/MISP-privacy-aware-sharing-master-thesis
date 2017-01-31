#Encrypted backend
Convert misp attributes to encrypted rules like explained in 
> van de Kamp, T., Peter, A., Everts, M. H., & Jonker, W. (2016, October). Private Sharing of IOCs and Sightings. In Proceedings of the 2016 ACM on Workshop on Information Sharing and Collaborative Security (pp. 35-38). ACM.

# Installation

- sudo apt-get install libmysqlclient-dev
- sudo pip install -r requirements.txt

# MISP virtual machine configuration (not needed)
- Remote access to sql:
	- vim /etc/mysql/my.cnf
	- replace line "bind-address          = 127.0.0.1" by "# bind-address          = 127.0.0.1"
	- mysql -uroot -pPassword1234
	- CREATE USER 'user'@'%' IDENTIFIED BY 'Password1234';
	- GRANT ALL ON *.* TO 'user'@'%';
- One of the VM address is 192.168.56.50 thus I've configured my machine in the same subnetwork by adding a new ip address (for example):
	- ip addr add 192.168.56.10/24 dev eth0 


# readMisp.py
- help : 
	- ./readMisp.py -h
- Read from mysql : 
	- copy encrypt_configuration.py.orig to encrypt_configuration.py
	- fill the misp, misp mysql and rules sections
	- ./readmisp --misp mysql --iterations 1000 --ipiteration 100000
- Read from misp web api :
	- copy encrypt_configuration.py.orig to encrypt_configuration.py
	- fill the misp, misp web api and rules sections
	- ./readmisp --misp mysql --iterations 1000 --ipiteration 100000
