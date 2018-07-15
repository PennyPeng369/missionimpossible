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
import pika


class RabbitListener(tweepy.StreamListener):

    def __init__(self, api, hostAddr='127.0.0.1', queueName='streamqueue'):
        tweepy.StreamListener.__init__(self)
        self.hostAddr = hostAddr
        self.queueName = queueName
        self.api = api

        # Build queue connection
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostAddr))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queueName)

        except Exception as e:
            print e

    def on_data(self, raw_data):

        try:
            # Publish to receiver
            self.channel.basic_publish(exchange='',
                                       routing_key=self.queueName,
                                       body=raw_data)
        except Exception as e:

            print e

        return True

    def on_error(self, status_code):

        print "Error occured: %s" % status_code
        return True

    def on_disconnect(self, notice):

        print "Discontinued: %s" % notice
