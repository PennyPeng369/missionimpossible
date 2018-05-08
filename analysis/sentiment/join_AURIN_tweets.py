import json


def get_city_map():
    with open("CityMap.json","r") as f:
        city_map=f.read()
    return json.loads(city_map)


def get_aurin_health():
    with open("HealthAU.json","r") as f:
        aurin_health=f.read()
    return json.loads(aurin_health)


def get_aurin_income():
    with open("Income.json","r") as f:
        aurin_income=f.read()
    return json.loads(aurin_income)


def get_senti():
    with open("CityPage620000.json","r") as f:
        senti_data=f.read()
    return json.loads(senti_data)

def get_main_cities(city_map,aurin_health,aurin_income,senti_data):
    health_cities=aurin_health.keys()
    income_cities=aurin_income.keys()
    senti_cities=senti_data.keys()
    map_cities={}
    for city in city_map.keys():
        cities=city_map[city]
        for c in cities:
            map_cities[c]=city
    intersect_cities= list(set(health_cities) & set(income_cities) & set(senti_cities) & set(map_cities.keys()))
    print len(intersect_cities)

    main_cities={}
    for c in senti_data.keys():
        if c not in intersect_cities:
            continue
        c_senti=senti_data[c]
        total_pos=c_senti["totalPos"]
        total_neg=c_senti["totalNeg"]
        total_senti=c_senti["totalSenti"]
        total_tweet=c_senti["totalTweet"]
        income=aurin_income[c]["income"]
        health=aurin_health[c]["fair_poor"]
        city=map_cities[c]
        great_city=main_cities.get(city,{})
        cities=great_city.get("cities",{})
        origin_len=len(cities)
        c_senti["income"]=income
        c_senti["health"]=health
        cities[c]=c_senti
        great_city["cities"]=cities
        great_city["income"] =(income + origin_len*great_city.get("income",0.0))/len(cities)
        great_city["health"] =(health + origin_len*great_city.get("health",0.0))/len(cities)
        great_city["totalTweet"] =total_tweet + great_city.get("totalTweet",0)
        great_city["totalPos"] =total_pos+great_city.get("totalPos",0)
        great_city["totalNeg"] =total_neg+great_city.get("totalNeg",0)
        great_city["totalSenti"] =total_senti+great_city.get("totalSenti",0)
        great_city.setdefault("city_name",city)
        main_cities[city]=great_city

    f = open('cityDetail.json', 'w')
    f.write(json.dumps(main_cities))
    f.close()

def get_city_list():
    with open("cityList.json","r") as f:
        city_data=json.loads(f.read())

    with open("cityDetail.json","r") as f:
        city_detail=json.loads(f.read())

    city_list=city_data["cityList"]
    for i in range(len(city_list)):
        city_name=city_list[i]["content"]["name"]
        print city_name
        total_tweet=city_detail[city_name]["totalTweet"]
        total_pos=city_detail[city_name]["totalPos"]
        total_neg=city_detail[city_name]["totalNeg"]
        pro_neg=100*float(total_neg)/total_tweet
        pro_pos=100*float(total_pos)/total_tweet
        city_list[i]["content"]["Pos"]="Pos:"+str(pro_pos)+"%"
        city_list[i]["content"]["Neg"] = "Pos:" + str(pro_neg) + "%"

    city_data["cityList"]=city_list

    f = open('cityListNew.json', 'w')
    f.write(json.dumps(city_data))
    f.close()




city_map=get_city_map()
aurin_health=get_aurin_health()
aurin_income=get_aurin_income()
senti_data=get_senti()
# get_main_cities(city_map,aurin_health,aurin_income,senti_data)
get_city_list()

