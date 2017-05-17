#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evolution of the matching time for a complete /16 range
in function of the iteration number, the FP rate and the number of element 
inside the attribute compared to the standard PBKDF2 implementation

-> Pour match normalement on peut directement modifier dans les metadata des rules
-> Ensuite faire varier
"""
from helpers import DatabaseHelper as dh, randIPv4
import timeit, shlex, subprocess

nIPs = 0
nIterations = 1
FP = .1
stepIP = 100
stepIterations = 100
stepFP = .05
maxIP = (256*256) // 3 #21845
maxIterations = 10000
maxFP = .5


def create_rules():
    # TODO Modifier la configuration
    ...
    command = "./readMisp.py --misp res"
    args = shlex.split(command)
    subprocess.call(args)

def bruteforceIP():
    # TODO
    # pour avoir des mesures plus presices, il fautdrait trouver un moyen 
    # lancer la fonction avec un timeit et de la remettre à 0 genre timeit("import .. ")
    command = "./match_rules.py --input rangeip"
    args = shlex.split(command)
    subprocess.call(args)

def test_ip(name='ip_iterations_bruteforce'):
    db.addNRandomIP(nIP)
    results = []
    results.append("nIP,iterations,rate, pbkdf2, bloomy")
    for nIP in range(nIPs, maxIP, stepIP):
        # regenerate ip to test
        for iterations in range(nIterations, maxIterations, stepIterations):
            # change config
            for rate in range(FP, maxFP, stepFP):
                # change config
                # gen rules
                # timeit.timet(..., number=...) for bloomy_pbkf2
                # modify meta 
                # timeit.timet(..., number=...) for pbkdf2
                # add result line

            

    with open(name + '.csv', 'w') as f:
            f.write('\n'.join(results))

test_ip()
