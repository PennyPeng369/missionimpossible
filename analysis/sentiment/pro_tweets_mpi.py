"""
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
	  Na Chang (858604)
	  Zepeng Dan (933678)
	  Junhan Liu (878637)
	  Peishan Li (905508)
"""


import couchdb
from sentiment import sentiment_score,sentiment_scores_of_sents
import reverse_geocoder as rg
import json
from mpi4py import MPI

def count_update(score,city,counts):
    data_city = counts.get(city, {})
    data_city['totalTweet']=data_city.get('totalTweet',0)+1
    data_city['totalSenti']=data_city.get('totalSenti',0)+score
    if score>0.2:
        data_city['totalPos']=data_city.get('totalPos',0)+1
        data_city.setdefault('totalNeg',0)
    else:
        data_city['totalNeg']=data_city.get('totalNeg',0)+1
        data_city.setdefault('totalPos',0)
    counts[city]=data_city
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
    counts=count_update(score,city,counts)
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

    comm = MPI.COMM_WORLD
    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()

    batch = 300

    if comm_rank==0:
        user = "admin"
        password = "admin"
        couchserver = couchdb.Server("http://%s:%s@115.146.86.131:5984/" % (user, password))
        db_analysis = couchserver['analysis']
        info = db_analysis.info()
        doc_count = info['doc_count']
        doc_count = 10000
        # for i in range(comm_size-1):
        #     comm.send(doc_count,dest=i+1)
        skip = 0
        print "connected to db"
        i=0
        while skip < doc_count:
            limit = batch if doc_count - skip > batch else doc_count - skip
            rows = db_analysis.view('SentiDesign/sentiView', skip=skip, limit=limit)
            for index,row in enumerate(rows):
                comm.send(row,index%(comm_size-1)+1)
                i+=1
            skip += limit
            print skip
        print "send times: "+str(i)
    else:
        counts={}
        # doc_count=comm.recv(source=0)
        doc_count=10000
        if (doc_count % batch)%(comm_size-1) >= comm_rank :
            times = int(doc_count / (comm_size-1)) + 1
        else:
            times = int(doc_count / (comm_size-1))
        print "times: "+str(times)
        time=0
        while(time<times):
            # print "slave is waiting..."
            local_row=comm.recv(source=0)
            # print "slave is computing..."
            counts = count_senti(local_row, counts)
            time+=1
            if time%1000==0:
                print "slave has recieved" +str(time)+"times"
        print "slave prepare to send"
        comm.send(counts,dest=0)
        print "slave send"


    if comm_rank == 0:
        combined_counts=[]
        for i in range(1,comm_size):
            counts_data = comm.recv(source=i)
            combined_counts.append(counts_data)
        results = count_gather(combined_counts)
        write_file(results)






