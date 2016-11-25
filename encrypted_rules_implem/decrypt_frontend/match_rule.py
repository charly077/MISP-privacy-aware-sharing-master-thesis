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
import csv
from base64 import b64decode
from copy import deepcopy
from Crypto.Cipher import AES
from Crypto.Util import Counter
from functools import lru_cache
from hkdf import HKDF
from multiprocessing import SimpleQueue, Process, cpu_count
import redis

parser = argparse.ArgumentParser(description='Evaluate a network dump against rules.')
parser.add_argument('attribute', nargs='*', help='key-value attribute eg. ip=192.168.0.0 port=5012')
parser.add_argument('--performance', action='store_true',
        help='run a performance test')
parser.add_argument('--input_redis', action='store_true',
        help='input is not in the argument but in redis')

parser.add_argument('-p', '--multiprocess', action='store',
        type=int, help='Use multiprocess, the maximum is the number of cores minus 1', default=0, )
args = parser.parse_args()

metadata = {}
conf = Configuration()

####################
# helper functions #
####################

def iter_queue(queue):
    # iter on a queue without infinite loop
    def next():
        if queue.empty():
            return None
        else:
            return queue.get()
    # return iterator
    return iter(next, None)

#####################
# process functions #
#####################
def redis_matching_process(r, queue):
    # get data
    log = r.rpop("logstash")
    while log:
        log = log.decode("utf8")
        log_dico = json.loads(log)
        dico_matching(log_dico, queue)
        log = r.rpop("logstash")

def print_queue_process(queue):
    # this is an infinite loop as get waits when empty
    for elem in iter(queue.get, None):
       print(elem)



####################
# crypto functions #
####################
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


###################
# match functions #
###################
def dico_matching(attributes, queue):
    global conf
    global metadata
    # test each rules
    for rule in rules:
        rule_attr = rule['attributes']
        password = ''
        try:
            password = '||'.join([attributes[attr] for attr in rule_attr])
        except:
            pass # nothing to do
            
        match, plaintext = cryptographic_match(metadata['hash_name'], password, rule['salt'], metadata['iterations'], conf.misp_token, metadata['dklen'], rule['iv'], rule['ciphertext'])
        if match:
            queue.put("IOC '{}' matched for: {}\nCourse of Action\n================\n{}\n".format(conf.misp_token, attributes, plaintext.decode('utf-8')))

def argument_matching():
    attributes = dict(pair.split("=") for pair in args.attribute)
    match = SimpleQueue()
    dico_matching(attributes, match)

    # print matches
    for match in iter_queue(match):
        print(match)

def test(name):
    print(name)

def redis_matching():
    # data is enriched in logstash
    conf = Configuration()
    r = redis.StrictRedis(host=conf.redis_host, port=conf.redis_port, db=conf.redis_db)

    match = SimpleQueue()
    if args.multiprocess > 0:
        n = min(args.multiprocess, cpu_count()-1)
        processes = list()
        for i in range(n):
            process = Process(target=redis_matching_process, args=(r, match))
            process.start()
            processes.append(process)

        # print match if there are some
        print_process = Process(target=print_queue_process, args=([match]))
        print_process.start()

        for process in processes:
            process.join()
        print_process.terminate()
    else:
        redis_matching_process(r, match)
        for item in iter_queue(match):
            print(item)

########
# Main #
########
if __name__ == "__main__":
    conf = Configuration
    rules = list()
    rule_location = conf.rule_location
    # get configuration
    metaParser = configparser.ConfigParser()
    metaParser.read(conf.rule_location + "/metadata")
    metadata = metaParser._sections
    metadata = metadata['crypto']
    metadata['dklen'] = int(metadata['dklen'])
    metadata['iterations'] = int(metadata['iterations'])

    # get rules from csv
    with open(conf.rule_location+"/rules.csv", "r") as f:
        data = csv.DictReader(f)
        # copy data
        for d in data:
            d['salt'] = b64decode(d['salt'])
            d['iv'] = int.from_bytes(b64decode(d['iv']), 'big')
            d['attributes'] = d['attributes'].split('||')
            d['ciphertext'] = b64decode(d['ciphertext'])
            rules.append(d)


    if not rules:
        sys.exit("No rules found.")
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
