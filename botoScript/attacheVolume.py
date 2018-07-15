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

def attach_volume():

	ec2_conn = connector.get_conn()
	vol_size = 40
	avail_zone = 'melbourne-qh2'
	
	instance_pool = ec2_conn.get_all_reservations()
	
	instance_list = []
	
	for i in range(4):
		instance_list.append(instance_pool[i].instances[0])
	
	
	print "checking the server instance"
	while instance_list[0].state_code != 16 or instance_list[1].state_code != 16 or instance_list[2].state_code != 16 or instance_list[3].state_code != 16:
		#print "instance status: ", instance.state_code, instance.state 
		time.sleep(5)
		#state = instance.state_code
	
	#print "creating volume..."
	
	inst_vol_list = []
	
	for i in range(len(instance_list)):
	
		volume_request = ec2_conn.create_volume(vol_size, avail_zone)
	
	for i in range(len(instance_list)):
		current_volume = ec2_conn.get_all_volumes()[i]
		inst_vol_list.append((instance_list[i], current_volume))
		#current_volume = ec2_conn.get_all_volumes()[0]
	
	
	print "attaching to volume..."
	for inst, vol in inst_vol_list:
		print "attaching to volume..."
		result = vol.attach(inst.id, '/dev/vdc')
		print result



