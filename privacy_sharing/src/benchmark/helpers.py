#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
read/write misp database for testing purpose
(Easier to directly user mysql)
"""
from configuration import Configuration

import random, os, sys
import shlex
import subprocess

class DatabaseHelper:
    # mysql import
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import create_engine
    from sqlalchemy.schema import MetaData
    # connection
    def __init__(self):
        conf = Configuration()
        Base = automap_base()
        engine = create_engine('mysql://{}:{}@{}/{}'.format(conf['mysql']['user'], conf['mysql']['password'], conf['mysql']['host'], conf['mysql']['dbname']))

        Base.prepare(engine, reflect=True)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        self.conn = engine.connect()
    	
    # close database
    def closedb(self):
        self.conn.close()

    # rename de db, create one for test
    def saveAttr(self):
            self.conn.execute("RENAME TABLE attributes TO saved_attributes")
            self.conn.execute("CREATE TABLE attributes LIKE saved_attributes")
            # for safety:
            self.conn.execute("INSERT INTO attributes (uuid, event_id, sharing_group_id, category, type, to_ids, value1, value2, comment) values('removable', 0, 0, 'external analysis', 'test', 0, 'removable', '', 'Testing table that can be removed')")

        # delete attributes and rename saved_attributes to attributes
    def restoreAttr(self):
            c = "SELECT value1 FROM attributes where attributes.type='test'" 
            for val in self.conn.execute(c):
                if val[0] == 'removable':
                    self.conn.execute("DROP TABLE attributes")
                    self.conn.execute("RENAME TABLE saved_attributes TO attributes")

    # add a random ip
    def addRandomIP(self):
            uuid = "select count(*) from attributes;"
            for val in self.conn.execute(uuid):
                uuid = val[0]
            self.conn.execute("INSERT INTO attributes (uuid, event_id, sharing_group_id, category, type, to_ids, value1, value2, comment) values('"+str(uuid+1)+"', 0, 0, 'external analysis', 'ip-dst', 1, '" + randIPv4() + "', '', 'Testing: Random IP for testbench :)')")

    def addNRandomIP(self, N):
            for i in range(N):
                self.addRandomIP()



#################
# IP Generation #
#################
def createNRandomIP(N):
    IPs = []
    i = 0
    while i < N:
        ip = randIPv4192168()
        if ip not in IPs:
            IPs.append(ip)
            i += 1
        else:
            print("Oups pas de bol %d" % N)
    return IPs

def createNRandomIPRes(N):
    if N > 20*256/2:
        print("N exceeds the maximum value")
        sys.exit(1)

    # remove misp_events.csv
    if os.path.exists('../res/misp_events.csv'):
        os.remove('../res/misp_events.csv')

    header = 'uuid,event_id,category,type,value,comment,to_ids,date'
    CSV = [header]
    IPs = createNRandomIP(N)
    for i,IP in enumerate(IPs):
        CSV.append(str(i+1) + ',' + str(i+1) + ',test,ip-dst,' + IP + ',comment,1,20170516')

    with open('../res/misp_events.csv', 'w') as f:
        f.write('\n'.join(CSV))

def randStr():
    return str(round(random.uniform(0,255)))

def randStr10():
    return str(round(random.uniform(0,9)))

def randIPv4():
    return randStr() + '.' + randStr() + '.' + randStr() + '.' + randStr()

def randIPv4192168():
    return '192.168.' + randStr10() + '.' + randStr()

###############
# Run helpers #
###############
def create_rules():
    command = "./readMisp.py --misp res -v"
    args = shlex.split(command)
    subprocess.call(args)

def bruteforceIP():
    command = './matchRules.py --input rangeip'
    args = shlex.split(command)
    subprocess.call(args)
