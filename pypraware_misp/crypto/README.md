# Crypto System package
Cryptographic functions used for matching or creating rules are implemented as modules.


# Improve the matching performance with bloom filters
In order to improve the performance of the matching script,
the idea was to add a bloom filter with a chosen false positive rate (Configuration file).

For that, only need to add 'bloomy\_' before the name of the crypto module to use in the configuration file.

ex: [rules][cryptomodule] pbkdf2 => bloomy\_pbkdf2

# List

- pbkdf2 (NIST recommended KDF, PKCS #5 v2.0, RFC 2898)
- bcrypt (slower)
- hkdf (Faster, for data where bruteforce is not a problem)
- SHA256, SHA384, SHA512 (if needed)
- bloom\_filter (mostly used for the bloomy implementation)


# Add a crypto system
- Create a new python3 class that implements Crypto from interface.py
- Modify choose\_crypto.py to import the right functions
