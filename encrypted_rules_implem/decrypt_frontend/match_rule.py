#!/usr/bin/env python3
# this code is inspired from https://github.com/CRIPTIM/private-IOC-sharing
# which is using the MIT license

from configuration import Configuration
import argparse
import configparser
import glob
import hashlib
import os
import re
import subprocess
import sys
import json
from base64 import b64decode
from copy import deepcopy
from Crypto.Cipher import AES
from Crypto.Util import Counter
from functools import lru_cache
from hkdf import HKDF
from multiprocessing import cpu_count, Process
import redis

parser = argparse.ArgumentParser(description='Evaluate a network dump against rules.')
parser.add_argument('attribute', nargs='+', help='key-value attribute eg. ip=192.168.0.0 port=5012')
parser.add_argument('--performance', action='store_true',
        help='run a performance test')
parser.add_argument('--plaintext', action='store_true',
        help='evaluate on the plaintext rules instead of cryptographic \
                rules')
parser.add_argument('--input_redis', action='store_true',
        help='input is not in the argument but in redis')

parser.add_argument('-p', '--multiprocess', action='store',
        type=int, help='Use multiprocess, it needs a redis cache and the maximum is the number of cores minus 1', default=0)
args = parser.parse_args()

def load_rule(filename):
    ruleParser = configparser.ConfigParser()
    ruleParser.read(filename)
    rule = ruleParser._sections
    try:
        rule['iterations'] = 1
        rule['hash_name'] = rule['hkdf']['hash_name']
        rule['salt'] = b64decode(rule['hkdf']['salt'])
        rule['dklen'] = int(rule['hkdf']['dklen'])
    except:
        try:
            rule['iterations'] = int(rule['pbkdf2']['iterations'])
            rule['hash_name'] = rule['pbkdf2']['hash_name']
            rule['salt'] = b64decode(rule['pbkdf2']['salt'])
            rule['dklen'] = int(rule['pbkdf2']['dklen'])
        except:
            raise Exception('Not a rule file.')
    rule['ioc']['attributes'] = rule['ioc']['attributes'].split('||')
    rule['ioc']['iv'] = int.from_bytes(b64decode(rule['ioc']['iv']), 'big')
    rule['ioc']['ciphertext'] = b64decode(rule['ioc']['ciphertext'])
    return rule


def derive_key(hash_name, password, salt, iterations, info, dklen=None):
    if iterations == 1:
        kdf = HKDF(hash_name)
        return kdf.expand(kdf.extract(salt, password), info, dklen)
    else:
        return hashlib.pbkdf2_hmac(hash_name, password, salt, iterations, dklen=dklen)

#@lru_cache(maxsize=None)
def cryptographic_match(hash_name, password, salt, iterations, info, dklen, iv, ciphertext):
    dk = derive_key(hash_name, password.encode('utf8'), salt, iterations, bytes(info, encoding='ascii'), dklen=dklen)

    ctr = Counter.new(128, initial_value=iv)
    cipher = AES.new(dk, AES.MODE_CTR, b'', counter=ctr)
    # A match is found when the first block is all null bytes
    if cipher.decrypt(ciphertext[:16]) == b'\x00'*16:
        plaintext = cipher.decrypt(ciphertext[16:])
        return (True, plaintext)
    else:
        return (False, '')


def argument_matching():
    attributes = dict(pair.split("=") for pair in args.attribute)
    dico_matching(attributes)


def dico_matching(attributes):
    # test each rules
    for rule in rules:
        rule_attr = rule['ioc']['attributes']
        password = ''
        try:
            password = '||'.join([attributes[attr] for attr in rule_attr])
        except:
            pass # nothing to do
            
        if args.plaintext:
            if rule['ioc']['plaintext'] == password:
                print("IOC '{}' matched for: {}\nCourse of Action\n================\n{}\n".format(rule['ioc']['id'], attributes, rule['ioc']['coa']))
        else:
            match, plaintext = cryptographic_match(rule['hash_name'], password, rule['salt'], rule['iterations'], rule['ioc']['token'], rule['dklen'], rule['ioc']['iv'], rule['ioc']['ciphertext'])
            if match:
                print("IOC '{}' matched for: {}\nCourse of Action\n================\n{}\n".format(rule['ioc']['token'], attributes, plaintext.decode('utf-8')))


def redis_matching():
    # data is enriched in logstash
    conf = Configuration()
    r = redis.StrictRedis(host=conf.redis_host, port=conf.redis_port, db=conf.redis_db)

    # get data
    log = r.rpop("logstash")
    while log:
        log = log.decode("utf8")
        log_dico = json.loads(log)
        dico_matching(log_dico)
        log = r.rpop("logstash")


# Performance test settings
if args.performance:
    import timeit
    number_of_runs = 5
    number_of_experiments = 100

if __name__ == "__main__":
    conf = Configuration
    rules = list()
    rule_location = conf.rule_location
    if os.path.isfile(rule_location):
        rules.append(deepcopy(load_rule(rule_location)))
    elif os.path.isdir(rule_location):
        rule_directory = os.path.normpath(rule_location + "/")
        for filename in glob.glob(os.path.join(rule_directory, "*.rule")):
            rules.append(deepcopy(load_rule(filename)))

    if not rules:
        sys.exit("No rules found.")
    print("Attention implem ca et enlever l'argement obligatoire")
    if args.multiprocess > 0:
        r = redis.StrictRedis(host=conf.redis_host, port=conf.redis_port, db=conf.redis_db)
        try:
            r.set("test", "test_value")
        except:
            sys.exit("No redis cache found")



    print("rules loaded")
    if args.input_redis:
        if args.performance:
            print("to implement") #TODO
        else:
            redis_matching()
    else:
        if args.performance:
            print(timeit.timeit("argument_matching()",number=5))
        else:
            argument_matching()
