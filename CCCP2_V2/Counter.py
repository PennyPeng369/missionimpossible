'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
       Na Chang (858604)
       Zepeng Dan (933678)
       Junhan Liu (878637)
       Peishan Li (905508)
'''
import threading
import time
from datetime import datetime


class Counter(threading.Thread):

    def __init__(self, interval=0.1):
        threading.Thread.__init__(self)
        self.interval = interval
        self.value = 0
        self.alive = False

    def run(self):

        self.alive = True

        while self.alive:
            time.sleep(self.interval)
            self.value += self.interval

    def finish(self):

        self.alive = False
        return self.value

    def getToday(self):

        return datetime.today().date()
