"""
Create an interface for the cryptographic functions
"""

class Crypto():
    def generate_salt():
        pass

    def derive_key(bpassword, bsalt, btoken, attr_types, dklen=None):
        """
        Generate the key further used for encryption
        """
        pass

    def encrypt(bmessage):
        """
        Use the generated key and salt to 
        encrypt the message
        """
        pass

    def match(bcipher, bpassword, bsalt):
        """
        Sometimes we don't need to decrypt the whole
        ciphertext to know if there is a match
        """
        pass

    def decrypt(bcipher, bpassword, bsalt):
        pass
