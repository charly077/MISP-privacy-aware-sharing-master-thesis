#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
read/write misp database for testing purpose
"""
from encrypt_backend.configuration import Configuration as e_conf
# mysql import
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData, Table
from sqlalchemy.sql import select

class DatabaseHelper:
	# connection
	def __init__(self):
		Base = automap_base()
	    engine = create_engine('mysql://{}:{}@{}/{}'.format(e_conf.user, e_conf.password, e_conf.host, e_conf.dbname))

	    Base.prepare(engine, reflect=True)
	    metadata = MetaData()
	    metadata.reflect(bind=engine)
	    self.conn = engine.connect()
	    self.attributes_table = Table("attributes", metadata, autoload=True)
		
	# close database
	def closedb():
		self.connection.close()

	# Save all attr in database as a tsv file
	def saveAttr(self, attr_type):
		s = select([self.attributes_table]).where(self.attributes_table.c.attr_type == attr_type)
		results = self.conn.execute(s)
		for row in s:
			print(results)

	# Restore all attr in database from tsv file 
	def restoreAttr(self, attr_file):
		pass

	# add attr
	def addAttr(self, attr, attr_type):
		pass