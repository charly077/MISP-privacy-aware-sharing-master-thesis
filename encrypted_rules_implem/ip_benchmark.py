"""
Impact of the number of ip on time
"""
from helpers import DatabaseHelper as dh, randIPv4
from decrypt_frontend.match_rule import file_matching
import timeit


# create a file with random ip
def prepareBruteforce():
    with open("ips", 'w') as f:
        for i in range(100000):
            f.write(randIPv4() + "\n")
    
def bruteforceIP():
    file_matching("ips")

def test_ip():
    db = dh()
    db.saveAttr()
    for i in range(100):
        db.addNRandomIP(100)
        prepareBruteForce()
        print(timeit.timeit("bruteforceIP()","from __main__ import bruteforceIP", number = 100))

    db.restoreAttr()
    db.closedb()

test_ip()
