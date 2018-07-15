'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
	   Na Chang (858604)
	   Zepeng Dan (933678)
	   Junhan Liu (878637)
	   Peishan Li (905508)
'''

from VicCouchConnection import VicCouchConnection


def readFile():

    db = VicCouchConnection(dbName="vic_data")
    with open('tweet_Melbourne_subset.txt') as f:
        line = f.readline()

        while line:
            line = f.readline().decode('utf-8').strip().split('\t')
            print line
            # db.save(line)
            break

readFile()