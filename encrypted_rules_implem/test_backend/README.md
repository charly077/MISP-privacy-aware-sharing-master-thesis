#Encrypted backend
Get data from misp, encrypt them like explained in
> van de Kamp, T., Peter, A., Everts, M. H., & Jonker, W. (2016, October). Private Sharing of IOCs and Sightings. In Proceedings of the 2016 ACM on Workshop on Information Sharing and Collaborative Security (pp. 35-38). ACM.

# Installation

- sudo apt-get install libmysqlclient-dev

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
