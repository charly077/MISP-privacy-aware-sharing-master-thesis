# Normalize data to increase matches

## url
Use basic normalization from RFC 3986 and the one explained in
	"""
	Lee, S. H., Kim, S. J., & Hong, S. H. (2005, May). On URL normalization. 
	In International Conference on Computational Science and Its Applications (pp. 1076-1085).
	 Springer Berlin Heidelberg.
	"""
(these had been synthesized in wikipedia)

- scheme and host => lower case
- escape character => replace by the real character
- port => removed

- remove dot segment in path
- remove directory index
- remove the fragment
- replace ip by domain name
- remove protocol => not sure it is interesting https -> http (not sure to implement it)
- remove // in the path
- remove www
- remove querry "?______" 
- add / at the end

## uri
try to consider it like and url, else
- to lower case
- remove dot segment

## hostname
- to lowercase
- remove www 

## link
- Some links have the attribute to\_ids => consider them as an url
