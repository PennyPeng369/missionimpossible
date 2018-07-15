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
from RabbitListener import RabbitListener
from HeartBeat import HeartBeat

authName = "Liu4"
auth = Credential.getTwitterAuth(authName)
api = tweepy.API(auth)


def startStreamer():
    heart = HeartBeat(6000)
    heart.start()
    streamAPI = tweepy.Stream(auth=auth, listener=RabbitListener(api))

    ausLocation = Credential.ausLocation

    streamAPI.filter(locations=ausLocation, async=True)

startStreamer()
