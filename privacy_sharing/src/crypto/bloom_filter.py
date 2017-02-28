"""
Cryptographic system for bloom filter
"""
from crypto.interface import Crypto
import configparser
import glob, hashlib, os
from base64 import b64encode

# hash and crypto import
from crypto.lib.python-bloomfilter.pybloom.pybloom import BloomFilter

class Bloom_filter(Crypto):
    def __init__(self, conf, metadata=None):
        self.conf = conf
        self.f = BloomFilter

    def create_rule(self, ioc, message):
        """
        We need to create one rule, thus we need a state
        """
        # Spit + redo allow to ensure the same order to create the password
        attr_types = '||'.join(attr_type for attr_type in ioc)
        password = '||'.join(ioc[attr_type] for attr_type in ioc)


        # create the rule
        rule = {}

        return rule


    def match(self, attributes, rule, queue):
        """
        Sometimes we don't need to decrypt the whole
        ciphertext to know if there is a match
        as it is the case here thanks to ctr mode
        """
        rule_attr = rule['attributes']
        password = ''
        try:
            password = '||'.join([attributes[attr] for attr in rule_attr])
            attr_types = '||'.join(attr_type for attr_type in rule_attr)
        except:
            pass # nothing to do
        if match:
            queue.put("IOC matched for: {}\nSecret Message (uuid-event id-date)\n===================================\n{}\n".format(attributes, plaintext.decode('utf-8')))



    def save_meta(self):
        meta = configparser.ConfigParser()
        meta['crypto'] = {}
        meta['crypto']['name'] = 'bloom_filter' 
        meta['crypto']['capacity'] = 
        meta['crypto']['error_rate'] = 
        with open(self.conf['rules']['location'] + '/metadata', 'w') as config:
            meta.write(config)

