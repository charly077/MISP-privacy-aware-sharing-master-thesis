"""
Cryptographic system with HKDF: HMAC-based Extract-and-Expand Key Derivation Function
Should be used only if the size of the domain of the type of data
is enough to avoid bruteforce attacks
"""
from pypraware_crypto.interface import Crypto
from pypraware_crypto.helper import *
import configparser
import glob, hashlib, os
from base64 import b64encode

# hash and crypto import
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

class HKDF(Crypto):
    def __init__(self, conf, metadata=None):
        self.conf = conf
        self.btoken = bytes(conf['misp']['token'], encoding='ascii')

        # For matching (only token is kept from config file)
        if metadata is not None:
            metadata = metadata['crypto']

    def derive_key(self, bpassword, bsalt, attr_types):
        """
        Generate the key used for encryption
        """
        passToken = bpassword + self.btoken
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=bsalt,
            info=self.btoken,
            backend=default_backend())

        return hkdf.derive(bpassword)

    def create_rule(self, ioc, message):
        salt = os.urandom(16)
        attr_types, password = get_types_values(ioc)
        dk = self.derive_key(password.encode('utf8'), salt, attr_types)
        return aes_create_rule(dk, message, attr_types, salt)

    def match(self, attributes, rule, queue):
        rule_attr = rule['attributes']
        match = False
        try:
            password = '||'.join([attributes[attr] for attr in rule_attr])
            attr_types = '||'.join(attr_type for attr_type in rule_attr)
        except:
            pass # Nothing to do
        dk = self.derive_key(password.encode('utf8'), rule['salt'], attr_types)
        ciphertext = [rule['ciphertext-check'], rule['ciphertext']]
        match, plaintext = aes_match_rule(dk, password, rule['nonce'],\
                ciphertext)

        if match:
            queue.put("IOC matched for: {}\nSecret Message (uuid-event id-date)\n===================================\n{}\n".format(attributes, plaintext.decode('utf-8')))



    def save_meta(self):
        meta = configparser.ConfigParser()
        meta['crypto'] = {}
        meta['crypto']['name'] = 'hkdf'
        with open(self.conf['rules']['location'] + '/metadata', 'w') as config:
            meta.write(config)

