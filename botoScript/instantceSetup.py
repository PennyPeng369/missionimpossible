'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
	   Na Chang (858604)
	   Zepeng Dan (933678)
	   Junhan Liu (878637)
	   Peishan Li (905508)
'''

import attacheVolume, createInstance

counter = 4

while counter > 0:
	createInstance.create_instance()
	counter -= 1

attacheVolume.attach_volume()