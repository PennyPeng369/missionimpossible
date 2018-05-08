'''
Team: Team 22
City: Melbourne
Name: Na Chang
Student ID: 858604
'''

import couchConnector
import json
import itertools

from datetime import datetime
from dateutil import tz

from sentiment import sentiment_score as score

filehdle = open('mostTwitteUser.txt')

userid_pool = []
for line in filehdle:
    userid_pool.append(line.split(',')[2])

print len(userid_pool)


###START OF VAR###
pos_score_baseline = 0.2
view_name = 'formal/cooTwi'
#view_name = 'userID/user'
f_name = 'tracking.json'

###END OF VAR###


db = couchConnector.dbConnect(db_name = 'stalker')


###START OF CALCULATION METHODS###
def user_tweet_extract(userID):

    user_dict = {}

    time_slice = range(25)
    time_dict = {}
    for time_slot in time_slice:
        time_dict[str(format(time_slot,'02'))] = []

    tweet_list = db.view(view_name, key=userID)
    user_dict['totalTweet'] = len(tweet_list)
    user_dict['like'] = []

    user_dict['name'] = None
    user_dict['totalPos'] = 0
    user_dict['totalNeg'] = 0
    user_dict['tracking'] = time_dict
    user_dict['user_ID'] = userID

    topics = {}
    text = []

    for item in tweet_list:

        try:
            tweet = item.value

            tweet_text = tweet['text']

            coor = tweet['coordinates']['coordinates']

            time = time_convert(tweet['createdAt'])

            name = tweet['user']['name']

        except:
            print "data format error"
            continue

        text.append(tweet_text)
        user_dict['tracking'][time].append(coor)

        score = sentiment(tweet_text)

        if user_dict['name'] is None:
            user_dict['name'] = name
        if score >= pos_score_baseline:
            user_dict['totalPos'] += 1
        else:
            user_dict['totalNeg'] += 1
        topic = get_topic(tweet_text)
        topics[topic] = topics.get(topic,0) + 1

    user_dict['tweets'] = text

    for topic,value in topics.items():
        user_dict['like'].append({"topic":topic,"tweetcount":value})

    total_tracking = user_dict['tracking'].values()

    if len(list(itertools.chain(*total_tracking)))> 0:
        return user_dict
    else:
        return None

def time_convert(time):
    local_format = '%H:%M:%S'
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    time = time.split()
    day = time[0]
    utc_time = time[3]

    utc = datetime.strptime(utc_time, local_format)
    utc = utc.replace(tzinfo=from_zone)
    actual_time = utc.astimezone(to_zone).strftime(local_format)

    return actual_time.split(':')[0]


def sentiment(tweet):
    return score(tweet)


def get_topic(tweet):
    return None


def scan_user_list(userid_pool):
    userList = {}
    for id in userid_pool:
        if user_tweet_extract(id):
            userList[id] = (user_tweet_extract(id))
    return json.dumps(userList)
###END OF CALCULATION METHODS###


###START OF MAIN METHODS###
json_string = scan_user_list(userid_pool)
fhdle = open(f_name, 'a')
fhdle.write(json_string)
fhdle.flush()
fhdle.close()
###END OF MAIN METHODS###


