'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
       Na Chang (858604)
       Zepeng Dan (933678)
       Junhan Liu (878637)
       Peishan Li (905508)
'''
import json

def get_lga_name(lga_string):
    lga_name_split = lga_string.split(' ')
    if 'Unincorp' in lga_name_split[0]:
        lga_name = lga_name_split[0] + ' ' + lga_name_split[1]
    elif lga_name_split[0] == 'Campbelltown':
        # print lga_string
        # print lga_name_split
        lga_name = lga_name_split[0] + ' ' + lga_name_split[1]
    else:
        lga_name = ' '.join(lga_name_split[0:-1])
    return lga_name

def process_income():
    with open('data/AURIN_income.json','r') as f:
        str_data=f.read()
        dict_data=json.loads(str_data)
        features = dict_data['features']

    inc_counts={}
    for feature in features:
        properties=feature['properties']
        inc_250=properties['inc_over15_wkly_1_499_%']
        inc_250=inc_250 if inc_250 is not None else 0
        inc_750=properties['inc_over15_wkly_500_999_%']
        inc_750 = inc_750 if inc_750 is not None else 0
        inc_1500=properties['inc_over15_wkly_1000_1999_%']
        inc_1500 = inc_1500 if inc_1500 is not None else 0
        inc_2500=properties['inc_over15_wkly_2000_2999_%']
        inc_2500 = inc_2500 if inc_2500 is not None else 0
        inc_3500=properties['inc_over15_wkly_over_3k_%']
        inc_3500 = inc_3500 if inc_3500 is not None else 0
        inc_average=inc_250*2.5+inc_750*7.5+inc_1500*15+inc_2500*25+inc_3500*35

        lga_name=get_lga_name(properties['lga_name16'])
        inc_counts[lga_name]={"income":inc_average}

    file_income=open("Income.json",'w')
    file_income.write(json.dumps(inc_counts))
    file_income.close()

def process_health_au():
    with open('data/AURIN_health_au.json','r') as f:
        str_data = f.read()
        dict_data = json.loads(str_data)
        features = dict_data['features']

    heal_counts = {}
    for feature in features:
        properties=feature['properties']
        fair_poor=properties['fair_poor_hlth_2_asr']
        if fair_poor is None:
            continue
        lga_name=get_lga_name(properties['lga_name'])
        heal_counts[lga_name]={"fair_poor":fair_poor}

    file_income = open("HealthAU.json", 'w')
    file_income.write(json.dumps(heal_counts))
    file_income.close()

def process_health_vic():
    with open('data/AURIN_health_vic.json','r') as f:
        str_data = f.read()
        dict_data = json.loads(str_data)
        features = dict_data['features']

    heal_counts = {}
    for feature in features:
        properties=feature['properties']
        fair_poor=properties['ppl_reporting_fair_or_poor_hlth_status_perc']
        if fair_poor is None:
            continue
        lga_name=get_lga_name(properties['lga_name'])
        heal_counts[lga_name]={"fair_poor":fair_poor}

    file_income = open("HealthVIC.json", 'w')
    file_income.write(json.dumps(heal_counts))
    file_income.close()




# def process_traf_acc_au():


process_health_au()
process_health_vic()
process_income()

