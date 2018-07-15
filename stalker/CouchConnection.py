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


class CouchConnection:

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

        if info is not False:
            try:
                self.db[info[0]] = info[1]
                # print("valid id: %s" % info[0])

            except couchdb.http.ResourceConflict:

                # print("id conflict: %s" % info[0])
                return info[0]  # return conflict id
        else:
            return False

    @staticmethod
    def mapData(jsonObj):

        docID = jsonObj["id_str"]

        try:
            data = {

                "id": jsonObj["id_str"],
                "createdAt": jsonObj["created_at"],
                "text": jsonObj["text"],
                "user": {
                    "id": jsonObj["user"]["id_str"],
                    "name": jsonObj["user"]["name"] if jsonObj["user"]["name"] else None,
                    "screenName": jsonObj["user"]["screen_name"],
                    "location": jsonObj["user"]["location"] if jsonObj["user"]["location"] else None,
                    "friendsCount": jsonObj["user"]["friends_count"],
                    "followersCount": jsonObj["user"]["followers_count"],
                    "createdAt": jsonObj["user"]["created_at"]
                },
                "coordinates": jsonObj["coordinates"] if jsonObj["coordinates"] else None,
                "place": {
                    "id": jsonObj["place"]["id"] if jsonObj["place"]["id"] else None,
                    "placeType": jsonObj["place"]["place_type"] if jsonObj["place"]["place_type"] else None,
                    "name": jsonObj["place"]["name"] if jsonObj["place"]["name"] else None,
                    "fullName": jsonObj["place"]["full_name"] if jsonObj["place"]["full_name"] else None,
                    "countryCode": jsonObj["place"]["country_code"] if jsonObj["place"]["country_code"] else None,
                    "boundingBox": jsonObj["place"]["bounding_box"] if jsonObj["place"]["bounding_box"] else
                    jsonObj[[jsonObj["coordinates"]]]
                },
                "hashTags": jsonObj["entities"]["hashtags"] if jsonObj["entities"]["hashtags"] else None,
                "language": jsonObj["lang"]
            }
        except TypeError as e:
            print "Type Error %s" % e
            return False
        except (ValueError, KeyError) as e:
            print 'value or key error %s' % e
            return False

        return docID, data

