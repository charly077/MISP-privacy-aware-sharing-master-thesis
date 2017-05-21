#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate graphs from csv
x in function of y
"""
import csv
import matplotlib.pyplot as plt

# Get result from file
bcrypt = []
with open('kdf_bcrypt.csv', 'r') as f:
    rows = csv.DictReader(f)
    for row in rows:
        bcrypt.append(row)

pbkdf2 = []
with open('kdf_pbkdf2.csv', 'r') as f:
    rows = csv.DictReader(f)
    for row in rows:
        pbkdf2.append(row)


rounds = []
time = []
for row in bcrypt:
    rounds.append(row['Rounds'])
    time.append(row['Time'])



plt.plot(rounds, time)
plt.xlabel('Number of rounds')
plt.ylabel('Time (s)')
plt.title('Bcrypt for a initial key of length 10')
plt.grid(True)
plt.show()


it = []
time = []
for row in pbkdf2:
    it.append(row['Iterations'])
    time.append(row['Time'])
plt.plot(it, time)
plt.xlabel('Number of iterations')
plt.ylabel('Time (s)')
plt.title('PBKDF2 for a initial key of length 10')
plt.grid(True)
plt.show()