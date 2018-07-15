'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
       Na Chang (858604)
       Zepeng Dan (933678)
       Junhan Liu (878637)
       Peishan Li (905508)
'''

import couchdb
import Credential
import json


class VicCouchConnection:

    def __init__(self, dbName=Credential.dbName, address=Credential.couchAddress):

        try:
            self.server = couchdb.Server(address)
            if dbName in self.server:
                self.db = self.server[dbName]
            else:
                self.db = self.server.create(dbName)

        except couchdb.HTTPError as e:
            print "Connection error: %s" % e

    def save(self, data):

        info = self.mapData(data)

        try:
            self.db[info[0]] = info[1]
            # print("valid id: %s" % info[0])

        except couchdb.http.ResourceConflict:

            # print("id conflict: %s" % info[0])
            return info[0]  # return conflict id

    @staticmethod
    def mapData(listData):

        docID = listData[0]

        try:
            data = {
                "id": docID,
                "createdTime": listData[1],
                "text": listData[2],
                "lat": listData[3],
                "long": listData[4],
            }
        except TypeError:

            print "Type Error"
            return False
            pass

        return docID, data

