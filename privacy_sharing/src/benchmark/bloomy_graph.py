#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate graphs from csv
x in function of y
"""
import csv
import matplotlib.pyplot as plt



################
# Parse values #
################
"""
Pour 200 ip, 200 iterations, 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 - vs standard
"""
"""
200,200,0.1,128.54801860299995,24.00833705449986
200,200,0.2,128.54801860299995,32.80486614649999
200,200,0.30000000000000004,128.54801860299995,44.09520444249938
200,200,0.4,128.54801860299995,55.24887130600109
200,200,0.5,128.54801860299995,68.70795204800015
200,200,0.6,128.54801860299995,77.7170775175
200,200,0.7000000000000001,128.54801860299995,93.82025254050313
200,200,0.8,128.54801860299995,113.23266721700202
200,200,0.9,128.54801860299995,125.90128009250111
"""
r1 = 128.54801860299995
r09 = 125.90128009250111
r08 = 113.23266721700202
r07 = 93.82025254050313
r06 = 77.7170775175
r05 = 68.70795204800015
r04 = 55.24887130600109
r03 = 44.09520444249938
r02 = 32.80486614649999
r01 = 24.00833705449986

rateFP = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
values = [r1, r09, r08, r07, r06, r05, r04, r03, r02, r01]

plt.figure(1)
plt.plot(rateFP, values)


plt.xlabel('Bloom Filter False Positive rate')
plt.ylabel('Time (s)')
plt.title('Impact of the Bloom Filter False Positive rate (Bloomy_)PBKDF2 for 200 iterations with 200 rules')
plt.grid(True)
plt.savefig("(Bloomy)PBKDF2-FPrate(200-200).png")
plt.show()



################
# Get result from file
results = []
with open('bloomy_results.csv', 'r') as f:
    rows = csv.DictReader(f)
    for row in rows:
        results.append(row)



################
"""
En abcise le nombre d'élements avec 100 iterations
graphe pbkdf2 - 0.2 - 0.4 - 0.6
"""
x = []
pbkdf2 = []
bloomy02 = []
bloomy04 = []
bloomy06 = []
for row in results:
    # X axis
    n = int(row['nIP'])
    if n not in x:
        x.append(n)

    # Y axis
    if int(row['iterations'])==200 :
        rate = float(row['rate'])
        if rate == 0.2:
            pbkdf2.append(float(row[' pbkdf2']))
            bloomy02.append(float(row[' bloomy']))
        elif rate == 0.4:
            bloomy04.append(float(row[' bloomy']))
        elif rate == 0.6:
            bloomy06.append(float(row[' bloomy']))

plt.figure(2)
nb, = plt.plot(x, pbkdf2, label='pbkdf2')
b02, = plt.plot(x, bloomy02, label='pbkdf2 - BF FP 0.2')
b04, = plt.plot(x, bloomy04, label='pbkdf2 - BF FP 0.4')
b06, = plt.plot(x, bloomy06, label='pbkdf2 - BF FP 0.6')


plt.xlabel('Number of ip-dst rules')
plt.ylabel('Time (s)')
plt.title('Impact of the number of IP rules on (Bloomy_)PBKDF2 for 200 iterations (192.168.{0-10}.0/24)')
plt.grid(True)
plt.legend(handles=[nb, b06, b04, b02])
plt.savefig("(Bloomy)PBKDF2-numberIP.png")
plt.show()

################
"""
En abcise le nombre d'iterations avec 200 elements 
graphe pbkdf2 - 0.2 - 0.4 - 0.6
"""
x = []
pbkdf2 = []
bloomy02 = []
bloomy04 = []
bloomy06 = []
for row in results:
    # X axis
    n = int(row['iterations'])
    if n not in x:
        x.append(n)

    # Y axis
    if int(row['nIP'])==200 :
        rate = float(row['rate'])   
        if rate == 0.2:
            pbkdf2.append(float(row[' pbkdf2']))
            bloomy02.append(float(row[' bloomy']))
        elif rate == 0.4:
            bloomy04.append(float(row[' bloomy']))
        elif rate == 0.6:
            bloomy06.append(float(row[' bloomy']))

plt.figure(3)
nb, = plt.plot(x, pbkdf2, label='pbkdf2')
b02, = plt.plot(x, bloomy02, label='pbkdf2 - BF FP 0.2')
b04, = plt.plot(x, bloomy04, label='pbkdf2 - BF FP 0.4')
b06, = plt.plot(x, bloomy06, label='pbkdf2 - BF FP 0.6')


plt.xlabel('Number of iterations')
plt.ylabel('Time (s)')
plt.title('Impact of the number of iterations on (Bloomy_)PBKDF2 for 200 IP rules (192.168.{0-10}.0/24)')
plt.grid(True)
plt.legend(handles=[nb, b06, b04, b02])
plt.savefig("(Bloomy)PBKDF2-numberiterations.png")
plt.show()


