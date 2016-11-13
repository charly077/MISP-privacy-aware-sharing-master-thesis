# thesis
- encrypt backend: first implementation
- decrypt frontend: first implementation

# How to use
- Put your token in encrypt backend/configuration.py and decrypt frontend/configuration.py
- Run ./readMisp (You may need to create res and rules folders)
- copy the rules folder into decrypt backend
- Run ./match_rule.py attr1=val1 [attr2=val2 [...]]

# TODO
- create the decrypt step on 
	- an argument (OK)
	- analyse logs/network dump/... => logstash => redis => match_rule (ongoing working but need to be improved)
- improve the speed of loading rules with redis 
	=> Not feasible (rule is not serializable)
