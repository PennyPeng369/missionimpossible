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
from multiprocessing import Process, Queue,Pool

def get_geo(latitude,longitude):
    geo_info = rg.search((latitude, longitude),mode=1)
    city = geo_info[0]['admin2']
    return city

def count_senti(row,counts):
    try:
        value = row.value
        coordinates=value[2]['boundingBox']['coordinates'][0][0]
        longitude=coordinates[0]
        latitude=coordinates[1]
        language=value[3]
        if language!='en':
            return counts
        city=get_geo(latitude,longitude)
        if city =='':
            return counts
        score = sentiment_score(value[0])
    except:
        return counts

    data_city = counts.get(city, {})
    data_city['totalTweet'] = data_city.get('totalTweet', 0) + 1
    data_city['totalSenti'] = data_city.get('totalSenti', 0) + score
    if score > 0.1:
        data_city['totalPos'] = data_city.get('totalPos', 0) + 1
        data_city.setdefault('totalNeg', 0)
    else:
        data_city['totalNeg'] = data_city.get('totalNeg', 0) + 1
        data_city.setdefault('totalPos', 0)
    counts[city] = data_city

    return counts


def process_func(tuple):
    skip = tuple[0]
    doc_count = tuple[1]
    batch = tuple[2]
    couchserver = couchdb.Server("http://admin:admin@115.146.86.131:5984/")
    db_analysis = couchserver['tweets']
    counts={}
    while skip < doc_count:
        limit = batch if doc_count - skip > batch else doc_count - skip
        rows = db_analysis.view('cities/sentiView', skip=skip, limit=limit)

        for row in rows:
            counts = count_senti(row, counts)

        skip += limit
        print skip

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

def init_pool():
    pool = Pool()
    #58417
    doc_num=610000
    ave=doc_num/4
    batch=5000
    print (0, ave, batch), (ave, 2*ave, batch), (2*ave, 3*ave, batch), (3*ave, doc_num, batch)
    result = pool.map(process_func, [(0, ave, batch), (ave, 2*ave, batch), (2*ave, 3*ave, batch), (3*ave, doc_num, batch)])
    # result = pool.map(process_func, [(0,2500,300), (2500,5000,300), (5000,7500,300),(7500,10000,300)])
    pool.close()
    pool.join()
    counts = count_gather(result)
    return counts

def write_file(data):
    f=open('CityPage610000.json','w')
    f.write(json.dumps(data))
    f.close()

if __name__=='__main__':
    counts=init_pool()
    write_file(counts)









