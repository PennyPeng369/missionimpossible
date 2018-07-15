'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
	   Na Chang (858604)
	   Zepeng Dan (933678)
	   Junhan Liu (878637)
	   Peishan Li (905508)
'''
import boto 
from boto.ec2.regioninfo import RegionInfo
import time

import connector

def create_instance():
	ec2_conn = connector.get_conn()
	avail_zone = 'melbourne-qh2'
	
	print "creating instance"
	instance_pool = ec2_conn.run_instances('ami-e2d5e55e', #imageID
							key_name = 'Inst1',
							instance_type = 'm1.medium',
							security_groups = ['ssh','https','couchdb','erlang','icpm'],
							placement = avail_zone) 
	
	instance = instance_pool.instances[0]
	
	print "end of execution"
