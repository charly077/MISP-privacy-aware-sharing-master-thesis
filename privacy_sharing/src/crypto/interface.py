"""
Create an abstract class for the cryptographic functions
"""

class Crypto():
    def generate_salt(self):
        self.salt = ''

    def set_salt(self, salt):
        self.salt = salt

    def derive_key(self, bpassword, btoken, attr_types, dklen=None):
        """
        Generate the key further used for encryption
        """
        pass

    def encrypt(self, bmessage):
        """
        Use the generated key and salt to 
        encrypt the message
        """
        pass

    def match(self, bcipher, bpassword, bsalt):
        """
        Sometimes we don't need to decrypt the whole
        ciphertext to know if there is a match
        """
        pass

    def decrypt(self, bcipher, bpassword, bsalt):
        pass
