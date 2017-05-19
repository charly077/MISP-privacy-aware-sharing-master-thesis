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
import subprocess
import configparser

<<<<<<< HEAD
nIPs = 100
nIterations = 100
FP = .1
stepIP = 100
stepIterations = 100
stepFP = .1
maxIP = 1000
maxIterations = 1000
maxFP = .9
=======
>>>>>>> ff2dc9034cf66a580131474d41e576feabf4f096

def start(name='ip_iterations_bruteforce'):
    nIPs = 100
    nIterations = 1
    FP = .1
    stepIP = 100
    stepIterations = 100
    stepFP = .05
    maxIP = (20*256) // 3 
    maxIterations = 10000
    maxFP = .9

    rangeFP = [FP + stepFP*x for x in range(int((maxFP - FP)/stepFP))]
    print('Start Bloomy benchmark')
    configurationSave()
    # Configuration:
    configSet('rules', 'cryptomodule', 'bloomy_pbkdf2')

    # Tests
    with open(name + '.csv', 'w') as f:
        f.write("nIP,iterations,rate, pbkdf2, bloomy\n")
        for nIP in range(nIPs, maxIP, stepIP):
            # Generate IPs
            print("Genereate IPs")
            createNRandomIPRes(nIPs)
            for iterations in range(nIterations, maxIterations, stepIterations):
                # Set Config
                configSet('pbkdf2', 'ipiterations', iterations)
                pbkdf2Time = -1
                for rate in rangeFP:
                    print("Test :" + ','.join([str(nIP), str(iterations), str(rate)]))
                    # Set Config
                    configSet('bloomy', 'fp_rate', rate)
                    create_rules()

                    bloomyTime =  timeit.timeit("bruteforceIP()","from benchmark.helpers import bruteforceIP", number = 2)

                    # modify meta in order to forget about the bloom filter without regenerating everything (only once)
                    if pbkdf2Time == -1:
                        configSet('crypto', 'name', 'pbkdf2', '../rules/metadata')
                        pbkdf2Time =  timeit.timeit("bruteforceIP()","from benchmark.helpers import bruteforceIP", number = 2)

                    # Add result
                    f.write(','.join([str(x) for x in [nIP, iterations, rate, pbkdf2Time, bloomyTime]]) + '\n')
                    f.flush() # have result time to time

    configurationReset()

########
# Main #
########
if __name__ == "__main__":
    start()
