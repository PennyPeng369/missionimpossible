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
import json
import Credential


class StreamQueue:

    def __init__(self, queueName='streamqueue', dbName=Credential.dbName):
        self.queueName = queueName
        self.dbName = dbName
        self.count = 0

        try:

            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queueName)
            self.db = CouchConnection(dbName=self.dbName)
            self.streamDB = CouchConnection(dbName="stream_db")

        except Exception as e:
            print 'CouchdbError: %s' % e

        self.startStreaming()

    def callback(self, ch, method, properties, raw_data):

        print '[%s] received' % self.count

        try:
            tweet = json.loads(raw_data)
            flag = self.db.save(tweet)  # save to tweets pool that includes history tweets
            self.streamDB.save(tweet)   # save to fresh tweets pool
            if flag is None:
                self.count = self.count + 1
                print 'done'

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as err:
            print 'problem occured in callBack %s' % err

    def startStreaming(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback, queue=self.queueName)
        print 'Streaming queue building completed'
        self.channel.start_consuming()


s = StreamQueue()
