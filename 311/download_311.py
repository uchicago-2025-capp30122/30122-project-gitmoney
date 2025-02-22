from http_functions import cached_get
from urllib.parse import quote
import json
import time

allowed_short_codes = ['GRAF','SFD','PHF','SIE','SCP','SFB','PCE','SEE','SFA',
                       'SED','SDR','PHB','PBS','SCT','SDP','PCB','SFK','PCC',
                       'VBL','SFN','SFQ','SFC','NAA','PBLDR','PBE']
sc_cat_dict = {'GRAF':'Beautification',
               'SFD':'Streets & Transportation',
               'PHF':'Streets & Transportation',
               'SIE':'Beautification',
               'SCP':'Beautification',
               'SFB':'Streets & Transportation',
               'PCE':'Streets & Transportation',
               'SEE':'Plants, Gardens, & Sustainability',
               'SFA':'Lighting',
               'SED':'Plants, Gardens, & Sustainability',
               'SDR':'Security Cameras',
               'PHB':'Streets & Transportation',
               'PBS':'Streets & Transportation',
               'SCT':'Beautification',
               'SDP':'Streets & Transportation',
               'PCB':'Streets & Transportation',
               'SFK':'Streets & Transportation',
               'PCC':'Streets & Transportation',
               'VBL':'Bike Infrastructure',
               'SFN':'Streets & Transportation',
               'SFQ':'Streets & Transportation',
               'SFC':'Lighting',
               'NAA':'Parks & Rec',
               'PBLDR':'Bike Infrastructure',
               'PBE':'Streets & Transportation'}

def get_311():
    """
    Download the most recent 11,200,000 311 calls
    """
    limit = 1000
    offset = 0
    base_url = "https://data.cityofchicago.org/resource/v6vf-nfxy.json?$query="
    query = f"""
    SELECT sr_number, sr_type, sr_short_code, status, created_date, last_modified_date,
    closed_date, street_address, street_number, street_direction, street_name, duplicate,
    legacy_sr_number, parent_sr_number, ward, latitude, longitude
    ORDER BY sr_number DESC NULL FIRST
    LIMIT 1000 OFFSET {offset}
    """

    calls = []
    count = 0
    for _ in range(11200):
        encoded_query = quote(query)
        url = base_url + encoded_query
        output=json.loads(cached_get(url))
        calls.extend(output)
        offset = offset + limit
        count += 1
        if count % 100 == 0:
            print(count)
        time.sleep(1)

    with open("311_data.json", "w") as rv:
        json.dump(calls, rv)

def clean_311():
    """
    Clean the 311 json data and write a new clean file
    """

    with open("311_data.json",'r') as file:
        reader = json.load(file)

    clean_copy = []
    count = 0
    for call in reader:
        code = call.get('sr_short_code', None)
        if code in allowed_short_codes:
            loc = call.get('location', None)
            if loc is None:
                call['location'] = None
            else:
                call['latitude'] = call['location'].get('latitude',None)
                call['longitude'] = call['location'].get('longitude',None)
            del call['location']
            call['cat'] = sc_cat_dict[code]
            clean_copy.append(call)
        count += 1
        if count % 100 == 0:
            print(count)

    with open("311_clean.json","w") as rv:
        json.dump(clean_copy,rv)
