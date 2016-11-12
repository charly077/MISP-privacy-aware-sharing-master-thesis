# thesis
- report: explanation draft
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
	- squid3 log
	- network dump
- improve the speed of loading rules with redis (ongoing)
