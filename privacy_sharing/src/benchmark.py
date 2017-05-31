#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

"""
Tool to execute Benchmarks
"""

def bloomy():
    import benchmark.bloomy as bloomy
    bloomy.start()

def kdf():
    import benchmark.kdf as kdf
    kdf.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run tests')
    parser.add_argument('-a', '--all', dest='all', action='store_true', help='Runs all benchmarks')
    parser.add_argument('--bloomy', action='store_true', help='Runs bloomy benchmarks')
    parser.add_argument('--kdf', action='store_true', help='Runs key derivation function benchmarks')
    args = parser.parse_args()

    if args.all:
        bloomy()
        kdf()
    elif args.bloomy:
        bloomy()
    elif args.kdf:
        kdf()
    else:
        print("Chosse an argument (./benchmark.py -h)")
