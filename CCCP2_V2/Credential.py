'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
     Na Chang (858604)
     Zepeng Dan (933678)
     Junhan Liu (878637)
     Peishan Li (905508)
'''
from tweepy import *
from TwitterAuth import userAuth

ausLocation = [112.7190591613,
               -43.8414384519,
               154.2796384016,
               -10.4986145114]

ausBox = [[112.921114, -43.740482],
          [112.921114, -9.142176],
          [159.109219, -9.142176],
          [159.109219, -43.740482]]

dbName = "tweets"
couchAddress = "http://admin:admin@115.146.86.131:5984/"


def getTwitterAuth(user="Liu1"):

    try:
        user = userAuth[user]
        authentication = OAuthHandler(user.cKey, user.cSec)
        authentication.set_access_token(user.aToken, user.aSec)
        return authentication

    except ValueError:
        print "No such user!"
