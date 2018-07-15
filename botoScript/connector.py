'''depend: Python
	sudo apt-get update
	sodu apt-get install python-boto\
	pip install boto'''
	
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


avail_zone = 'melbourne-qh2'
region = RegionInfo(name=avail_zone, endpoint = 'nova.rc.nectar.org.au')


#my cloud
access_key = 'b32b5d7b630f4c248d86391ee1a28194'
secret_key = '6f3481428d7442d085d053af6e9b7659'

#project cloud
#access_key = '93711129c3584af7bb17cd0d25ef3017'
#secret_key = '962c8c989b464ee6a55875e17c0ddc71'


print "connecting to remote..."
ec2_conn = boto.connect_ec2(aws_access_key_id = access_key,
							aws_secret_access_key = secret_key,
							is_secure = True, #below all default
							region = region,
							port = 8773,
							path = '/services/Cloud',	
							validate_certs = False)

def get_conn():
	return ec2_conn


'''
print "getting images..."
images = ec2_conn.get_all_images()
for img in images:
	print img.id, img.name
'''






























