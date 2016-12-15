# thesis
This is a modifed version of:
> van de Kamp, T., Peter, A., Everts, M. H., & Jonker, W. (2016, October). Private Sharing of IOCs and Sightings. In Proceedings of the 2016 ACM on Workshop on Information Sharing and Collaborative Security (pp. 35-38). ACM.

- encrypt backend: get attributes from MISP and transform them into sharable IOCs called rules
- decrypt frontend: Look for a match

# How to use
- Put your token in encrypt backend/configuration.py and decrypt frontend/configuration.py
- Run ./readMisp (You may need to create res and rules folders)
- copy the rules folder into decrypt backend
- Run ./match_rule.py attr1=val1 [attr2=val2 [...]]
