#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evolution of the time for key generation for :
    - PBKDF2
    - Bcrypt
in function of:
    - the complexity (respectively number of iterations and number of rounds)
"""
from configuration import configSet, configurationSave, configurationReset
import timeit

#timeit.timeit("bruteforceIP()","from benchmark.helpers import bruteforceIP", number = 2)
# /2

####################
# Setup for PBKDF2 #
####################

setupStartPBKDF2 = """
import hashlib, os
value = ''
attrType = 'test'
bsalt = os.urandom(hashlib.new('sha256').digest_size)
def kdf():
    hashlib.pbkdf2_hmac('sha256', """
# value
afterValuePBKDF2 = ", bsalt, "
# it
setupEndPBKDF2 = ', dklen=32)'

def pbkdf2_setup(val, it):
    val = bytes(val, encoding="utf-8")
    return setupStartPBKDF2 + str(val) + afterValuePBKDF2 + str(it) + setupEndPBKDF2

####################
# Setup for Bcrypt #
####################
setupStartBcrypt = '''
import hashlib, os, bcrypt
bsalt = os.urandom(hashlib.new('sha256').digest_size)
token_pass = '''


afterValueBcrypt = '''

def kdf():
    key =  bcrypt.kdf(password = token_pass, 
                salt = bsalt,
                desired_key_bytes = 32,
                rounds = '''
#round
setupEndPBKDF2 = ')'

def bcrypt_setup(val, round):
    val = bytes(val, encoding="utf-8")
    return setupStartBcrypt + str(val) + afterValueBcrypt + str(round) + setupEndPBKDF2

def values():
    val = 10*'a'
    yield val
    for i in range(1):
        val += 10*'a'
        yield val

def start(name='kdf'):
    """
    Creates two csv files with the results:
        - name + _pbkdf2.csv
        - name + _bcrypt.csv
    """
    print('Start Key Derivation Function benchmark')
    with open(name + '_pbkdf2.csv', 'w') as pbRes:
        with open(name + '_bcrypt.csv', 'w') as bcryptRes:
            # Write header
            pbRes.write('Length,Iterations,Time')
            bcryptRes.write('Length,Rounds,Time')
            val = 'aaaaaaaaaaaaaa'
            for i in range(1,51):
                print(i)
                time = timeit.timeit('kdf()', pbkdf2_setup(val, 10*i), number=2000)/2000
                pbRes.write('\n'+ str(len(val)) + ',' + str(10*i) + ',' + str(time))
                time = timeit.timeit('kdf()', bcrypt_setup(val, 2*i), number=100)/100
                bcryptRes.write('\n'+ str(len(val)) + ',' + str(2*i) + ',' + str(time))
                pbRes.flush()
                bcryptRes.flush()

########
# Main #
########
if __name__ == "__main__":
    start()
