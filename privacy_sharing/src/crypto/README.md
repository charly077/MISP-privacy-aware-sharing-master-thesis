# Crypto System package
The idea was to be able to add as many crypto systems as we want.

# Improve the matching performance thanks to bloom filters
In order to improve the performance of the key derivation function,
the idea was to add a bloom filter with a 0.5 false positive rate.

For that, only need to add 'bloomy\_' before the name of the crypto module to use in the configuration file.

# Add a crypto system
- Create a new python3 class that implements Crypto from interface.py
- Modify choose_crypto.py to import the right functions
