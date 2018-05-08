'''
Team: Team 22
City: Melbourne
Name: Na Chang
Student ID: 858604
'''

import couchdb
import json

local_addr = 'http://admin:admin@localhost:5984'
remote_addr = 'http://admin:admin@115.146.86.131:5984'
remote_addr_secondary = 'http://admin:admin@115.146.85.205:5984'

#db_name = 'analysis'
db_server = couchdb.Server(remote_addr)


def dbConnect(db_name = 'tweets'):


	counter = 2
	addr = remote_addr
	while counter > 0:
		try:
			db_server = couchdb.Server(addr)
			return db_server[db_name]

		except: 
			print "connection to ", addr, " failed"
		counter -= 1
		addr = remote_addr_secondary
	
	return None



