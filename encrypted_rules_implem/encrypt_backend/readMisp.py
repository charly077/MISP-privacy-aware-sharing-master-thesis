#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# this code is inspired from https://github.com/CRIPTIM/private-IOC-sharing
# which is using the MIT license
from configuration import Configuration
import requests, csv, json
import argparse
import argparse
import configparser
import glob
import hashlib
import re
import subprocess
import sys
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter
from hkdf import HKDF


""" 
Create the paper solution for Misp
- read misp data
- encrypt / hash them
"""



parser = argparse.ArgumentParser(description='Create an encrypted IOC \
        rule.')
parser.add_argument('--hash', dest='hash_name', default='sha256',
        help='hash function to use')
parser.add_argument('--iterations', type=int, default=1,
        help='iterations needed before the decryption key is derived')
parser.add_argument('--plaintext', action='store_true',
        help='store the plaintext rule as well')

args = parser.parse_args()

conf = Configuration () # TODO change config to config file
token = bytes(conf.misp_token, encoding='ascii')

# update list is done via ./update.py
IOCs = list()
with open("res/misp_events.csv", "r") as f:
    data = csv.DictReader(f)
    for d in data:
        IOCs.append(d)

rules_counter = 0 # for filename generation
def create_rule(ioc, message):
    # encrypt the ioc and the message
    salt = Random.new().read(hashlib.new(args.hash_name).digest_size)
    dklen = 16 # AES block size
    iv = Random.new().read(16) # TODO they use it but check if secure

    # Spit + redo allow to ensure the same order to create the password
    attr_types = '||'.join(attr_type for attr_type in ioc)
    password = '||'.join(ioc[attr_type] for attr_type in ioc)

    # encrypt the message
    if args.iterations == 1:
        kdf = HKDF(args.hash_name)
        kdf.extract(salt, password.encode("utf8")) # Check if it works
        dk = kdf.expand(info=token, L=dklen)
    else:
        dk = hashlib.pbkdf2_hmac(args.hash_name, password.encode('utf8'), salt, args.iterations, dklen=dklen)

    ctr = Counter.new(128, initial_value=int.from_bytes(iv, 'big'))
    cipher = AES.new(dk, AES.MODE_CTR, b'', counter=ctr)
    ciphertext = cipher.encrypt(b'\x00'*16 + message.encode('utf-8'))

    # store the rules TODO improve this
    rule = configparser.ConfigParser()
    if args.iterations == 1:
        rule['hkdf'] = {}
        rule['hkdf']['hash_name'] = args.hash_name
        rule['hkdf']['salt'] = b64encode(salt).decode('ascii')
        rule['hkdf']['dklen'] = str(dklen)
    else:
        rule['pbkdf2'] = {}
        rule['pbkdf2']['hash_name'] = args.hash_name
        rule['pbkdf2']['salt'] = b64encode(salt).decode('ascii')
        rule['pbkdf2']['iterations'] = str(args.iterations)
        rule['pbkdf2']['dklen'] = str(dklen)
    rule['ioc'] = {}
    rule['ioc']['token'] = conf.misp_token
    rule['ioc']['attributes'] = attr_types
    rule['ioc']['iv'] = b64encode(iv).decode('ascii')
    rule['ioc']['ciphertext'] = b64encode(ciphertext).decode('ascii')
    if args.plaintext:
        rule['ioc']['dk'] = b64encode(dk).decode('ascii')
        rule['ioc']['plaintext'] = password
        rule['ioc']['coa'] = message

    global rules_counter
    filename = "rules/rule_" + str(rules_counter) + '.rule'
    rules_counter = rules_counter + 1
    with open(filename, 'w') as configfile:
        rule.write(configfile)


# message = information that we get when there is a match
def create_message(attr):
    uuid = attr["uuid"]
    event_id = attr["event_id"]
    date = attr["date"]
    return "{}:{}:{}".format(uuid, event_id, date)

def parse_attribute(attr):
    # an attribute can have either one type or a list of type
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
    create_rule(ioc, msg)


iocs = [parse_attribute(ioc) for ioc in IOCs]
