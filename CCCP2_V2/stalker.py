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
from HeartBeat import HeartBeat

db = CouchConnection(dbName='stalker')
api = tweepy.API(Credential.getTwitterAuth("Stalker"), wait_on_rate_limit=True)

count = 0

heart = HeartBeat()
heart.start()


for line in open('mostTwitteUser.txt'):
    userName = line.split(',')[0]
    userID = line.split(',')[2]
    count = 0
    print 'digging %s' % userName
    count = count + 1
    try:
        for tweet in tweepy.Cursor(api.user_timeline, id=userID).items():
            text = tweet._json

            try:
                boundingBox = text['place']['bounding_box']['coordinates'][0]

                if boundingBox is not None and isIn(boundingBox):
                    db.save(text)
                    count += 1

            except Exception as e:
                pass

    except tweepy.error.TweepError as e:
        print e
        pass

    print 'userID: %s has %s tweets in box.' % (userID, count)

print 'finished!'
heart.finish()

