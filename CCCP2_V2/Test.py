'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
	   Na Chang (858604)
	   Zepeng Dan (933678)
	   Junhan Liu (878637)
	   Peishan Li (905508)
'''
import tweepy
import Credential
from datetime import datetime, timedelta
import re

# api = tweepy.API(Credential.getTwitterAuth("Stalker"))
#
# placeCode = api.geo_search(query="AUS", granularity="country")[0].id
# placeQuery = 'place:' + placeCode

# tweetDate = "Fri Apr 20 21:14:52 +0000 2018"
# dateNow = datetime.now()
# fakeDate = '2011-03-02'
# while True:
#
#     for raw_tweet in tweepy.Cursor(api.user_timeline, id=348029933).items():
#         tweet = raw_tweet._json['created_at']
#
#         print tweet

# removeMs = lambda x: re.sub("\+\d+\s", "", x)
# mk_dt = lambda x: datetime.strptime(removeMs(x), "%a %b %d %H:%M:%S %Y")
# date = lambda x: "{:%Y-%m-%d}".format(mk_dt(x))
# datetime.strftime(dateNow, "%Y-%d-%m")
# d1 = datetime.strptime((datetime.strftime(datetime.now(), "%Y-%d-%m")), "%Y-%d-%m")
# # dateFormat = "%Y-%m-%d"


def formDate(tweetDate):

    removeMs = lambda x: re.sub("\+\d+\s", "", x)
    mk_dt = lambda x: datetime.strptime(removeMs(x), "%a %b %d %H:%M:%S %Y")
    date = lambda x: "{:%Y-%m-%d}".format(mk_dt(x))

    return date(tweetDate)


# print datetime.strptime(formDate(tweetDate), "%Y-%m-%d") - timedelta(days=7)

# today = datetime.today().date()
#
# dateCreated = datetime.strptime(formDate(tweetDate), dateFormat).date()
# print dateCreated > today
a = format(60, 'b')
b = format(13, 'b')
print 'a: %s' % a
print 'b: %s' % b

