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

def start(name='kdf'):
    """
    Creates two csv files with the results:
        - name + _pbkdf2.csv
        - name + _bcrypt.csv
    """
    print('Start Key Derivation Function benchmark')

    # Tests
    with open(name + '.csv', 'w') as f:
        f.write("nIP,iterations,rate, pbkdf2, bloomy\n")
        f.flush() # have result time to time


########
# Main #
########
if __name__ == "__main__":
    start()
