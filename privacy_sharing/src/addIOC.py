#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
	Once already read the misp implementation, sometimes, we only need to add additionnal element.
	This is really usefull for a high number of iterations

	This implementation could have been done directly in readMisp but I want to avoid misinterpretation
	or to add too many arguments that can be modified by others
		=> Here NO RULES are removed when running, the only action is to add some
			from res or from the form
"""

# MISP import
from configuration import Configuration
from readMisp import create_message, parse_attribute

# Tools import
import argparse, configparser, csv, sys

# Crypto import
from crypto.choose_crypto import Crypto

###################
# Parse Arguments #
###################
parser = argparse.ArgumentParser(description='Add new rules to already generated ones.')
parser.add_argument('--misp', default='args',
        help='form for filling the form OR res to get data from res in a CSV file')
parser.add_argument('--CSVname', default='addIOCs',
        help='Name of the CSV in the res/ folder (Without .csv)')
parser.add_argument('-v', '--verbose',\
        dest='verbose', action='store_true',\
        help='Explain what is being done')
args = parser.parse_args()

###########
# Helpers #
###########
def printv(value):
    if args.verbose:
        print(value)


def askContinue():
	res = input('Do you want to add more IOCs?: (Yes|No)').lower
	if 'yes' in res:
		return True
	else:
		return False
##################
# Implementation #
##################
IOCs = list()
conf = Configuration()

# Get configuration
printv('Get meta parameters')
metaParser = configparser.ConfigParser()
try:
	metaParser.read(conf['rules']['location'] + '/metadata')
	metadata = metaParser._sections
except:
	print('Rules must have already been created for adding news')
	sys.exit(1)


def ioc_csv(filename=args.CSVname):
	printv('Get new IOCs')
	if '.csv' not in filename:
		filename += '.csv'
	with open('../res/' + filename, 'r') as f:
		data = csv.DictReader(f)
		for d in data:
			IOCs.append(d)

def ioc_arg():
	print("Pay attention that no check are make on the inputs")
	ioc = {}
	ioc['id'] = input('id*: ')
	ioc['event_id'] = input('event id*: ')
	ioc['category'] = input('category*: ')
	ioc['type'] = input('type*: ')
	ioc['value1'] = input('value1*:')
	ioc['value2'] = input('value2:')
	ioc['to_ids'] = -1
	while ioc['to_ids'] not in [0, 1]:
		try:
			ioc['to_ids'] = int(input('to_ids*(1|0): '))
		except:
			print("Value must be either 0 or 1")
	ioc['uuid'] = input('uuid*: ')
	ok = 0
	while not ok:
		try:
			ioc['timestamp'] = int(input('timestamp*: '))
			inp = input('distribution: ')
			if inp not '':
				ioc['distribution'] = int(inp)
			inp = input('sharing group id: ')
			if inp not '':
				ioc['sharing_group_id'] = int(inp)
			ok = 1
		except:
			print('timestamp, distribution and sharing group id must be integers')
	
	IOCs.append(ioc)
	
def saveIOCs():
	pass
if __name__ == '__main__':
	"""Let's go!"""
	if args.misp == 'args':
		ioc_argv()
		cont = askContinue
		while cont:
			ioc_argv()
			cont = askContinue
	elif args.misp == 'res':
		ioc_arg()
	else:
		print("Choose a correct argument for misp")
	
	saveIOCs()
