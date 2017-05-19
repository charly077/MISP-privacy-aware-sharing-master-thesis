#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evolution of the matching time for a complete /16 range
in function of the iteration number, the FP rate and the number of element 
inside the attribute compared to the standard PBKDF2 implementation
"""
from benchmark.helpers import createNRandomIPRes, create_rules, bruteforceIP
from configuration import configSet, configurationSave, configurationReset
import timeit
import configparser


def start(name='ip_iterations_bruteforce'):
    nIPs = 100
    nIterations = 100
    stepIP = 100
    stepIterations = 100
    maxIP = 1001
    maxIterations = 1001

    rangeFP = [0.2, 0.4, 0.6]
    print('Start Bloomy benchmark')
    configurationSave()
    # Configuration:
    configSet('rules', 'cryptomodule', 'bloomy_pbkdf2')

    # Tests
    with open(name + '.csv', 'w') as f:
        f.write("nIP,iterations,rate, pbkdf2, bloomy\n")
        for nIP in range(nIPs, maxIP, stepIP):
            # Generate IPs
            print("Generate IPs")
            createNRandomIPRes(nIP)
            for iterations in range(nIterations, maxIterations, stepIterations):
                # Set Config
                configSet('pbkdf2', 'ipiterations', iterations)
                pbkdf2Time = -1
                for rate in rangeFP:
                    print("Test :" + ','.join([str(nIP), str(iterations), str(rate)]))
                    # Set Config
                    configSet('bloomy', 'fp_rate', rate)
                    create_rules()

                    bloomyTime =  timeit.timeit("bruteforceIP()","from benchmark.helpers import bruteforceIP", number = 2)/2

                    # modify meta in order to forget about the bloom filter without regenerating everything (only once)
                    if pbkdf2Time == -1:
                        configSet('crypto', 'name', 'pbkdf2', '../rules/metadata')
                        pbkdf2Time =  timeit.timeit("bruteforceIP()","from benchmark.helpers import bruteforceIP", number = 2)/2

                    # Add result
                    f.write(','.join([str(x) for x in [nIP, iterations, rate, pbkdf2Time, bloomyTime]]) + '\n')
                    f.flush() # have result time to time

    configurationReset()

########
# Main #
########
if __name__ == "__main__":
    start()
