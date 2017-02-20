"""
Create an abstract class for the cryptographic functions
Configuration must me in the configuration file
"""

class Crypto():
    def create_rule(self, ioc, message):
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

    def save_meta(self):
        """
        Save metadata for the specific crypto system
        """
        pass
