#!/usr/bin/env python3
# this code is inspired from https://github.com/CRIPTIM/private-IOC-sharing
# which is using the MIT license

# misp import
from decrypt_configuration import Configuration

# tools import
import argparse, configparser
import os, sys, glob, subprocess
from multiprocessing import SimpleQueue, Process, cpu_count, Lock
import json, csv, re
from functools import lru_cache
from copy import deepcopy
import redis
from url_normalize import url_normalize

# crypto import 
import hashlib
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

parser = argparse.ArgumentParser(description='Evaluate a network dump against rules.')
parser.add_argument('attribute', nargs='*', help='key-value attribute eg. ip=192.168.0.0 port=5012')
parser.add_argument('--input', default="argument",
        help='input is redis, argument or rangeip (testing purpose)')

parser.add_argument('-p', '--multiprocess', action='store',
        type=int, help='Use multiprocess, the maximum is the number of cores minus 1 (only for redis)', default=0, )
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

# from the csv file, read the rules and return them as a list
def rules_from_csv(filename, lock):
    lock.acquire()
    path = conf.rule_location+'/'+filename
    rules = list()
    if not os.path.exists(path):
        lock.release()
        return rules
    with open(path, "r") as f:
        data = csv.DictReader(f, delimiter='\t')
        # copy data
        for d in data:
            d['salt'] = b64decode(d['salt'])
            d['nonce'] = b64decode(d['nonce'])
            d['attributes'] = d['attributes'].split('||')
            d['ciphertext-check'] = b64decode(d['ciphertext-check'])
            d['ciphertext'] = b64decode(d['ciphertext'])
            rules.append(d)
    lock.release()
    return rules


file_attributes = {}
rules_dict = {}

def get_file_rules(filename, lock):
    try:
        rules = rules_dict[filename]
        return rules
    except:
        rules = rules_from_csv(filename, lock)
        rules_dict[filename] = rules
        return rules

def get_rules(attributes, lock):
    rules = list()
    # wich combinaison
    for filename in file_attributes:
        if all([i in attributes for i in file_attributes[filename]]):
            for rule in get_file_rules(filename, lock):
                rules.append(rule)
    return rules

# small normalization to increase matching
def normalize(ioc):
    for attr_type in ioc:
        # distinction bewtwee url|uri|link is often misused
        # Thus they are considered the same
        if attr_type == 'url' or\
            attr_type == 'uri' or\
            attr_type == 'link':
                ioc[attr_type] = url_normalize(ioc[attr_type])
        elif attr_type == 'hostname':
            ioc[attr_type] = ioc[attr_type].lower() 
    return ioc


#####################
# process functions #
#####################
def redis_matching_process(r, queue, lock):
    # get data
    log = r.rpop("logstash")
    while log:
        log = log.decode("utf8")
        log_dico = json.loads(log)
        dico_matching(log_dico, queue, lock)
        log = r.rpop("logstash")

def print_queue_process(queue):
    # this is an infinite loop as get waits when empty
    for elem in iter(queue.get, None):
       print(elem)



####################
# crypto functions #
####################
def derive_key(hash_name, bpassword, bsalt, iterations, ipiterations, btoken, attr_types, dklen=None):
    # iterations
    it = 1
    if '||'.join(attr_types) in ["ip-dst", "ip-src", "ip-src||port", "ip-dst||port"]:
        it = ipiterations
    else:
        it = iterations
    return hashlib.pbkdf2_hmac(hash_name, bpassword + btoken, bsalt, it, dklen=dklen)

#@lru_cache(maxsize=None)
def cryptographic_match(hash_name, password, salt, iterations, ipiterations, info, dklen, nonce, ciphertext, attr_types):
    dk = derive_key(hash_name, password.encode('utf8'), salt, iterations, ipiterations, bytes(info, encoding='ascii'), attr_types, dklen=dklen)

    backend = default_backend()
    cipher = Cipher(algorithms.AES(dk), modes.CTR(nonce), backend=backend)
    dec = cipher.decryptor()
    # A match is found when the first block is all null bytes
    if dec.update(ciphertext[0]) == b'\x00'*16:
        plaintext = dec.update(ciphertext[1]) + dec.finalize()
        return (True, plaintext)
    else:
        return (False, '')


###################
# match functions #
###################
def dico_matching(attributes, queue, lock):
    global conf
    global metadata
    # normalize data 
    attributes = normalize(attributes)
    # test each rules
    for rule in get_rules(attributes, lock):
        rule_attr = rule['attributes']
        password = ''
        try:
            password = '||'.join([attributes[attr] for attr in rule_attr])
        except:
            pass # nothing to do
        ciphertext = [rule['ciphertext-check'], rule['ciphertext']]
        match, plaintext = cryptographic_match(metadata['hash_name'], password, rule['salt'],\
                metadata['iterations'], metadata['ipiterations'], conf.misp_token,\
                metadata['dklen'], rule['nonce'], ciphertext, rule_attr)

        if match:
            queue.put("IOC matched for: {}\nSecret Message (uuid-event id-date)\n===================================\n{}\n".format(attributes, plaintext.decode('utf-8')))

def argument_matching(values=args.attribute):
    attributes = dict(pair.split("=") for pair in values)
    match = SimpleQueue()
    dico_matching(attributes, match, Lock())

    # print matches
    for match in iter_queue(match):
        print(match)

def rangeip_matching():
    for ip4 in range(256):
        ip=["ip-dst=192.168.0." + str(ip4)]
        argument_matching(ip)

def redis_matching():
    # data is enriched in logstash
    conf = Configuration()
    r = redis.StrictRedis(host=conf.redis_host, port=conf.redis_port, db=conf.redis_db)

    lock = Lock()
    match = SimpleQueue()
    if args.multiprocess > 0:
        n = min(args.multiprocess, cpu_count()-1)
        processes = list()
        for i in range(n):
            process = Process(target=redis_matching_process, args=(r, match, lock))
            process.start()
            processes.append(process)

        # print match if there are some
        print_process = Process(target=print_queue_process, args=([match]))
        print_process.start()
        for process in processes:
            process.join()
        print_process.terminate()
    else:
        redis_matching_process(r, match, lock)
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
    metadata['ipiterations'] = int(metadata['ipiterations'])

    if not os.path.exists(conf.rule_location):
        sys.exit("No rules found.")


    # get all files attribbutes
    filenames = os.listdir(conf.rule_location)
    for name in filenames:
        split = (name.split('.')[0]).split('_')
        file_attributes[name] = split

    if args.input == "redis":
        redis_matching()
    elif args.input == "rangeip":
        rangeip_matching()
    else:
        argument_matching()
