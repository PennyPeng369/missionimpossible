'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
       Na Chang (858604)
       Zepeng Dan (933678)
       Junhan Liu (878637)
       Peishan Li (905508)
'''
import couchdb
from sentiment import sentiment_score,sentiment_scores_of_sents
import reverse_geocoder as rg
import json

def count_update(score,city,counts):

    return counts

def get_geo(latitude,longitude):
    geo_info = rg.search((latitude, longitude))
    # state=geo_info[0]['admin1']
    city = geo_info[0]['admin2']
    # suburb = geo_info[0]['name']
    return city

def count_senti(row,counts):
    value = row.value
    coordinates=value[2]['boundingBox']['coordinates'][0][0]
    longitude=coordinates[0]
    latitude=coordinates[1]
    language=value[3]
    if language!='en':
        return counts
    time=value[1]
    city=get_geo(latitude,longitude)
    score = sentiment_score(value[0])
    data_city = counts.get(city, {})
    data_city['totalTweet'] = data_city.get('totalTweet', 0) + 1
    data_city['totalSenti'] = data_city.get('totalSenti', 0) + score
    if score > 0.2:
        data_city['totalPos'] = data_city.get('totalPos', 0) + 1
        data_city.setdefault('totalNeg', 0)
    else:
        data_city['totalNeg'] = data_city.get('totalNeg', 0) + 1
        data_city.setdefault('totalPos', 0)
    counts[city] = data_city
    return counts

def count_gather(gathered_counts):
    combined_counts = {}
    for counts in gathered_counts:
        for city in counts.keys():
            counts_city = counts[city]
            combined_city = combined_counts.get(city, {})
            combined_city['totalTweet'] = combined_city.get('totalTweet', 0) + counts_city['totalTweet']
            combined_city['totalPos'] = combined_city.get('totalPos', 0) + counts_city['totalPos']
            combined_city['totalNeg'] = combined_city.get('totalNeg', 0) + counts_city['totalNeg']
            combined_city['totalSenti'] = combined_city.get('totalSenti', 0) + counts_city['totalSenti']
            combined_counts[city] = combined_city
    return combined_counts

def write_file(data):
    f=open('CityPage.json','w')
    f.write(json.dumps(data))
    f.close()

if __name__=='__main__':

    batch = 300
    user = "admin"
    password = "admin"
    couchserver = couchdb.Server("http://%s:%s@115.146.86.131:5984/" % (user, password))
    db_analysis = couchserver['analysis']
    info = db_analysis.info()
    doc_count = info['doc_count']
    doc_count = 10000
    skip = 0
    counts={}
    while skip < doc_count:
        limit = batch if doc_count - skip > batch else doc_count - skip
        rows = db_analysis.view('SentiDesign/sentiView', skip=skip, limit=limit)

        for row in rows:
            counts=count_senti(row,counts)

        skip += limit
        print skip




