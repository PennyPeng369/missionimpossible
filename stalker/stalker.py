'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
	   Na Chang (858604)
	   Zepeng Dan (933678)
	   Junhan Liu (878637)
	   Peishan Li (905508)
'''
import Credential
import tweepy
from CouchConnection import CouchConnection

db = CouchConnection(dbName='stalker')
api = tweepy.API(Credential.getTwitterAuth("Stalker"), wait_on_rate_limit=True)

count = 0


def isIn(tweetCoord):
    print tweetCoord

    ausBox = Credential.ausBox

    if ausBox[0][0] < tweetCoord[0][0] and ausBox[0][1] < tweetCoord[0][1] and ausBox[2][0] > \
            tweetCoord[2][0] and ausBox[2][1] > tweetCoord[2][1]:
        return True
    else:
        return False


def findTweet(userID):
    pass


for line in open('mostTwitteUser.txt'):

    userID = line.split(',')[2]

    print 'user Count %s' % count
    count = count + 1
    for tweet in tweepy.Cursor(api.user_timeline, id=userID).items():

        text = tweet._json

        try:
            boundingBox = text['place']['bounding_box']['coordinates'][0]

            if boundingBox is not None and isIn(boundingBox):
                db.save(text)

        except Exception as e:
            print text["place"]
            print e




