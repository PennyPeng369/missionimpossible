from sentiment import sentiment_score,sentiment_scores_of_sents
from multiprocessing import Process, Queue,Pool
import reverse_geocoder as rg
import couchdb

def get_geo(lat,lon):
    geo_info = rg.search((lat, lon),mode=1)
    city = geo_info[0]['admin2']
    return city

def count_senti(row,counts):
    value = row.value
    coordinates = value[2]['boundingBox']['coordinates'][0][0]
    longitude = coordinates[0]
    latitude = coordinates[1]
    language = value[3]
    if language != 'en':
        return counts
    time = value[1]
    city = get_geo(latitude, longitude)
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


def process_func(tuple):
    skip=tuple[0]
    doc_count=tuple[1]
    batch=tuple[2]
    couchserver = couchdb.Server("http://admin:admin@115.146.86.131:5984/")
    db_analysis = couchserver['analysis']
    rows = db_analysis.view('SentiDesign/sentiView')
    counts = {}
    while skip < doc_count:
        limit = batch if doc_count - skip > batch else doc_count - skip
        rows = db_analysis.view('SentiDesign/sentiView', skip=skip, limit=limit)

        for row in rows:
            counts = count_senti(row, counts)

        skip += limit
        print skip

    return counts


def multipro_test():

    pool=Pool()
    result=pool.map(process_func,[(0,1,1),(0,2,1),(0,3,1),(0,4,1)])
    pool.close()
    pool.join()
    print result

def divide_doc():
    doc_num=58714
    ave=doc_num/4
    batch=300
    #result = pool.map(process_func, [(0, ave, batch), (ave, 2*ave, batch), (2*ave, 3*ave, batch), (3*ave, doc_num, batch)])
    print (0, ave, batch), (ave, 2*ave, batch), (2*ave, 3*ave, batch), (3*ave, doc_num, batch)

divide_doc()


# scores=sentiment_scores_of_sents(sents_list)
# multipro_test()

# senti_test()
#scores()
    # spark()
    # print rg.search((-37.8011,144.9789))
    # print rg.search((-37.8290,144.9570))
    # print rg.search((-37.8215,145.1260))
    # print rg.search((-37.8260, 145.0360))
    # count_update(0.9,"melbourne","carlton")
    # print json.dumps(counts)