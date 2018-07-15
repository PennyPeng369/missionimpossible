'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
       Na Chang (858604)
       Zepeng Dan (933678)
       Junhan Liu (878637)
       Peishan Li (905508)
'''
import datetime
import threading
import time


class HeartBeat(threading.Thread):

    def __init__(self, heartRate=60):
        threading.Thread.__init__(self)
        self.alive = False
        self.heartRate = heartRate
        print 'heatBeat rate is: 1 per %s seconds' % self.heartRate

    def run(self):
        self.alive = True

        while self.alive:
            print 'last beat: %s' % datetime.datetime.now()
            time.sleep(self.heartRate)

    def finish(self):

        print 'heatBeat stopped at: %s' % datetime.datetime.now()
        self.alive = False
