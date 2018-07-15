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
from tweepy import error
import pika
from pika import exceptions
import sys
import json
import Counter
from datetime import datetime, timedelta
import re
from HeartBeat import HeartBeat


class Searcher:

    def __init__(self, api, queueName='searcherqueue'):
        self.api = api
        self.queueName = queueName
        self.maxID = sys.float_info.max
        self.heartBeat = HeartBeat(600)

        try:
            self.limitStatus = self.api.rate_limit_status()["resources"]["search"]

        except error.RateLimitError:

            self.limitStatus = None

        try:

            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queueName)

        except pika.exceptions as e:
            print 'RabbitSearchMQ connection failed: %s' % e

    def run(self):

        placeCode = self.api.geo_search(query="AUS", granularity="country")[0].id
        placeQuery = 'place:' + placeCode
        self.heartBeat.start()

        while True:

            print 'counter Start!'
            counter = Counter.Counter()
            global today
            today = counter.getToday()
            counter.start()

            for raw_tweet in tweepy.Cursor(self.api.search, q=placeQuery, max_id=self.maxID).items():

                targetID = raw_tweet._json['user']['id']
                tweetID = raw_tweet._json["id"]
                self.sendToQueue(raw_tweet._json)

                if str(self.maxID) > tweetID:
                    self.maxID = tweetID - 1
                    print 'new ID: %s' % self.maxID

                try:
                    self.findTweet([targetID], 'self')
                    self.digFriends([targetID])

                except (error.RateLimitError, error.TweepError):

                    timeElapsed = counter.finish()

                    print 'time reached %s' % timeElapsed
                    sleepTime = 900 - timeElapsed

                    try:
                        print 'limit in: %s the sys will sleep ' % sleepTime
                        self.connection.sleep(sleepTime)

                    except exceptions.ConnectionClosed:
                        self.connection.close()
                        self.reconnection()

                    print 'started'

                # except error.TweepError as e:
                    # print 'unalthorized %s' % e

                except exceptions.ConnectionClosed:
                    self.reconnection()

    def digFriends(self, target, loop=2, item=10):  # Dig user into their friends

            print target
            if loop > 0:
                friends = []

                for i in target:
                    for nameList in tweepy.Cursor(self.api.friends, id=i, wait_on_rate_limit=False).items(item):

                        friends.append(nameList.id)

                self.findTweet(friends, loop)
                self.digFriends(friends, loop-1, item-5)

    def findTweet(self, friends, l):
        print "layer %s" % l
        print 'friends: %s' % friends

        for f in friends:

            count = self.digOneYearInterval(f)

            print 'user %s has %s tweets in one year' % (f, count)

    def digOneYearInterval(self, userID):

        page = 1
        global deadEnd
        deadEnd = False
        count = 0
        print 'userID %s is being dig' % userID

        while True:

            tweets = self.api.user_timeline(id=userID, page=page)

            for tweet in tweets:

                body = tweet._json
                count += 1
                createdTime = body['created_at']

                if self.isInOneYear(createdTime) is True:

                    try:
                        box = body['place']['bounding_box']['coordinates'][0]

                        if (box is not None) and (self.isIn(box) is True):
                            self.sendToQueue(body)

                    except TypeError:
                        pass
                else:
                    deadEnd = True
                    return count

            if not deadEnd:
                page += 1

    @staticmethod
    def isIn(tweetCoord):

        # print tweetCoord
        ausBox = Credential.ausBox

        if ausBox[0][0] < tweetCoord[0][0] and ausBox[0][1] < tweetCoord[0][1] and ausBox[2][0] > \
                tweetCoord[2][0] and ausBox[2][1] > tweetCoord[2][1]:

            return True

        else:
            return False

    def sendToQueue(self, twitter):

        try:

            self.channel.basic_publish(exchange='',
                                       routing_key='searcherqueue',
                                       body=json.dumps(twitter))

        except exceptions.ConnectionClosed:
            self.reconnection()

    def isInOneYear(self, date_created):

        dateFormat = "%Y-%m-%d"
        created_date = datetime.strptime(self.formDate(date_created), dateFormat).date()

        if created_date > today - timedelta(days=365):
            return True
        else:
            return False

    @staticmethod
    def formDate(tweetDate):

        removeMs = lambda x: re.sub("\+\d+\s", "", x)
        mk_dt = lambda x: datetime.strptime(removeMs(x), "%a %b %d %H:%M:%S %Y")
        date = lambda x: "{:%Y-%m-%d}".format(mk_dt(x))

        return date(tweetDate)

    def reconnection(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queueName)


sc = Searcher(tweepy.API(Credential.getTwitterAuth("Dan1")))
sc.run()
