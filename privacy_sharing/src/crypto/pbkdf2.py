"""
Create an abstract class for the cryptographic functions
"""
from crypto.interface import Crypto
import configparser
import glob, hashlib, os
from base64 import b64encode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class Pbkdf2(Crypto):
    def __init__(self, conf):
        self.conf = conf
        self.hash_name = conf['pbkdf2']['hash_name']
        self.dklen = int(conf['pbkdf2']['dklen'])
        self.btoken = bytes(conf['misp']['token'], encoding='ascii')
        self.iterations = int(self.conf['pbkdf2']['iterations'])
        self.ipiterations = int(self.conf['pbkdf2']['ipiterations'])


    def derive_key(self, bpassword, bsalt, attr_types):
        """
        Generate the key further used for encryption
        """
        it = 1
        if attr_types in ["ip-dst", "ip-src", "ip-src||port", "ip-dst||port"]:
            it = self.ipiterations
        else:
            it = self.iterations
        return hashlib.pbkdf2_hmac(self.hash_name, bpassword + self.btoken, bsalt, it, dklen=self.dklen)

    def encrypt(self, attr_types, password, message):
        """
        Use the generated key and salt to 
        encrypt the message
        """
        key = self.derive_key(...)
        
    def create_rule(self, ioc, message):
        nonce = os.urandom(16)
        salt = os.urandom(hashlib.new(self.hash_name).digest_size)

        # Spit + redo allow to ensure the same order to create the password
        attr_types = '||'.join(attr_type for attr_type in ioc)
        password = '||'.join(ioc[attr_type] for attr_type in ioc)

        # encrypt the message
        dk = self.derive_key(password.encode('utf8'), salt, attr_types)

        backend = default_backend()
        cipher = Cipher(algorithms.AES(dk), modes.CTR(nonce), backend=backend)
        encryptor = cipher.encryptor()
        ct_check = encryptor.update(b'\x00'*16)
        ct_message = encryptor.update(message.encode('utf-8'))
        ct_message += encryptor.finalize()

        # create the rule
        rule = {}
        rule['salt'] = b64encode(salt).decode('ascii')
        rule['attributes'] = attr_types
        rule['nonce'] = b64encode(nonce).decode('ascii')
        rule['ciphertext-check'] = b64encode(ct_check).decode('ascii')
        rule['ciphertext'] = b64encode(ct_message).decode('ascii')

        return rule


    def match(self, bcipher, bpassword, bsalt):
        """
        Sometimes we don't need to decrypt the whole
        ciphertext to know if there is a match
        """
        pass


    def save_meta(self):
        meta = configparser.ConfigParser()
        meta['crypto'] = {}
        meta['crypto']['hash_name'] = self.conf['pbkdf2']['hash_name']
        meta['crypto']['dklen'] = self.conf['pbkdf2']['dklen'] # AES block size
        meta['crypto']['iterations'] = str(self.iterations)
        meta['crypto']['ipiterations'] = str(self.ipiterations)
        with open(self.conf['rules']['location'] + '/metadata', 'w') as config:
            meta.write(config)

