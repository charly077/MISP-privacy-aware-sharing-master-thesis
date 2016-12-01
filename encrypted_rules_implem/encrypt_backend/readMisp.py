#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# this code is inspired from https://github.com/CRIPTIM/private-IOC-sharing
# which is using the MIT license

# misp import
from configuration import Configuration
import update, requests, csv, json

# tools import
import argparse, configparser
import sys, subprocess, os, shutil
import datetime, copy, re

# crypto import
import glob, hashlib
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter
from hkdf import HKDF

# mysql import
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData, Table
from sqlalchemy.sql import select




###################
# Parse Arguments #
###################
parser = argparse.ArgumentParser(description='Create an encrypted IOC \
        rule.')
parser.add_argument('--hash', dest='hash_name', default='sha256',
        help='hash function to use')
parser.add_argument('--iterations', type=int, default=1,
        help='iterations needed before the decryption key is derived')
parser.add_argument('--misp', default='csv',
        help='csv => misp attributes in /res/misp_events.csv \n ;\
                mysql => get attributes from the database (need configuration.py)')
parser.add_argument('-v', '--verbose',\
        dest='verbose', action='store_true',\
        help='Explain what is being done')
args = parser.parse_args()

####################
# Global Variables #
####################
conf = Configuration ()
token = bytes(conf.misp_token, encoding='ascii')

# IOC list 
IOCs = list()

##########
# Helper #
##########
# Used for verbose
def printv(value):
    if args.verbose:
        print(value)

def ioc_csv():
    printv("Update data from misp")
    update.update()
    printv("Cache misp data")
    with open("res/misp_events.csv", "r") as f:
        data = csv.DictReader(f)
        for d in data:
            IOCs.append(d)

def ioc_mysql():
    printv("Connection to mysql database")
    Base = automap_base()
    engine = create_engine('mysql://{}:{}@{}/{}'.format(conf.user, conf.password, conf.host, conf.dbname))

    Base.prepare(engine, reflect=True)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    connection = engine.connect()
    attributes_table = Table("attributes", metadata, autoload=True)
    users_table = Table("users", metadata, autoload=True)

    # misp token must be the same as the authkey
    printv("Check authentication key (token)")
    query = select([users_table.c.authkey]).where(users_table.c.email == conf.misp_email)
    resp = connection.execute(query)
    for authkey in resp:
        if not conf.misp_token == authkey[0]:
            sys.exit("Your misp_token must be your authentication key. Please check your configuration file")

    # get all ids attributes 
    printv("Get Attributes")
    attributes = connection.execute(select([attributes_table]))
    for attr in attributes:
        dic_attr = dict(attr.items())
        if dic_attr['to_ids'] == 1:
            timestamp = dic_attr['timestamp']
            dic_attr['date'] = datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y%m%d")
            dic_attr['value'] = dic_attr['value1']
            if (attr['value2']):
                dic_attr['value'] = dic_attr['value'] + '|' + dic_attr['value2']
            IOCs.append(dic_attr)

# message = COA = information that we get when there is a match
def create_message(attr):
    uuid = attr["uuid"]
    event_id = attr["event_id"]
    date = attr["date"]
    return "{}:{}:{}".format(uuid, event_id, date)

#################
# IOCs -> rules #
#################
def create_rule(ioc, message):
    # encrypt the ioc and the message
    salt = Random.new().read(hashlib.new(args.hash_name).digest_size)
    dklen = 16 # AES block size
    iv = Random.new().read(16)

    # Spit + redo allow to ensure the same order to create the password
    attr_types = '||'.join(attr_type for attr_type in ioc)
    password = '||'.join(ioc[attr_type] for attr_type in ioc)

    # encrypt the message
    if args.iterations == 1:
        kdf = HKDF(args.hash_name)
        kdf.extract(salt, password.encode("utf8"))
        dk = kdf.expand(info=token, L=dklen)
    else:
        dk = hashlib.pbkdf2_hmac(args.hash_name, password.encode('utf8'), salt, args.iterations, dklen=dklen)

    ctr = Counter.new(128, initial_value=int.from_bytes(iv, 'big'))
    cipher = AES.new(dk, AES.MODE_CTR, b'', counter=ctr)
    ciphertext = cipher.encrypt(b'\x00'*16 + message.encode('utf-8'))

    # create the rule
    rule = {}
    rule['salt'] = b64encode(salt).decode('ascii')
    rule['attributes'] = attr_types
    rule['iv'] = b64encode(iv).decode('ascii')
    rule['ciphertext'] = b64encode(ciphertext).decode('ascii')

    return rule

def parse_attribute(attr):
    # IOC can be composed of a unique attribute type or of a list of attribute types
    split_type = attr["type"].split('|')
    ioc = {}
    if (len(split_type)>1):
        # more than one value
        split_value = attr["value"].split('|')
        for i in range(len(split_type)):
            ioc[split_type[i]] = split_value[i]
    else:
        ioc[attr["type"]] = attr["value"]
    msg = create_message(attr)
    return create_rule(ioc, msg)


########
# Main #
########
if __name__ == "__main__":
    # first clean up the rule folder
    printv("Clean rules folder")
    if os.path.exists("rules"):
        shutil.rmtree("rules")
    os.mkdir("rules")

    # fill IOC list
    printv("Get IOCs from " + args.misp)
    if args.misp == 'csv':
        ioc_csv()
    elif args.misp == 'mysql':
        ioc_mysql()
    else:
        sys.exit('misp argument is mis configured. Please select csv or mysql')

    # create metadata
    printv("Create metadata")
    meta = configparser.ConfigParser()
    meta['crypto'] = {}
    meta['crypto']['hash_name'] = args.hash_name
    meta['crypto']['dklen'] = str(16) # AES block size
    meta['crypto']['iterations'] = str(args.iterations)
    with open('rules/metadata', 'w') as config:
        meta.write(config)

    # Parse IOCs
    printv("Create rules")
    iocs = [parse_attribute(ioc) for ioc in IOCs]

    # sort iocs in different files for optimization
    printv("Sort IOCs with attributes")
    iocDic = {}
    for ioc in iocs:
        typ = "_".join(ioc["attributes"].split('||'))
        try:
            iocDic[typ].append(ioc)
        except:
            iocDic[typ] = [ioc]

    printv("Store IOCs in files")
    for typ in iocDic:
        with open('rules/'+ typ +'.csv', 'wt') as output_file:
            dict_writer = csv.DictWriter(output_file, iocDic[typ][0].keys(), delimiter='\t')
            dict_writer.writeheader()
            dict_writer.writerows(iocDic[typ])
