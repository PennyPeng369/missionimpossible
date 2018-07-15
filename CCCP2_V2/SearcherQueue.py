'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
       Na Chang (858604)
       Zepeng Dan (933678)
       Junhan Liu (878637)
       Peishan Li (905508)
'''
import pika
from CouchConnection import CouchConnection
import Credential
import json


class SearcherQueue:

    def __init__(self, queueName='searcherqueue', dbName=Credential.dbName):
        # Initialize Database
        self.queueName = queueName
        self.dbName = dbName
        self.count = 0

        try:
            # Initialize Queuing system

            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queueName)
            self.db = CouchConnection(dbName=self.dbName)

        except Exception as err:

            print 'Error Occured in Searchqueue %s' % err
        self.start()

    def callback(self, ch, method, properties, tweet):

        print '[%s] totalSaved' % self.count

        try:
            flag = self.db.save(json.loads(tweet))

            if flag is None:
                self.count = self.count + 1
                print 'done'

        except Exception as err:
            print 'problem occured in search callBack %s' % err

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback, queue=self.queueName)
        print "Rabbit Start, searqueue"
        self.channel.start_consuming()


sq = SearcherQueue()
